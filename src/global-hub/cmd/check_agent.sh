#!/bin/bash
# Copyright (c) 2023 Red Hat, Inc.
# Copyright Contributors to the Open Cluster Management project

REPO_DIR="$(cd "$(dirname ${BASH_SOURCE[0]})/.." ; pwd -P)"

output=${REPO_DIR}/output
mkdir -p ${output}

python ${REPO_DIR}/scripts/agent.py "$1" "$2"