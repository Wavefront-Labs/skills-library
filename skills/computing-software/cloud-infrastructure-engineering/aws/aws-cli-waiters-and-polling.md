---
id: computing-software.cloud-infrastructure-engineering.aws.aws-cli-waiters-and-polling
name: aws-cli-waiters-and-polling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-cli, waiters, wait-command, polling, sdk, automation, boto3]
level: practitioner
status: docs-checked
description: "Use AWS CLI and SDK waiters instead of sleep loops: wait commands, polling intervals and timeouts, exit codes, custom boto3 waiter config, and bounded pollers."
sources: ["https://docs.aws.amazon.com/cli/latest/reference/wait/index.html", "https://github.com/aws/aws-cli/blob/v2/awscli/customizations/waiters.py", "https://github.com/aws/aws-cli/blob/v2/awscli/topics/return-codes.rst", "https://github.com/boto/botocore/blob/develop/botocore/waiter.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS CLI and SDK waiters

## 1. CLI wait commands
```bash
aws ec2 run-instances ... --query 'Instances[0].InstanceId' --output text > id
aws ec2 wait instance-status-ok --instance-ids $(cat id)
aws cloudformation wait stack-create-complete --stack-name app
aws rds wait db-instance-available --db-instance-identifier orders
aws lambda wait function-updated-v2 --function-name api
aws ecs wait services-stable --cluster prod --services web
aws s3api wait object-exists --bucket b --key out/result.json
```
`aws <service> wait help` lists the waiters for a service.
- Each waiter has a fixed delay and max attempts in its service model, e.g. `ec2 wait instance-running` polls every
  15 s up to 40 times (10 min); `cloudformation wait stack-create-complete` every 30 s up to
  120 times (60 min); `lambda wait function-updated-v2` every 1 s up to 300 times; `s3api wait object-exists` every 5 s up to 20 times. Check the reference page for each.
- When the maximum number of attempts is reached or a waiter hits a terminal failure state (for `stack-create-complete`, `CREATE_FAILED`, `ROLLBACK_COMPLETE` and similar), the CLI exits with return code **255** (the general error code). Use `set -e` or check `$?` in scripts.

## 2. boto3 waiters with custom timing
```python
ec2 = boto3.client("ec2")
ec2.get_waiter("instance_running").wait(
    InstanceIds=[iid], WaiterConfig={"Delay": 5, "MaxAttempts": 60})
cfn.get_waiter("stack_update_complete").wait(StackName="app",
    WaiterConfig={"Delay": 20, "MaxAttempts": 180})
```
`botocore.exceptions.WaiterError` carries `last_response` — log it for the failure reason. Other SDKs have their own waiter APIs; check their documentation.

## 3. No waiter? Write a bounded poller
```bash
for i in $(seq 1 60); do
  s=$(aws glue get-job-run --job-name etl --run-id "$RUN" --query JobRun.JobRunState --output text)
  case "$s" in SUCCEEDED) exit 0;; FAILED|ERROR|TIMEOUT|STOPPED|EXPIRED) echo "$s"; exit 1;; esac
  sleep 30
done; echo "timed out"; exit 1
```
Always bound attempts, treat terminal failure states explicitly, back off for slow operations.

## Gotchas
- `instance-running` and `instance-status-ok` are different waiters; the second waits for passing status checks, so prefer it before connecting to the instance.
- Wait for `lambda wait function-updated-v2` before a second `update-function-*` call so the first update has finished.
- Waiters make repeated API calls; many parallel waiters can add to throttling.

## Verify
- [ ] Deployment scripts contain no unbounded `sleep` loops; each wait has a timeout and failure handling.
- [ ] A forced failure (e.g. stack rollback) makes the script exit non-zero quickly, not after the full timeout.

## Checked
Date: 2026-10-24. Sources: aws-cli v2 branch (waiters.py, return-codes topic), botocore develop branch (waiter.py, waiters-2.json for ec2, cloudformation, lambda, ecs, rds, s3, and the Glue service model).
Confirmed: waiter delay and max attempts for the named waiters, exit code 255 on timeout or terminal failure, existence of lambda FunctionUpdatedV2, ecs ServicesStable, rds DBInstanceAvailable and s3 ObjectExists waiters, boto3 WaiterConfig keys Delay and MaxAttempts, WaiterError.last_response, Glue JobRunState values.
Removed as unconfirmed: JavaScript and Go waiter call examples.
Method: documentation only; no commands were run.
