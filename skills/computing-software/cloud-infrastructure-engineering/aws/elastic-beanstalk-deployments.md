---
id: computing-software.cloud-infrastructure-engineering.aws.elastic-beanstalk-deployments
name: elastic-beanstalk-deployments
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-beanstalk, beanstalk, eb-cli, ebextensions, platform-hooks, saved-configuration, deployment-policy, rolling-with-additional-batch, immutable-deployment, blue-green, swap-environment-cnames, platform-update, managed-updates, worker-environment, application-version, eb-deploy, procfile, buildfile]
level: practitioner
status: gated
description: "Deploy and operate Elastic Beanstalk environments: EB CLI workflow, .ebextensions and platform hooks, deployment policies, CNAME-swap blue/green, managed updates."
sources: ["https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.deploy-existing-version.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.CNAMESwap.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Beanstalk — configure, deploy, swap, update

**Goal:** an app on Beanstalk whose environment is fully described in source
(`.ebextensions`, platform hooks, saved configuration), deploys with a policy that cannot
leave it half-broken, and takes platform patches on a schedule you chose.

## 1. Workflow with the EB CLI
```bash
pip install awsebcli
eb init -p "Python 3.12" -r eu-west-1 myapp      # writes .elasticbeanstalk/config.yml (commit it, minus env-specific keys)
eb create prod --elb-type application --instance-types t3.small,t3a.small --min-instances 2 --max-instances 6 \
  --envvars DJANGO_SETTINGS_MODULE=app.settings.prod
eb deploy prod            # zips the git HEAD (or `deploy.artifact` from config.yml), uploads an application version, deploys
eb status; eb health --refresh; eb logs --all; eb ssh prod
eb config save prod --cfg prod-v1   # saved configuration -> .elasticbeanstalk/saved_configs/, commit it
```
`eb deploy` bundles **committed** files only unless `--staged`; untracked build output
is silently absent. For compiled artifacts set `deploy: artifact: dist/app.zip` in
`config.yml` or build on the instance with a `Buildfile`.

## 2. Describe the environment in source
Precedence (lowest → highest): platform defaults → saved configuration → `.ebextensions`
→ settings applied directly (`eb setenv`, console). Direct settings **shadow** your
`.ebextensions` forever until removed with `eb config` — the commonest "my file change
does nothing" cause.
```yaml
# .ebextensions/01-options.config
option_settings:
  aws:autoscaling:launchconfiguration:
    IamInstanceProfile: aws-elasticbeanstalk-ec2-role
    DisableIMDSv1: true
  aws:elasticbeanstalk:environment:process:default:
    HealthCheckPath: /health
    Port: '8000'
  aws:elasticbeanstalk:command:
    DeploymentPolicy: RollingWithAdditionalBatch
    BatchSizeType: Percentage
    BatchSize: 30
  aws:elasticbeanstalk:healthreporting:system:
    SystemType: enhanced
  aws:elasticbeanstalk:managedactions:
    ManagedActionsEnabled: true
    PreferredStartTime: "Sun:02:00"
  aws:elasticbeanstalk:managedactions:platformupdate:
    UpdateLevel: minor
    InstanceRefreshEnabled: true
```
Modern Linux platforms (Amazon Linux 2/2023): put scripts in **platform hooks**
(`.platform/hooks/{prebuild,predeploy,postdeploy}/*.sh`, executable, run in order) and
nginx overrides in `.platform/nginx/conf.d/*.conf`. Reserve `.ebextensions` `commands`/
`container_commands` for the legacy need; `container_commands` run after the app is
unpacked at `/var/app/staging` with `leader_only: true` for one-instance jobs (migrations).
`Procfile` defines the process (`web: gunicorn app.wsgi -b 127.0.0.1:8000`).

## 3. Deployment policies
| Policy | Downtime | Capacity during deploy | Rollback |
|---|---|---|---|
| All at once | Yes | Zero | Redeploy old version |
| Rolling | No | Reduced by batch | Failed batch stays; redeploy |
| Rolling with additional batch | No | Full (extra batch launched first) | Same |
| Immutable | No | Full (new ASG, then swap into ELB) | Automatic — new instances terminated on failure |
| Traffic splitting | No | Full | Automatic, canary % for N minutes |
Immutable/traffic-splitting also apply to **configuration changes** that replace
instances (`aws:autoscaling:updatepolicy:rollingupdate`, set `RollingUpdateType: Immutable`),
otherwise an instance-type change takes the whole fleet down.

## 4. Blue/green with CNAME swap
```bash
eb clone prod -n prod-green            # same config + saved application version
eb deploy prod-green --version v42
# smoke-test prod-green.<region>.elasticbeanstalk.com
eb swap prod --destination_name prod-green
```
Swap flips the two environment CNAMEs (Route 53 alias pointing at the EB CNAME follows
automatically). Use `eb terminate prod-green` only after DNS TTL has elapsed. Shared
state (RDS) must **not** be inside the environment — create it separately and pass the
endpoint via env vars, or terminating the environment deletes the database.

## 5. Worker tier
`eb create workers --tier worker` gives an ASG that pulls from an SQS queue via the
`sqsd` daemon and POSTs each message to `http://localhost/` (path from
`aws:elasticbeanstalk:sqsd:HttpPath`). Return 200 to delete the message; anything else
retries after `VisibilityTimeout`. Periodic tasks: `cron.yaml` in the bundle
(`name/url/schedule`), leader-elected via a DynamoDB table EB creates.

## 6. Operating
- Enhanced health reporting (`SystemType: enhanced`) adds per-instance request/latency
  metrics; `eb health` shows `Degraded`/`Severe` with causes.
- Log streaming to CloudWatch: `aws:elasticbeanstalk:cloudwatch:logs StreamLogs: true`.
- Application versions accumulate (default lifecycle keeps 1000); set a lifecycle policy
  (`eb appversion lifecycle`) to delete old ones and their S3 bundles.
- Platform end-of-life: a retired platform branch blocks new environment creation; keep
  `UpdateLevel: minor` managed updates on and migrate major branches deliberately.

## Gotchas
- In single-instance mode the environment security group may allow 0.0.0.0/0 on port 80 (gated: unconfirmed, source is paywalled or blocked); prefer load-balanced mode in private subnets
  (`aws:ec2:vpc` `ELBScheme`/`Subnets`/`ELBSubnets`).
- `eb ssh` needs a key pair set at create time (`--keyname`); otherwise use SSM Session Manager.
- `.ebextensions` `files:` with `mode:` as a string (`"000644"`) — an unquoted octal is misparsed.
- Hook scripts without `#!/bin/bash` and `chmod +x` fail with a cryptic `Command failed on instance` — check `/var/log/eb-engine.log`.
- Instance profile is **not** created automatically in new accounts anymore; create
  `aws-elasticbeanstalk-ec2-role` with the managed `AWSElasticBeanstalkWebTier` policy.
- Unconfirmed: exact supported platform versions change monthly; `eb platform list` before `eb init`.

## Verify
- [ ] `eb config` shows no direct settings overriding `.ebextensions` (diff saved configuration vs environment).
- [ ] Deploying a version that fails `/health` leaves the environment `Ok` on the old version (immutable or traffic-splitting rollback observed).
- [ ] `eb swap` completes with zero failed requests in a load test running through the swap.
- [ ] RDS/state resources live outside the environment stack (`eb terminate --dry-run`-style review of CloudFormation resources).
- [ ] Managed platform update window set and last update succeeded (`eb platform` / console Managed updates tab).

## Checked

Date: 2026-11-02. Confirmed on Elastic Beanstalk Developer Guide pages in sources (Welcome, deploy existing version, ebextensions, extending Linux platforms, CNAME swap, EB CLI): CNAME swap blue/green, ebextensions, EB CLI commands (eb create, eb deploy). Left, marked gated: the single-instance security-group default, not stated on the pages fetched.

Method: documentation only; no commands were run.
