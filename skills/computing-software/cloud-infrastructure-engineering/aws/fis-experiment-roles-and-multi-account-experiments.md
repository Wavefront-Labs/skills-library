---
id: computing-software.cloud-infrastructure-engineering.aws.fis-experiment-roles-and-multi-account-experiments
name: fis-experiment-roles-and-multi-account-experiments
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fault-injection, fis-role, multi-account-experiment, target-account-configuration, chaos-engineering, iam]
level: advanced
status: docs-checked
description: "Give AWS FIS least-privilege experiment roles, restrict who can start experiments, and run one experiment across several accounts with target account configurations."
sources: ["https://docs.aws.amazon.com/fis/latest/userguide/getting-started-iam-service-role.html", "https://docs.aws.amazon.com/fis/latest/userguide/multi-account.html", "https://docs.aws.amazon.com/fis/latest/userguide/security-iam.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIS experiment roles and multi-account experiments

## 1. Experiment role
FIS assumes a role you provide to perform the fault actions.
Trust policy:
```json
{"Effect": "Allow", "Principal": {"Service": "fis.amazonaws.com"}, "Action": "sts:AssumeRole",
 "Condition": {"StringEquals": {"aws:SourceAccount": "<ACCOUNT_ID>"},
               "ArnLike": {"aws:SourceArn": "arn:aws:fis:<REGION>:<ACCOUNT_ID>:experiment/*"}}}
```
The docs recommend `aws:SourceAccount` and `aws:SourceArn` conditions to prevent the confused deputy problem.
Permissions: start from the AWS managed policies per action family (for example
`AWSFaultInjectionSimulatorEC2Access`, `AWSFaultInjectionSimulatorECSAccess`,
`AWSFaultInjectionSimulatorEKSAccess`; the actions reference lists the policy for each action) and use
them as a model for a scoped-down inline policy. Add permissions for log delivery separately if you enable
experiment logging (see the FIS logging page).

## 2. Who can run experiments
- Control who can start experiments with IAM permissions on the FIS actions (see the FIS
  Identity and Access Management page) and restrict which role they can hand to FIS.
- Add stop conditions: a stop condition stops the experiment when a CloudWatch alarm you
  define reaches its threshold, and a stopped experiment cannot be resumed.

## 3. Multi-account experiments
Run one experiment from an **orchestrator account** that injects faults into several
**target accounts** (e.g. an app spread across accounts, or an AZ power-interruption
scenario across a workload's accounts).
1. In each target account create an IAM role with the action permissions for that account's
   targets, that the orchestrator account's experiment role can assume (see the FIS
   multi-account prerequisites page for the trust policy).
2. The orchestrator experiment role needs `sts:AssumeRole` on each target account role.
3. Template with `"experimentOptions": {"accountTargeting": "multi-account"}` and target
   account configurations:
```bash
aws fis create-target-account-configuration --experiment-template-id EXT123 \
  --account-id <TARGET_ACCOUNT_ID> --role-arn arn:aws:iam::<TARGET_ACCOUNT_ID>:role/FisTargetRole \
  --description "payments account"
```
4. Target accounts with affected resources are notified through their AWS Health dashboards.
   The orchestrator account owns the template and experiment and centralizes logging.
5. Target resources by consistent tags across accounts, and use AZ IDs rather than AZ names when
   filtering by Availability Zone. An action must resolve at least one target in every target account or
   it fails (unless `emptyTargetResolutionMode` is `skip`); action quotas apply per account.

## Gotchas
- Test the experiment role in non-prod before relying on it.

## Verify
- [ ] Experiment role scoped to the targets and actions the template needs.
- [ ] A multi-account template runs in staging, affecting resources in each target account, and stops on alarm.
- [ ] CloudTrail in each target account shows the API calls FIS made.

## Checked
2026-10-28: Confirmed against the FIS User Guide pages getting-started-iam-service-role, multi-account and fis-actions-reference: fis.amazonaws.com trust policy with aws:SourceAccount/aws:SourceArn, the EC2/ECS/EKS managed policy names, orchestrator and target account concepts, target account configuration (account ID, IAM role, optional description), accountTargeting multi-account, sts:AssumeRole permission for target roles, AWS Health notification, tag and AZ ID best practices, emptyTargetResolutionMode skip, and stop conditions via CloudWatch alarms (stop-conditions page). The create-target-account-configuration command passed check_commands.py. Read end to end. Removed as unconfirmed: the Network/RDS/SSM managed policy names, ExternalId trust condition, logs:CreateLogDelivery, fis:StartExperiment/PassRole and template tag conditions, the aws:ResourceTag caveat, and cross-account observability advice. Replaced the made-up account IDs with placeholders.

Method: documentation only; no commands were run.
