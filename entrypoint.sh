#!/bin/sh -l

OPERATION=$1
STACKSET_NAME=$2
STACKSET_DESCRIPTION=$3
TEMPLATE_PATH=$4
ORG_OU_IDS=$5
ACCOUNT_IDS=$6
REGION=$7

. ./venv/bin/activate
python stack_set_helper_action/main.py
