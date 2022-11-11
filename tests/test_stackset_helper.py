from unittest.mock import ANY, patch, MagicMock
from click.testing import CliRunner

from stack_set_helper_action.stackset_helper import deploy, StackSetHelper


@patch("boto3.client")
@patch("builtins.open", MagicMock())
def test_deploy_stack_set_create(mock_boto):
    cfn_client = MagicMock()
    cfn_client.describe_stack_set_operation.return_value = {
        "StackSetOperation": {
            "Status": "SUCCEEDED"
        }
    }
    cfn_client._get_stack_instance_summaries.return_value = False
    mock_boto.return_value = cfn_client
    stackset_helper = StackSetHelper(debug=False)
    stackset_name = "an awesome stack"
    stackset_description = "description"
    template_path = "some path"
    org_ou_ids = ["ou_id"]
    regions = ["ap-southeast-2"]
    stackset_helper.deploy(
        stackset_name=stackset_name,
        stackset_description=stackset_description,
        template_path=template_path,
        org_ou_ids=org_ou_ids,
        regions=regions
    )
    assert cfn_client.describe_stack_set_operation.call_count == 2
    assert cfn_client.update_stack_instances.call_count == 0
    cfn_client.create_stack_instances.assert_called_once_with(
        StackSetName=stackset_name,
        DeploymentTargets={"OrganizationalUnitIds": org_ou_ids},
        Regions=regions,
        OperationPreferences={
            "RegionConcurrencyType": "PARALLEL",
            "FailureToleranceCount": 0,
            "MaxConcurrentCount": 100,
        },
        CallAs="DELEGATED_ADMIN",
    )


@patch("boto3.client")
@patch("builtins.open", MagicMock())
def test_deploy_stack_set_update(mock_boto):
    cfn_client = MagicMock()
    cfn_client.describe_stack_set_operation.return_value = {
        "StackSetOperation": {
            "Status": "SUCCEEDED"
        }
    }
    cfn_client_paginator = MagicMock()
    cfn_client_paginator.paginate.return_value = [
        {
            "Summaries": [{
                "StackSetId": "stack_set_id"
            }]
        }
    ]
    cfn_client.get_paginator.return_value = cfn_client_paginator
    mock_boto.return_value = cfn_client
    stackset_helper = StackSetHelper(debug=True)
    stackset_name = "an awesome stack"
    stackset_description = "description"
    template_path = "some path"
    org_ou_ids = ["org_ou_ids"]
    regions = ["ap-southeast-2"]
    stackset_helper.deploy(
        stackset_name=stackset_name,
        stackset_description=stackset_description,
        template_path=template_path,
        org_ou_ids=org_ou_ids,
        regions=regions
    )
    assert cfn_client.describe_stack_set_operation.call_count == 2
    assert cfn_client.create_stack_instances.call_count == 0
    cfn_client.update_stack_instances.assert_called_once_with(
        StackSetName=stackset_name,
        DeploymentTargets={"OrganizationalUnitIds": org_ou_ids},
        Regions=regions,
        OperationPreferences={
            "RegionConcurrencyType": "PARALLEL",
            "FailureToleranceCount": 0,
            "MaxConcurrentCount": 100,
        },
        CallAs="DELEGATED_ADMIN",
    )


@patch("boto3.client")
@patch("builtins.open", MagicMock())
def test_deploy_stack_set_to_account_create(mock_boto):
    cfn_client = MagicMock()
    cfn_client.describe_stack_set_operation.return_value = {
        "StackSetOperation": {
            "Status": "SUCCEEDED"
        }
    }
    cfn_client._get_stack_instance_summaries.return_value = False
    mock_boto.return_value = cfn_client
    stackset_helper = StackSetHelper(debug=True)
    stackset_name = "an awesome stack"
    stackset_description = "description"
    template_path = "some path"
    org_ou_ids = ["org_ou_ids"]
    account_ids = ["account-valid-id"]
    regions = ["ap-southeast-2"]
    stackset_helper.deploy(
        stackset_name=stackset_name,
        stackset_description=stackset_description,
        template_path=template_path,
        org_ou_ids=org_ou_ids,
        account_ids=account_ids,
        regions=regions
    )
    assert cfn_client.describe_stack_set_operation.call_count == 2
    assert cfn_client.update_stack_instances.call_count == 0
    cfn_client.create_stack_instances.assert_called_once_with(
        StackSetName=stackset_name,
        DeploymentTargets={"OrganizationalUnitIds": org_ou_ids, "Accounts": account_ids,
                           "AccountFilterType": "INTERSECTION"},
        Regions=regions,
        OperationPreferences={
            "RegionConcurrencyType": "PARALLEL",
            "FailureToleranceCount": 0,
            "MaxConcurrentCount": 100,
        },
        CallAs="DELEGATED_ADMIN",
    )


@patch("boto3.client")
@patch("builtins.open", MagicMock())
def test_deploy_stack_set_to_account_update(mock_boto):
    cfn_client = MagicMock()
    cfn_client.describe_stack_set_operation.return_value = {
        "StackSetOperation": {
            "Status": "SUCCEEDED"
        }
    }
    cfn_client_paginator = MagicMock()
    cfn_client_paginator.paginate.return_value = [
        {
            "Summaries": [{
                "StackSetId": "stack_set_id"
            }]
        }
    ]
    cfn_client.get_paginator.return_value = cfn_client_paginator
    mock_boto.return_value = cfn_client
    stackset_helper = StackSetHelper(debug=False)
    stackset_name = "an awesome stack"
    stackset_description = "description"
    template_path = "some path"
    org_ou_ids = ["org_ou_ids"]
    account_ids = ["account-valid-id"]
    regions = ["ap-southeast-2"]
    stackset_helper.deploy(
        stackset_name=stackset_name,
        stackset_description=stackset_description,
        template_path=template_path,
        org_ou_ids=org_ou_ids,
        account_ids=account_ids,
        regions=regions
    )
    assert cfn_client.describe_stack_set_operation.call_count == 2
    assert cfn_client.create_stack_instances.call_count == 0
    cfn_client.update_stack_instances.assert_called_once_with(
        StackSetName=stackset_name,
        DeploymentTargets={"OrganizationalUnitIds": org_ou_ids, "Accounts": account_ids,
                           "AccountFilterType": "INTERSECTION"},
        Regions=regions,
        OperationPreferences={
            "RegionConcurrencyType": "PARALLEL",
            "FailureToleranceCount": 0,
            "MaxConcurrentCount": 100,
        },
        CallAs="DELEGATED_ADMIN",
    )


def test_raise_exception_when_empty_account_list_provided():
    runner = CliRunner()
    result = runner.invoke(deploy, [
        "--stackset_name", "ignore",
        "--stackset-description", "ignore",
        "--template-path", "ignore",
        "--org-ou-id", "ignore",
        "--account-ids", ""
    ]
                           )
    assert result.exit_code == 2
