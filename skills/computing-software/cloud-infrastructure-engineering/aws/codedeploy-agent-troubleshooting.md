---
id: computing-software.cloud-infrastructure-engineering.aws.codedeploy-agent-troubleshooting
name: codedeploy-agent-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, codedeploy, codedeploy-agent, deployment-troubleshooting, lifecycle-hooks, appspec, ec2-deployment]
level: practitioner
status: docs-checked
description: "Diagnose CodeDeploy EC2/on-prem deployments: agent health, agent and deployment logs, instance profile and endpoint access, script timeouts and ApplicationStop failures."
sources: ["https://docs.aws.amazon.com/codedeploy/latest/userguide/troubleshooting-deployments.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-verify.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install-ssm.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-cloudwatch-agent.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CodeDeploy agent troubleshooting

## Install and check
Install through Systems Manager Distributor (package `AWSCodeDeployAgent`; see the install-with-SSM page for the command and a State Manager association that keeps it updated), then check:
```bash
systemctl status codedeploy-agent                              # Amazon Linux, RHEL, Ubuntu
powershell.exe -Command Get-Service -Name CodeDeployagent      # Windows
```
Linux logs:
- Agent: `/var/log/aws/codedeploy-agent/codedeploy-agent.log`
- Deployment/script output: `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log`
- Updater: `/var/log/aws/codedeploy-agent/codedeploy-agent-updater.log` (agent 2.0.x and later), `/tmp/codedeploy-agent.update.log` (1.8.x and earlier)
- Deployment archive: `/opt/codedeploy-agent/deployment-root/<deployment-group-id>/<deployment-id>/deployment-archive`
Prefer shipping these to CloudWatch Logs (CloudWatch agent wizard on the agent-logs page). The Systems Manager Automation runbook `AWSSupport-TroubleshootCodeDeploy` automates many checks.

## Failure patterns
| Symptom | Cause / fix |
|---|---|
| All lifecycle events skipped, `HEALTH_CONSTRAINTS` ("too many individual instances failed ... too few healthy instances") | Agent not installed or running; instance cannot reach the CodeDeploy or S3 public endpoint on port 443 (public IP with route and outbound 443, or a NAT gateway from a private subnet); service role lacks permissions; HTTP proxy not set in `:proxy_uri:`; clock skew (`InvalidSignatureException - Signature expired` in the agent log); instance low on memory or disk (lower `max_revisions` in the agent configuration); missing or inadequate instance profile (restart the instance after fixing) |
| `CommandPoller: Missing credentials - please check if this instance was started with an IAM instance profile` | No instance profile, or it lacks permissions to talk to CodeDeploy and download the revision from S3 |
| `Validation of PKCS7 signed message failed` | Agent older than 1.0.1.854 (SHA-1 only); update the agent |
| Script "failed to complete in N seconds" | Hook exceeded its `timeout`; the default lifecycle event timeout is one hour. A script that starts a long-running process must detach: `cmd > /dev/null 2> /dev/null < /dev/null &`. A bare `&` can leave the deployment pending up to the one-hour timeout |
| Failure in `ApplicationStop`, `BeforeBlockTraffic` or `AfterBlockTraffic` | These run from the **previous successful** deployment's AppSpec (all other hooks use the current one), via the `<deployment-group-id>_last_successful_install` file in `deployment-instructions`. Fix the script or create a deployment with `--ignore-application-stop-failures` |
| `The deployment failed because a specified file already exists at this location` | Files in the target folder are not in the cleanup file. Choose overwrite or retain for the deployment (`--file-exists-behavior`), or delete the files in `ApplicationStop`/`BeforeInstall`. Redeploys also fail if the deployment group ID changed (group or application deleted and recreated, different application name) |
| `DownloadBundle` fails with `UnknownError: not opened for reading` | S3 internal error (redeploy), instance profile lacks S3 access, or the bucket is in a different Region than the instances; enable wire logging (`:log_aws_wire:`) to see "access denied" |
| `AllowTraffic` fails with no error in the logs (blue/green) | Misconfigured load balancer health checks |
| `No such file or directory` on Windows | Paths over 260 characters; enable `LongPathsEnabled` (agent 1.4.0 or later) and restart the agent |

## Script hygiene
- `runas: user-name` in the hook sets the user (Amazon Linux and Ubuntu only); by default scripts run as the agent's user.
- Hook scripts get environment variables such as `LIFECYCLE_EVENT`, `DEPLOYMENT_ID`, `DEPLOYMENT_GROUP_ID` and `APPLICATION_NAME`.
- A `ValidateService` hook should actually probe the app, with retries.

## On-premises
Register instances with `aws deploy register-on-premises-instance` (IAM user or role session ARN) and tag them for deployment groups; see the on-premises instances pages for the agent configuration file.

## Verify
- [ ] `aws deploy get-deployment-instance` shows each lifecycle event Succeeded.
- [ ] Agent updates are automated; logs ship to CloudWatch; `max_revisions` set.

## Checked
2026-10-28. Confirmed on the troubleshooting-deployments, agent-operations (verify, install-ssm, cloudwatch-agent) and appspec hooks pages: log paths, failure causes and fixes above, runas behaviour, environment variable names, default one-hour timeout. Fixed: the "restart the agent after attaching the role" advice (docs say restart the instance), `ScriptTimedOut` replaced by the documented message. Removed as unconfirmed: the `AWS-ConfigureAWSPackage` command line, the `codedeploy-commands-secure` VPC endpoint name, Windows log path, `DEPLOYMENT_GROUP_NAME`, root-by-default, the `:max_revisions:` file path, on-premises config file path.
Method: documentation only; no commands were run.
