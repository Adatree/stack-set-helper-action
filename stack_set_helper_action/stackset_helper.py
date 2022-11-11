import logging
import sys
import time

import boto3

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s")


class StackSetHelper:
    def __init__(self, debug, default_region='ap-southeast-2'):
        self.logger = logging.getLogger(self.__class__.__name__)
        if debug:
            self.logger.setLevel("DEBUG")
        else:
            self.logger.setLevel("INFO")
        self.cfn_client = boto3.client("cloudformation", region_name=default_region)
        self.org_client = boto3.client("organizations", region_name=default_region)

    def _who_am_i(self):
        response = boto3.client("sts").get_caller_identity()
        print(
            f"Calling as {response['UserId']} from account {response['Account']} (Role {response['Arn'].split('/')[1]})"
        )

    def _stackset_exists(self, stackset_name):
        try:
            response = self.cfn_client.describe_stack_set(
                StackSetName=stackset_name, CallAs="DELEGATED_ADMIN"
            )
            self.logger.debug(response)
            result = True
        except self.cfn_client.exceptions.StackSetNotFoundException:
            result = False
        self.logger.debug(f"StackSet {stackset_name} exists: {result}")
        return result

    def _load_template_body(self, template):
        with open(template) as file:
            template_data = file.read()
        self.cfn_client.validate_template(TemplateBody=template_data)
        return template_data

    def _create_stackset(self, stackset_name, stackset_description, template_path):
        stackset_id = self.cfn_client.create_stack_set(
            StackSetName=stackset_name,
            Description=stackset_description,
            TemplateBody=self._load_template_body(template_path),
            Capabilities=["CAPABILITY_NAMED_IAM"],
            PermissionModel="SERVICE_MANAGED",
            AutoDeployment={"Enabled": True, "RetainStacksOnAccountRemoval": False},
            CallAs="DELEGATED_ADMIN",
        )["StackSetId"]
        self.logger.info(
            f"Created new stackset '{stackset_name}' (StackSetId: {stackset_id}) "
        )

    def _get_accounts_in_ou(self, ou_id):
        paginator = self.org_client.get_paginator("list_accounts_for_parent")
        accounts_in_ou = sorted(
            [
                (account["Id"], account["Name"])
                for page in paginator.paginate(ParentId=ou_id)
                for account in page["Accounts"]
            ],
            key=lambda account: account[1],
        )
        return accounts_in_ou

    def _update_stackset(self, stackset_name, stackset_description, template_path):
        operation_id = self.cfn_client.update_stack_set(
            StackSetName=stackset_name,
            Description=stackset_description,
            TemplateBody=self._load_template_body(template_path),
            Capabilities=["CAPABILITY_NAMED_IAM"],
            PermissionModel="SERVICE_MANAGED",
            AutoDeployment={"Enabled": True, "RetainStacksOnAccountRemoval": False},
            OperationPreferences={
                "RegionConcurrencyType": "PARALLEL",
                "FailureToleranceCount": 0,
                "MaxConcurrentCount": 100,
            },
            CallAs="DELEGATED_ADMIN",
        )["OperationId"]
        self.logger.info(
            f"Updating existing stackset: '{stackset_name}' (OperationId: {operation_id}) "
        )
        return operation_id

    def _get_stack_instance_summaries(self, stackset_name, region):
        paginator = self.cfn_client.get_paginator("list_stack_instances")
        try:
            stack_instance_summaries = sorted(
                [
                    summary
                    for page in paginator.paginate(
                        StackSetName=stackset_name,
                        CallAs="DELEGATED_ADMIN",
                        StackInstanceRegion=region,
                    )
                    for summary in page["Summaries"]
                ],
                key=lambda summary: summary["StackSetId"],  # order by StackSetId
            )
        except self.cfn_client.exceptions.StackSetNotFoundException:
            stack_instance_summaries = []
        self.logger.debug(
            f"stack_instance_summaries in region {region}: {stack_instance_summaries}"
        )
        return stack_instance_summaries

    def _create_stack_instances(self, stackset_name, org_ou_ids, account_ids, regions):
        deployment_targets={"OrganizationalUnitIds": org_ou_ids}
        if account_ids:
            deployment_targets["Accounts"] = account_ids
            deployment_targets["AccountFilterType"] = "INTERSECTION"
        operation = self.cfn_client.create_stack_instances(
            StackSetName=stackset_name,
            DeploymentTargets=deployment_targets,
            Regions=regions,
            OperationPreferences={
                "RegionConcurrencyType": "PARALLEL",
                "FailureToleranceCount": 0,
                "MaxConcurrentCount": 100,
            },
            CallAs="DELEGATED_ADMIN",
        )
        for k, v in operation.items():
            self.logger.info(f"key:{k}, value:{v}")
        operation_id = operation["OperationId"]
        self.logger.info(
            f"Stackset '{stackset_name}': Creating stack instances (org_ou_ids: {org_ou_ids}, regions: {regions}, OperationId: {operation_id}) "
        )
        return operation_id

    def _update_stack_instances(self, stackset_name, org_ou_ids, account_ids, regions):
        deployment_targets={"OrganizationalUnitIds": org_ou_ids}
        if account_ids:
            deployment_targets["Accounts"] = account_ids
            deployment_targets["AccountFilterType"] = "INTERSECTION"
        operation_id = self.cfn_client.update_stack_instances(
            StackSetName=stackset_name,
            DeploymentTargets=deployment_targets,
            Regions=regions,
            OperationPreferences={
                "RegionConcurrencyType": "PARALLEL",
                "FailureToleranceCount": 0,
                "MaxConcurrentCount": 100,
            },
            CallAs="DELEGATED_ADMIN",
        )["OperationId"]
        self.logger.info(
            f"Stackset '{stackset_name}': Updating stack instances (org_ou_ids: {org_ou_ids}, regions: {regions}, OperationId: {operation_id}) "
        )
        return operation_id

    def _wait_for_operation_to_finish(self, stackset_name, operation_id):
        done = False
        while not done:
            time.sleep(5)
            stackset_operation = self.cfn_client.describe_stack_set_operation(
                StackSetName=stackset_name,
                OperationId=operation_id,
                CallAs="DELEGATED_ADMIN",
            )["StackSetOperation"]
            self.logger.debug(f"Operation status: {stackset_operation}")
            current_operation_status = stackset_operation["Status"]
            self.logger.info(
                f"Stackset '{stackset_name}': Waiting for operation {operation_id} to finish (current status: {current_operation_status})."
            )
            done = current_operation_status in ["SUCCEEDED", "FAILED", "STOPPED"]

    def _deploy_stackset(self, stackset_name, stackset_description, template_path):
        if not self._stackset_exists(stackset_name):
            self._create_stackset(stackset_name, stackset_description, template_path)
        else:
            operation_id = self._update_stackset(
                stackset_name, stackset_description, template_path
            )
            self._wait_for_operation_to_finish(stackset_name, operation_id)

    def _deploy_stack_instances(self, stackset_name, org_ou_id, account_ids, region):
        stack_instance_summaries = self._get_stack_instance_summaries(
            stackset_name, region
        )
        if not stack_instance_summaries:
            operation_id = self._create_stack_instances(
                stackset_name, [org_ou_id], account_ids, [region]
            )
        else:
            operation_id = self._update_stack_instances(
                stackset_name, [org_ou_id], account_ids, [region]
            )
        self._wait_for_operation_to_finish(stackset_name, operation_id)

    def _delete_stack_instances(self, stackset_name, org_ou_id, region):
        stack_instance_summaries = self._get_stack_instance_summaries(
            stackset_name, region
        )
        if stack_instance_summaries:
            operation_id = self.cfn_client.delete_stack_instances(
                StackSetName=stackset_name,
                DeploymentTargets={"OrganizationalUnitIds": [org_ou_id]},
                Regions=[region],
                RetainStacks=False,
                CallAs="DELEGATED_ADMIN",
            )["OperationId"]
            self.logger.info(
                f"Stackset '{stackset_name}': Deleting stack instances (org_ou_id: {org_ou_id}, region: {region}, OperationId: {operation_id}) "
            )
            self._wait_for_operation_to_finish(stackset_name, operation_id)
        else:
            self.logger.info(
                f"Stackset '{stackset_name}': Deleting stack instances (org_ou_id: {org_ou_id}, region: {region}) - nothing to do"
            )

    def _delete_stackset(self, stackset_name):
        if self._stackset_exists(stackset_name):
            self.cfn_client.delete_stack_set(
                StackSetName=stackset_name, CallAs="DELEGATED_ADMIN"
            )
            self.logger.info(f"Stackset '{stackset_name}': Deleting")
        else:
            self.logger.info(f"Stackset '{stackset_name}': Deleting - nothing to do")

    def deploy(
        self, stackset_name, stackset_description, template_path, org_ou_ids, account_ids=None, regions=None
    ):
        self.logger.info(
            f"Deploying stackset: '{stackset_name}' (org_ou_ids: {org_ou_ids}, regions: {regions})"
        )
        self._deploy_stackset(stackset_name, stackset_description, template_path)

        for org_ou_id in org_ou_ids:
            for region in regions:
                self._deploy_stack_instances(stackset_name, org_ou_id, account_ids, region)
        self.logger.info(f"Deploying stackset: '{stackset_name}' - success")

    def delete(self, stackset_name, org_ou_ids, regions):
        self.logger.info(
            f"Deleting stackset: '{stackset_name}' (org_ou_ids: {org_ou_ids}, regions: {regions})"
        )
        for org_ou_id in org_ou_ids:
            for region in regions:
                self._delete_stack_instances(stackset_name, org_ou_id, region)
        self._delete_stackset(stackset_name)
        self.logger.info(f"Deleting stackset: '{stackset_name}' - success")


if __name__ == "__main__":
    sys.exit(run_ssh())
