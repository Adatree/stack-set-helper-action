import os

from stack_set_helper_action.exceptions import StackSetHelperException
from stack_set_helper_action.stackset_helper import StackSetHelper


def run():
    operation = os.getenv("OPERATION")
    stackset_name = os.getenv("STACKSET_NAME")
    stackset_description = os.getenv("STACKSET_DESCRIPTION", stackset_name)
    template_path = os.getenv("TEMPLATE_PATH")
    org_ou_ids = os.getenv("ORG_OU_IDS").split(",")
    account_ids = os.getenv("ACCOUNT_IDS", None)
    regions = os.getenv("REGIONS").split(",")
    debug = os.environ.get("DEBUG") in ["true", "True"]
    if operation == "deploy":
        deploy(stackset_name, stackset_description, template_path, org_ou_ids, account_ids, regions, debug)
    if operation == "delete":
        delete(stackset_name, org_ou_ids, regions, debug)


def deploy(stackset_name, stackset_description, template_path, org_ou_ids, account_ids, regions, debug):
    if account_ids and len(account_ids) == 0:
        raise StackSetHelperException("Cannot process an empty account list")
    StackSetHelper(debug).deploy(
        stackset_name,
        stackset_description,
        template_path,
        org_ou_ids,
        account_ids,
        regions
    )


def delete(stackset_name, org_ou_ids, regions, debug):
    StackSetHelper(debug).delete(stackset_name, org_ou_ids, regions)


if __name__ == "__main__":
    run()
