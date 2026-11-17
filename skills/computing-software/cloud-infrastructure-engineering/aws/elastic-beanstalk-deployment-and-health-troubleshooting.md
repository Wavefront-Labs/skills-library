---
id: computing-software.cloud-infrastructure-engineering.aws.elastic-beanstalk-deployment-and-health-troubleshooting
name: elastic-beanstalk-deployment-and-health-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-beanstalk, eb-troubleshooting, enhanced-health, eb-logs, eb-engine-log, severe-health]
level: practitioner
status: docs-checked
description: "Fix failed Elastic Beanstalk deployments and Severe/Degraded health: events, eb-engine.log, bundle logs, enhanced health causes, aborted updates and rebuild."
sources: ["https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/troubleshooting.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Beanstalk deployment and health troubleshooting

## 1. Start with events and health causes
```bash
eb events -f                         # or:
aws elasticbeanstalk describe-events --environment-name app-prod --max-items 30 \
  --query 'Events[].[EventDate,Severity,Message]' --output table
aws elasticbeanstalk describe-environment-health --environment-name app-prod \
  --attribute-names All --query '{c:Color,s:HealthStatus,causes:Causes}'
aws elasticbeanstalk describe-instances-health --environment-name app-prod --attribute-names All
eb health --refresh
```
Enhanced health reporting (`SystemType=enhanced`) lists the causes behind a colour; read them
before touching the environment.

## 2. Logs
```bash
eb logs --all          # bundle logs from all instances
aws elasticbeanstalk request-environment-info --environment-name app-prod --info-type bundle
aws elasticbeanstalk retrieve-environment-info --environment-name app-prod --info-type bundle
```
Useful files on the instance:
- `/var/log/eb-engine.log`: errors, startup failures and deployment issues; first place for failed deployments.
- `/var/log/web.stdout.log`: your application's output.
Stream to CloudWatch Logs with `StreamLogs=true` in the `aws:elasticbeanstalk:cloudwatch:logs` namespace
(creates log groups for proxy and deployment logs).

## 3. Common failures
| Symptom | Fix |
|---|---|
| Deployment timed out | Raise `Timeout` in `aws:elasticbeanstalk:command` (default 600 s, range 1 to 3600; Beanstalk adds 240 s internally, so the effective default is 840 s) |
| Degraded after deploy | Check `HealthCheckPath` in the `aws:elasticbeanstalk:environment:process:default` namespace (default `/`); the app must answer it quickly |
| Environment stuck updating | `aws elasticbeanstalk abort-environment-update`; if the environment is unrecoverable, rebuild it or launch a new one |

## 4. Recovery actions
- `aws elasticbeanstalk update-environment --version-label <previous>` redeploys an existing
  application version.
- `eb swap` swaps CNAMEs back if you used blue/green.
- `rebuild-environment` recreates the environment's resources; decouple databases first
  (see the Beanstalk RDS decoupling skill).

## Gotchas
- Platform updates can introduce failures that look like your deploy; check the platform
  version in events.

## Verify
- [ ] Health `Green/Ok` with no causes; `eb health` shows all instances Ok.
- [ ] Logs stream to CloudWatch when `StreamLogs=true`.
- [ ] Redeploying the previous version label works in a staging environment.

## Checked
2026-10-28: Confirmed against the Beanstalk Developer Guide troubleshooting, health-enhanced, logging, command-options-general and CNAME swap pages: eb-engine.log and web.stdout.log, StreamLogs, aws:elasticbeanstalk:command Timeout (default 600, 1 to 3600, plus 240 s added internally), HealthCheckPath default /, SystemType enhanced, rebuild advice. Read end to end. Removed as unconfirmed: eb-hooks.log and nginx log paths, the 502/port 5000 explanation, quoted health cause strings, ASG health-check-type advice, container_commands/leader_only notes, root-volume note, and the table rows built on them.

Method: documentation only; no commands were run.
