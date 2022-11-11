


@click.group("stackset-helper")
def run_ssh():
    pass


@run_ssh.command()
@click.option("--stackset-name", type=str, default=(), required=True)
@click.option("--stackset-description", type=str, default=(), required=True)
@click.option("--template-path", type=str, default=(), required=True)
@click.option("--org-ou-ids", type=str, default=(), multiple=True, required=True)
@click.option("--account-ids", type=str, default=(), multiple=True, required=False)
@click.option("--region", type=str, default=(), multiple=True, required=True)
@click.option("--debug", is_flag=True)
def deploy(
    stackset_name, stackset_description, template_path, org_ou_ids, account_ids, region, debug
):
    if account_ids and len(account_ids) == 0:
        raise DeployToolsException("Cannot process an empty account list")
    StackSetHelper(debug=debug).deploy(
        stackset_name, stackset_description, template_path, [*org_ou_ids], [*account_ids], [*region]
    )


@run_ssh.command()
@click.option("--stackset-name", type=str, default=(), required=True)
@click.option("--org-ou-id", type=str, default=(), multiple=True, required=True)
@click.option("--region", type=str, default=(), multiple=True, required=True)
@click.option("--debug", is_flag=True)
def delete(stackset_name, org_ou_id, region, debug):
    StackSetHelper(debug=debug).delete(stackset_name, [*org_ou_id], [*region])
