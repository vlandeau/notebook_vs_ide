#!/bin/bash
set -eu

CLUSTER_ID=first-run-compute-environment_Batch_ecdde9a9-30c8-3a03-a8f1-25a24ea20fbc
TASK_FAMILY=Ekilibr8-Test

echo "Deleting Task :"
TASK_ARN=$(aws ecs list-tasks \
    --cluster ${CLUSTER_ID} \
    --family ${TASK_FAMILY} | \
    jq -r '.taskArns[0]'\
)
echo "\t- CLUSTER_ID=${CLUSTER_ID}"
echo "\t- TASK_ARN=${TASK_ARN}"
aws ecs stop-task \
    --cluster ${CLUSTER_ID} \
    --task "${TASK_ARN}"


echo "Deleting Task definition"
TASK_DEFINITION_ARN=$(aws ecs list-task-definitions \
    --family-prefix ${TASK_FAMILY} | \
    jq -r '.taskDefinitionArns[0]' \
)
echo "\t- TASK_FAMILY=${TASK_FAMILY}"
echo "\t- TASK_DEFINITION_ARN=${TASK_DEFINITION_ARN}"
aws ecs deregister-task-definition \
    --task-definition "${TASK_DEFINITION_ARN}"
