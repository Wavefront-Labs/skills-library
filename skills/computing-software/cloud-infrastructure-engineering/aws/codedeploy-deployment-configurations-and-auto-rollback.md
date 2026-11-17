---
id: computing-software.cloud-infrastructure-engineering.aws.codedeploy-deployment-configurations-and-auto-rollback
name: codedeploy-deployment-configurations-and-auto-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, codedeploy, deployment-configuration, auto-rollback, minimum-healthy-hosts, canary-deployment, alarm-rollback]
level: practitioner
status: docs-checked
description: "Choose and create CodeDeploy deployment configurations for EC2, Lambda and ECS (minimum healthy hosts, zonal, canary, linear) and wire CloudWatch-alarm automatic rollback."
sources: ["https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CodeDeploy deployment configurations and auto-rollback

## 1. Built-in configurations
| Platform | Configs |
|---|---|
| EC2/on-prem | `CodeDeployDefault.AllAtOnce`, `HalfAtATime`, `OneAtATime` (the default if you name none) |
| Lambda | `CodeDeployDefault.LambdaAllAtOnce`, `LambdaCanary10Percent5Minutes` (also 10, 15, 30 minutes), `LambdaLinear10PercentEvery1Minute` (also `Every2Minutes`, `Every3Minutes`, `Every10Minutes`) |
| ECS | `CodeDeployDefault.ECSAllAtOnce`, `ECSCanary10Percent5Minutes` / `ECSCanary10Percent15Minutes`, `ECSLinear10PercentEvery1Minutes` / `ECSLinear10PercentEvery3Minutes` |
EC2 configs define **minimum healthy hosts**. With `OneAtATime` on a multi-instance group the
deployment succeeds only if all instances succeed, except that a failure on the last instance still
counts as success (only one instance may be offline at a time). With `HalfAtATime` (up to half, rounded
down, at a time) it succeeds if at least half (rounded up) succeed; with nine instances, 4 at a time
and 5 successes needed. `AllAtOnce` succeeds if even one instance succeeds. With a Network Load Balancer on
ECS only `CodeDeployDefault.ECSAllAtOnce` is supported. No predefined configuration supports zonal configuration.

## 2. Custom configurations
```bash
# EC2: keep 75% healthy, deploy zone by zone
aws deploy create-deployment-config --deployment-config-name Web75Zonal \
  --compute-platform Server \
  --minimum-healthy-hosts type=FLEET_PERCENT,value=75 \
  --zonal-config 'firstZoneMonitorDurationInSeconds=600,monitorDurationInSeconds=300,minimumHealthyHostsPerZone={type=HOST_COUNT,value=1}'
# Lambda: 5% for 10 minutes, then the rest
aws deploy create-deployment-config --deployment-config-name Canary5Pct10Min \
  --compute-platform Lambda \
  --traffic-routing-config 'type=TimeBasedCanary,timeBasedCanary={canaryPercentage=5,canaryInterval=10}'
```
- `--compute-platform` is `Server`, `Lambda` or `ECS`. Canary or linear step is a percentage from 1 to 99; interval is in minutes (traffic routing types `TimeBasedCanary`, `TimeBasedLinear`, `AllAtOnce`).
- Zonal configuration deploys one Availability Zone at a time (otherwise CodeDeploy picks a random selection of hosts across the Region). Only in-place deployments to EC2 instances: not blue/green, not on-premises. Minimum healthy hosts per zone defaults to 0 percent. Rollbacks do NOT go zone by zone: CodeDeploy rolls back random hosts.
- CloudFormation-managed ECS blue/green deployments cannot use custom canary or linear configurations.

## 3. Automatic rollback
```bash
aws deploy update-deployment-group --application-name web --current-deployment-group-name prod \
  --auto-rollback-configuration enabled=true,events=DEPLOYMENT_FAILURE,DEPLOYMENT_STOP_ON_ALARM \
  --alarm-configuration 'enabled=true,ignorePollAlarmFailure=false,alarms=[{name=web-5xx-high},{name=web-p99-latency}]'
```
- A rollback is a **new deployment** (new deployment ID) of the last known good revision, not a restore. You can override the group's rollback setting when you create a deployment, and use SNS notifications to hear about automatic rollbacks.
- On EC2 the agent first removes files listed in the instance's cleanup file (the files the last successful deployment installed), then deploys. Files created by your scripts are not cleaned up or reverted: make scripts idempotent.
- Files already in the target location can make a deployment fail, be overwritten or be retained (choose per deployment). Rolling back after a failed OVERWRITE deployment can lose files you expected to retain, because the failed deployment already deleted them.
- Choose alarms that react quickly to the new version (for example target-group 5xx, an error metric for the new Lambda alias version, business metrics).

## Gotchas
- No predefined config does zonal deployments: create your own.
- `ignorePollAlarmFailure` is the alarm-configuration switch for what to do when CloudWatch cannot be polled; keep it `false` unless you accept deploying blind.
- Lifecycle hook scripts and Lambda validation hooks (see the CodeDeploy AppSpec reference) are the place to gate a deployment on a health check.

## Verify
- [ ] Deployment group shows auto-rollback on failure and on alarm, with fast-reacting alarms.
- [ ] A deliberately broken release in staging trips the alarm and rolls back automatically.
- [ ] Canary/linear configs match risk tolerance; zonal config for EC2 fleets across AZs.

## Checked
2026-10-28. Confirmed on the deployment-configurations, deployments-rollback-and-redeploy and deployment-configurations-create pages, and the codedeploy botocore model (`create-deployment-config` members, platform and routing enums, `AutoRollbackEvent`). Fixed: zonal support limits and the rollback-not-zonal rule, default config, cleanup-file behaviour, OneAtATime semantics. Removed as unconfirmed: "Lambda/ECS rollback shifts traffic back immediately", pre-existing ALARM / same-region claims, minimum-healthy-hosts "not enough healthy instances" error, the BeforeAllowTraffic/ValidateService specifics, ignorePollAlarmFailure=true explanation beyond its name.
Method: documentation only; no commands were run.
