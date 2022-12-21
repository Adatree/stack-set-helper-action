#!/bin/sh -l

export OPERATION=$1
export STACKSET_NAME=$2
export STACKSET_DESCRIPTION=$3
export TEMPLATE_PATH=$4
export ORG_OU_IDS=$5
export ACCOUNT_IDS=$6
export REGIONS=$7

. /./venv/bin/activate
python /stack_set_helper_action/main.py
