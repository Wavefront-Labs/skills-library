---
id: computing-software.devops-ci-cd.spinnaker.aws-ecs-provider-prerequisites
name: aws-ecs-provider-prerequisites
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [aws, ecs, fargate, iam, service-linked-role, awsvpc, task-execution-role]
level: advanced
status: docs-checked
description: "Prepare the Amazon ECS provider: cluster and networking, service-linked IAM roles, task execution role fallback on Fargate, and the clouddriver ecs account block."
sources:
  - https://spinnaker.io/docs/setup/install/providers/aws/aws-ecs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In the ECS provider an Account maps to a Spinnaker AWS account that can authenticate to a given AWS account.

**Cluster and network.** Create the ECS cluster first. With the EC2 launch type it needs enough instance capacity; with Fargate you add none. The `awsvpc` networking mode (required for Fargate) needs a VPC with at least one subnet group and security group visible in Spinnaker; modes like `bridge` need no extra networking.

**Service-linked roles.** The provider requires service-linked roles for Amazon ECS and Application Auto Scaling:

```
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
aws iam create-service-linked-role --aws-service-name ecs.application-autoscaling.amazonaws.com
```

**Task execution role.** Some services, such as those on Fargate, require one. A task definition artifact can name it; otherwise, for a Fargate server group, the provider falls back to the cloud provider account's assumed IAM role, whose trust policy must then allow `ecs-tasks.amazonaws.com` to `sts:AssumeRole`. An optional separate task role for application containers needs the same trust.

**Service Auto Scaling** is optional. Configure scaling policies with the Application Auto Scaling APIs or the ECS console, outside Spinnaker; when deploying a new server group you can enable the option to copy the previous server group's autoscaling policies.

**Spinnaker configuration.** Make sure the AWS provider is enabled, then enable ECS in clouddriver:

```yaml
ecs:
  enabled: true
  accounts:
    - name: ecs-account-name
      awsAccount: aws-account-name
```

`awsAccount` names an existing configured AWS account.

**Native ECS deployments** (one durable ECS service per cluster, updated in place) need no extra Clouddriver configuration; users opt in per deploy stage with the "Use native ECS deployment" checkbox. They require the account to use the long ECS resource ID format so services can be tagged `spinnaker:provider=ecs-native`, extra IAM actions on the SpinnakerManaged role, and, for blue/green, an Application Load Balancer with a production and a test listener rule, an alternate target group and an ECS blue/green service role.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Amazon ECS page. Confirmed cluster, networking, service-linked roles, task execution fallback, auto scaling note and the ecs account block. Removed the Spinnaker 1.18/1.19 version split and the hal command, which the current page does not state; added the native deployment summary.
