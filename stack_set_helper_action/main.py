import os

from stack_set_helper_action.stackset_helper import StackSetHelper


def run():
    operation = os.getenv("OPERATION")
    stackset_name = os.getenv("STACKSET_NAME")
    stackset_description = os.getenv("STACKSET_DESCRIPTION", stackset_name)
    template_path = os.getenv("TEMPLATE_PATH")
    org_ou_ids = os.getenv("ORG_OU_IDS").split(",")
    account_ids = os.getenv("ACCOUNT_IDS", "").split(",")
    regions = os.getenv("REGIONS").split(",")
    if operation == "deploy":
        deploy(
            stackset_name,
            stackset_description,
            template_path, org_ou_ids,
            account_ids if account_ids != [""] else None,
            regions
        )
    if operation == "delete":
        delete(stackset_name, org_ou_ids, regions)


def deploy(stackset_name, stackset_description, template_path, org_ou_ids, account_ids, regions):
    StackSetHelper(debug=True).deploy(
        stackset_name,
        stackset_description,
        template_path,
        org_ou_ids,
        account_ids,
        regions
    )


def delete(stackset_name, org_ou_ids, regions):
    StackSetHelper(debug=True).delete(stackset_name, org_ou_ids, regions)


if __name__ == "__main__":
    run()
