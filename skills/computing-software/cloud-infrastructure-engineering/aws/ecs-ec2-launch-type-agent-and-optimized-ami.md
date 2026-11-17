---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-ec2-launch-type-agent-and-optimized-ami
name: ecs-ec2-launch-type-agent-and-optimized-ami
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, ecs-agent, ecs-optimized-ami, ec2-launch-type, capacity-providers]
level: advanced
status: docs-checked
description: "Run ECS on EC2: ECS-optimized AMIs via SSM parameters, ecs.config settings, container agent updates and logs, capacity providers, draining and ENI trunking."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html", "https://github.com/aws/amazon-ecs-agent/blob/master/README.md", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-draining.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 launch type, the ECS agent and ECS-optimized AMIs

## 1. AMI
```bash
aws ssm get-parameter --name /aws/service/ecs/optimized-ami/amazon-linux-2023/recommended/image_id --query Parameter.Value --output text
# arm64: .../amazon-linux-2023/arm64/recommended ; GPU: .../amazon-linux-2023/gpu/recommended
```
The ECS guide recommends the Amazon Linux 2023 variants; the Amazon Linux 2 ECS-optimized AMI reached end of life on 30 June 2026. Use a dynamic Systems Manager parameter in the launch template so each stack deployment picks up a newer AMI. AMIs are not patched at launch: roll to a new AMI as releases appear.

## 2. User data: `/etc/ecs/ecs.config`
```bash
#!/bin/bash
cat >> /etc/ecs/ecs.config <<'E'
ECS_CLUSTER=prod
ECS_ENABLE_TASK_IAM_ROLE=true
ECS_AWSVPC_BLOCK_IMDS=true
ECS_CONTAINER_STOP_TIMEOUT=60s
ECS_IMAGE_PULL_BEHAVIOR=prefer-cached
ECS_ENABLE_SPOT_INSTANCE_DRAINING=true
ECS_INSTANCE_ATTRIBUTES={"workload":"batch"}
E
```
`ECS_AWSVPC_BLOCK_IMDS` blocks instance metadata access for tasks in awsvpc network mode; `ECS_ENABLE_SPOT_INSTANCE_DRAINING` sets the instance to DRAINING on a Spot interruption notice; `ECS_INSTANCE_ATTRIBUTES` only takes effect at first registration (use `PutAttributes` afterwards). `ECS_CONTAINER_STOP_TIMEOUT` defaults to 30s and `ECS_IMAGE_PULL_BEHAVIOR` accepts `default`, `always`, `once` and `prefer-cached`. After editing `ecs.config` on a running instance, restart the agent (`sudo systemctl restart ecs`). The full variable list lives in the agent README on GitHub.

## 3. Capacity providers
Associate the ASG with a capacity provider (managed scaling, managed termination protection and ASG scale-in protection are the relevant settings) and use capacity provider strategies on services.

## 4. Agent operations
- Agent and runtime logs are on the host; see "Viewing Amazon ECS container agent logs" in the ECS guide.
- Prefer rolling to a newer ECS-optimized AMI over updating the agent in place.
- `agentConnected: false` in `describe-container-instances` means the agent cannot reach ECS (check NAT or VPC endpoints). A disconnected agent does not by itself mark containers UNHEALTHY.

## 5. Draining and density
```bash
aws ecs update-container-instances-state --cluster prod --container-instances <ARN> --status DRAINING
aws ecs put-account-setting-default --name awsvpcTrunking --value enabled
```
ENI trunking raises awsvpc task density per instance on supported instance types, but only for container instances launched after the setting is enabled; a trunked instance carries the `ecs.awsvpc-trunk-id` attribute.

## Verify
- [ ] All container instances `ACTIVE`, `agentConnected: true`, current agent version.

## Checked
Checked 2026-10-24 against the ECS developer guide (ECS-optimized AMI, agent configuration) and the amazon-ecs-agent README on GitHub.
Confirmed: AL2023 recommended and AL2 end of life 30 June 2026, no launch-time security updates since June 2024 AMI releases, agent variables and defaults (ECS_CONTAINER_STOP_TIMEOUT 30s, ECS_ENABLE_TASK_IAM_ROLE default false, ECS_AWSVPC_BLOCK_IMDS, ECS_IMAGE_PULL_BEHAVIOR values, ECS_ENABLE_SPOT_INSTANCE_DRAINING, ECS_INSTANCE_ATTRIBUTES), systemctl restart ecs, trunk attribute.
SSM parameter paths for AL2023 x86, arm64 and GPU recommended image_id confirmed; awsvpcTrunking applies only to newly launched instances.
Removed as unconfirmed: local introspection endpoint paths, log file names, instance role policy name, capacity provider scaling percentages, update-container-agent usage.

Method: documentation only; no commands were run.
