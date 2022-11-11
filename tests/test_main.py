from pytest import raises
from unittest.mock import patch

from stack_set_helper_action.exceptions import StackSetHelperException
from stack_set_helper_action.main import run

stackset_name = "stackset_name"
template_path = "template_path"
org_ou_ids = "ou-12345"
account_ids = "320312"
regions = "ap-southeast-2,us-east-1"


def test_deploy_without_account_ids(monkeypatch):
    monkeypatch.setenv("OPERATION", "deploy")
    monkeypatch.setenv("STACKSET_NAME", stackset_name)
    monkeypatch.setenv("TEMPLATE_PATH", template_path)
    monkeypatch.setenv("ORG_OU_IDS", org_ou_ids)
    monkeypatch.setenv("ACCOUNT_IDS", account_ids)
    monkeypatch.setenv("REGIONS", regions)


def test_deploy_with_account_ids(monkeypatch):
    monkeypatch.setenv("OPERATION", "deploy")
    monkeypatch.setenv("STACKSET_NAME", stackset_name)
    monkeypatch.setenv("TEMPLATE_PATH", template_path)
    monkeypatch.setenv("ORG_OU_IDS", org_ou_ids)
    monkeypatch.setenv("ACCOUNT_IDS", account_ids)
    monkeypatch.setenv("REGIONS", regions)


def test_deploy_with_empty_account_list_throws_exceptions(monkeypatch):
    monkeypatch.setenv("OPERATION", "deploy")
    monkeypatch.setenv("STACKSET_NAME", stackset_name)
    monkeypatch.setenv("TEMPLATE_PATH", template_path)
    monkeypatch.setenv("ORG_OU_IDS", org_ou_ids)
    monkeypatch.setenv("ACCOUNT_IDS", "       ,       ")
    monkeypatch.setenv("REGIONS", regions)
    with raises(StackSetHelperException):
        run()


def test_delete(monkeypatch):
    monkeypatch.setenv("OPERATION", "delete")
    monkeypatch.setenv("STACKSET_NAME", stackset_name)
    monkeypatch.setenv("ORG_OU_IDS", org_ou_ids)
    monkeypatch.setenv("ACCOUNT_IDS", account_ids)
    monkeypatch.setenv("REGIONS", regions)
    with patch("stack_set_helper_action.main.StackSetHelper.delete") as stackset_helper_delete:
        run()
        stackset_helper_delete.assert_called_with(
            stackset_name,
            [org_ou_ids],
            ['ap-southeast-2', 'us-east-1']
        )
