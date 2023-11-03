#!bin/bash
uvicorn app.main:app --host=0.0.0.0 --reload 


$taskDef = aws ecs describe-task-definition --task-definition tax-w1 --region=eu-west-1 | ConvertFrom-Json
$taskDef.taskDefinition.containerDefinitions[0].image = "<container>:<version>"
$containerDefinitions = $taskDef.taskDefinition.containerDefinitions | ConvertTo-Json -Depth 10
aws ecs register-task-definition --family "tax-w1" --container-definitions $containerDefinitions 