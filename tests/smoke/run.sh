#!/usr/bin/env bash

echo ${BASH_SOURCE[0]}

#echo $(readlink -f ${BASH_SOURCE[0]})

#echo $(dirname $(readlink -f ${BASH_SOURCE[0]}))
#echo $(dirname $(readlink -f "${BASH_SOURCE[0]}"))

SCRIPT_PATH=$(readlink -f "${BASH_SOURCE[0]}")
SCRIPT_ROOT=$(dirname "${SCRIPT_PATH}")
echo ${SCRIPT_ROOT}

${SCRIPT_ROOT}/../../.venv/bin/mediadex -c ${SCRIPT_ROOT}/conf/no-paths.yaml
${SCRIPT_ROOT}/../../.venv/bin/mediadex -c ${SCRIPT_ROOT}/conf/no-backend.yaml

docker compose -f ${SCRIPT_ROOT}/docker/compose.yaml -p mediadex-test up -d
${SCRIPT_ROOT}/../../.venv/bin/mediadex -c ${SCRIPT_ROOT}/conf/docker.yaml
