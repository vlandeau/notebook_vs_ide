#!/bin/bash
set -eu

CLUSTER_ID=first-run-compute-environment_Batch_ecdde9a9-30c8-3a03-a8f1-25a24ea20fbc
TASK_ROLE_ARN=arn:aws:iam::366851335136:role/ecsExecutionRoleDockerHub
TASK_FAMILY=Ekilibr8-Test
SUBNET=subnet-0d28056e4a9f006cc
SECURITY_GROUP=sg-08df85a6d005ce660
SCRIPT_PATH="$( cd "$(dirname "$0")" &>/dev/null; pwd -P )"
CREATED_BY_TAG="key=Created-By,value=$(basename $0)"
TEMPLATE_PATH="$SCRIPT_PATH"/templates
CONTAINER_DEFINITION_TEMPLATE=$TEMPLATE_PATH/task_definition.template.json
CONTAINER_DEFINITION=$TEMPLATE_PATH/task_definition.json

jq '.containerDefinitions[0].image = "ekinoxio/bootcamp-2021-01-dash:'"$IMAGE_TAG"'"' "$CONTAINER_DEFINITION_TEMPLATE" > "$CONTAINER_DEFINITION"

aws ecs register-task-definition \
    --family ${TASK_FAMILY} \
    --task-role-arn ${TASK_ROLE_ARN} \
    --execution-role-arn ${TASK_ROLE_ARN} \
    --network-mode awsvpc \
    --cpu 1024 \
    --memory 8192 \
    --tags "$CREATED_BY_TAG" \
    --cli-input-json file://"$CONTAINER_DEFINITION"

rm "$CONTAINER_DEFINITION"

TASK_DEFINITION_ARN=$(aws ecs list-task-definitions \
    --family-prefix Ekilibr8-Test | \
    jq -r '.taskDefinitionArns[0]' \
)

aws ecs run-task \
    --count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[${SUBNET}],securityGroups=[${SECURITY_GROUP}],assignPublicIp=ENABLED}" \
    --tags "$CREATED_BY_TAG" \
    --task-definition "${TASK_DEFINITION_ARN}" \
    --cluster=${CLUSTER_ID}

TASK_ARN=$(aws ecs list-tasks \
    --cluster ${CLUSTER_ID} \
    --family ${TASK_FAMILY} | \
    jq -r '.taskArns[0]'\
)

sleep 10

NETWORK_ENI=$(aws ecs describe-tasks \
    --cluster ${CLUSTER_ID} \
    --tasks "${TASK_ARN}" | \
    jq -r '.tasks[0].attachments[0].details[] | select(.name == "networkInterfaceId").value')
PUBLIC_IP=$(aws ec2 describe-network-interfaces \
    --network-interface-ids "${NETWORK_ENI}" | \
    jq -r '.NetworkInterfaces[0].Association.PublicIp')

echo "Running on http://${PUBLIC_IP}"
