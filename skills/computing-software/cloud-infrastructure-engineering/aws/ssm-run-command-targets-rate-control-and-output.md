---
id: computing-software.cloud-infrastructure-engineering.aws.ssm-run-command-targets-rate-control-and-output
name: ssm-run-command-targets-rate-control-and-output
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, systems-manager, ssm, run-command, send-command, rate-control, max-concurrency, command-output-s3]
level: practitioner
status: docs-checked
description: "Run fleet commands with SSM Run Command: tag targets, max-concurrency and max-errors rate control, S3 and CloudWatch output, timeouts and command statuses."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/send-commands-multiple.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/monitor-commands.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command-handle-exit-status.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSM Run Command: targets, rate control and output

## Send to a fleet safely
```bash
aws ssm send-command --document-name AWS-RunShellScript \
  --targets Key=tag:Role,Values=web Key=tag:Env,Values=prod \
  --parameters 'commands=["systemctl restart nginx","systemctl is-active nginx"],executionTimeout=["600"]' \
  --max-concurrency 10% --max-errors 1 \
  --timeout-seconds 900 \
  --output-s3-bucket-name ops-command-output --output-s3-key-prefix run/ \
  --cloud-watch-output-config CloudWatchOutputEnabled=true,CloudWatchLogGroupName=/ssm/run \
  --comment "CHG-1234 restart nginx" --query Command.CommandId --output text
```
- Targets: `tag:<key>`, `InstanceIds`, `resource-groups:Name`; up to five keys and five values per key.
- `--max-concurrency` (number or %) limits simultaneous targets; `--max-errors` sets how many errors are
  allowed before the command stops being sent; invocations already running are allowed to complete. Start with 1 host, then 10%.
- Total timeout = `--timeout-seconds` (Timeout in the console) plus the document's `executionTimeout`
  (default 3,600 s for `AWS-RunShellScript`). A command not delivered before the total timeout becomes
  Delivery Timed Out.
- Use `AWS-RunPowerShellScript` for Windows.

## Read results
```bash
aws ssm list-command-invocations --command-id "$CID" --details \
  --query 'CommandInvocations[].[InstanceId,Status,CommandPlugins[0].ResponseCode]' --output table
aws ssm get-command-invocation --command-id "$CID" --instance-id i-0abc --query StandardOutputContent
```
- Send full output to S3 (`--output-s3-bucket-name`) or CloudWatch Logs (`--cloud-watch-output-config`) when you need it kept.

## Statuses
| Status | Meaning |
|---|---|
| Pending / InProgress | not yet received by the agent / sent or running |
| Delayed | send attempt failed; the system retries |
| Success | agent received it and returned exit code 0 (does not prove the work was right) |
| Failed | a plugin returned a non-zero result code; counts against max-errors |
| DeliveryTimedOut | not delivered before the total timeout; does not count against max-errors |
| ExecutionTimedOut | not finished before the execution timeout; counts as a failure |
| Undeliverable | node does not exist or is not responding; does not count against max-errors |
| Terminated | the parent command exceeded max-errors and the rest were cancelled |
| Cancelled | cancelled before completion |
| Incomplete (command level) | all attempted, some not Success, too few failures for Failed |
| No Instances In Tag (command level) | the tag or resource group matched no managed nodes |
You can configure SNS notifications for all status changes or specific ones, and EventBridge for state or status changes.

## Gotchas
- Targets must be managed nodes with a running SSM Agent.
- By default the exit code of the last command in a script is the script's exit code; make a shell script
  exit non-zero on the first failure (for example `set -e` or an explicit `exit <N>` check) if every step matters.
- Avoid putting secrets in command parameters; read them from Parameter Store or Secrets Manager inside the script.

## Verify
- [ ] Canary run on one instance, then a percentage rollout with max-errors 1.
- [ ] Full output in S3 for at least one invocation; statuses all Success.

## Checked
2026-10-28: Confirmed against the Systems Manager User Guide pages send-commands-multiple, monitor-commands and run-command-handle-exit-status, and the botocore ssm SendCommand model: tag/resource-groups targets (five keys, five values), max-concurrency as number or percent, max-errors behaviour (running invocations complete), total timeout formula and the 3,600 s RunShellScript executionTimeout default, the full status list with max-errors accounting, SNS/EventBridge notification options, default exit-code behaviour. Commands passed check_commands.py. Read end to end. Error fixed: --timeout-seconds was described as the delivery timeout only (the docs define a total timeout combining it with executionTimeout), and the statuses table lacked real statuses (Delayed, Incomplete, DeliveryTimedOut accounting). Removed as unconfirmed: the 24,000-character output limit, exit codes 3010/194, 30-day history, endpoint names, instance-profile permissions and the EventBridge detail-type string.

Method: documentation only; no commands were run.
