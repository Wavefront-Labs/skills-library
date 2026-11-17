---
id: computing-software.cloud-infrastructure-engineering.aws.datasync-task-failure-and-performance-troubleshooting
name: datasync-task-failure-and-performance-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, datasync, datasync-troubleshooting, agent-offline, task-execution-errors, transfer-performance, verification-errors]
level: practitioner
status: docs-checked
description: "Fix AWS DataSync problems: agent offline/activation, location access errors, task execution phase failures, verification mismatches, and slow transfers."
sources: ["https://docs.aws.amazon.com/datasync/latest/userguide/troubleshooting-datasync.html", "https://docs.aws.amazon.com/datasync/latest/userguide/working-with-task-executions.html", "https://docs.aws.amazon.com/datasync/latest/userguide/choosing-task-mode.html", "https://docs.aws.amazon.com/datasync/latest/userguide/agent-requirements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DataSync task failure and performance troubleshooting

## 1. Execution phases
`QUEUED` then `LAUNCHING`, `PREPARING` (listing and comparing source and destination),
`TRANSFERRING`, `VERIFYING`, `SUCCESS`/`ERROR`. Know which phase failed:
```bash
aws datasync describe-task-execution --task-execution-arn <arn> \
  --query '{s:Status,res:Result,files:FilesTransferred,bytes:BytesTransferred}'
```
`Result.ErrorCode`/`ErrorDetail` and per-phase status (`PrepareStatus`,
`TransferStatus`, `VerifyStatus`) narrow it down. Enable task logging to CloudWatch Logs
(`--cloud-watch-log-group-arn`, log level `TRANSFER` for per-file detail) and task reports
to S3 for a per-file success/failure manifest.

## 2. Agent problems
- Agent offline or activation failing: check the agent VM is powered on, has network
  connectivity to the DataSync service endpoint (or your VPC endpoint), and run the network
  connectivity test on the agent console. Network ports and key-expiry rules are in the
  agent requirements and network requirements pages (not re-checked here).
- Agents are for on-premises and other-cloud NFS, SMB, HDFS and object storage. For
  transfers to or from S3 no agent is required when the other side is cloud object storage
  or Azure Blob (see the task-mode page).
- Agent VM sizing (Basic mode): four virtual processors, 32 GB RAM for up to 20 million
  files/objects/directories and 64 GB above that; Enhanced-mode agents need eight virtual
  processors; 80 GB disk. Check the agent-requirements page for the current table.

## 3. Location and permission errors
Read the task execution `Result.ErrorCode` / `ErrorDetail` and the CloudWatch task log,
then check the matching side: the NFS export or SMB share permissions for the agent, the
location's IAM role (bucket, object and KMS permissions) and bucket policy for S3, and
security groups on EFS/FSx. For source files that change during the run, schedule the
task in a quiet period or rerun. See the DataSync troubleshooting page for the specific
error strings.

## 4. Verification mismatches
`VERIFYING` errors list files whose checksum/metadata differ at the destination: files
modified during the run, or destination changed by another writer. Per the task-mode
page, Basic mode verifies all data by default and Enhanced mode verifies only transferred
data. Set `--options VerifyMode=ONLY_FILES_TRANSFERRED` (faster) or
`POINT_IN_TIME_CONSISTENT` (full check) for final cutover; `NONE` skips verification.

## 5. Slow transfers
- Check bottleneck: agent CPU/memory (see sizing in section 2), source
  storage performance, network bandwidth.
- Check the task's `BytesPerSecond` option is not throttling the transfer.
- Many small files are dominated by the PREPARING phase (listing millions of files). Use
  **Enhanced mode** tasks (S3-to-S3 and other supported locations; higher file count
  limits and parallel listing), filters (`--includes`/`--excludes`) or split by top-level
  directory across multiple tasks/agents.
- Split very large datasets across several tasks running concurrently. A task execution
  queues (`QUEUED`) while another execution using the same agent is in progress.
- `TransferMode=CHANGED` skips unchanged files on incremental runs.

## Verify
- [ ] Agent `ONLINE`; location connectivity test passes.
- [ ] Execution reaches SUCCESS; task report shows zero failed files.
- [ ] Throughput metrics (`BytesTransferred` per minute in CloudWatch) meet the migration schedule.

## Checked

2026-10-28. Confirmed against the DataSync task-mode, agent-requirements, create-task and task-executions pages and the datasync botocore model: execution statuses (QUEUED, LAUNCHING, PREPARING, TRANSFERRING, VERIFYING, SUCCESS, ERROR), Result.PrepareStatus/TransferStatus/VerifyStatus/ErrorCode/ErrorDetail, VerifyMode example values, QUEUED meaning, Basic vs Enhanced verification and agent sizing. Removed (unconfirmed, the troubleshooting-task-execution page is unreadable): endpoint hostname pattern, port numbers, 30-minute activation key expiry, SMB status codes, Backup Operators advice, the error-string table, BytesPerSecond=-1 and multi-agent claims. Read end to end.

Method: documentation only; no commands were run.
