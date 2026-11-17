---
id: computing-software.cloud-infrastructure-engineering.aws.snowball-availability-changes-and-data-transfer-alternatives
name: snowball-availability-changes-and-data-transfer-alternatives
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, snow-family, snowball-alternatives, data-transfer-terminal, datasync, offline-data-transfer, large-data-migration]
level: practitioner
status: docs-checked
description: "Move large datasets to AWS now that Snow device options are shrinking: transfer time maths, DataSync over Direct Connect, AWS Data Transfer Terminal sites, and partner devices."
sources: ["https://aws.amazon.com/snowball/", "https://docs.aws.amazon.com/datasync/latest/userguide/configure-bandwidth.html", "https://docs.aws.amazon.com/datasync/latest/userguide/configure-data-verification-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowball availability changes and data transfer alternatives

## Status
AWS's Snowball page carries an end-of-support notice: on 31 December 2026 AWS discontinues support for AWS Snowball
devices (Snowball Edge Storage Optimized and Compute Optimized) in all AWS commercial Regions, and after that date the
AWS Snow Console and Snowball resources are no longer accessible. The notice says GovCloud and ADC Region customers
with active Snow jobs are not affected. Plan any new project around an online or other transfer method, and re-read
the notice before relying on a device.

## Transfer time maths
`days = TB x 8,000,000 Mb / (Mbps x utilisation x 86,400)` (decimal TB)
| Data | 1 Gbps at 80% | 10 Gbps at 80% |
|---|---|---|
| 10 TB | ~1.2 days | ~3 hours |
| 100 TB | ~11.6 days | ~1.2 days |
| 1 PB | ~116 days | ~11.6 days |

## Online option: DataSync
Use the DataSync User Guide to size and run the transfer.
- Bandwidth limits can be set on a task and on each of its executions: when creating, editing or starting a task.
- Verification (`VerifyMode`): `ONLY_FILES_TRANSFERRED` (the recommended mode) checksums the transferred data
  including metadata at the source and compares at the end; `POINT_IN_TIME_CONSISTENT` checks the entire source and
  destination and is not supported with Enhanced mode tasks; `NONE` skips verification.
- Task mode is `BASIC` or `ENHANCED`.
- Do an initial full copy, then incremental task runs until cutover.

## Gotchas
- Check encryption at rest on the target and metadata preservation before cutover.

## Verify
- [ ] Measured throughput in a pilot copy matches the plan's assumption.
- [ ] Post-copy verification report clean; object counts and sizes reconciled.

## Checked

2026-10-28. Confirmed against the AWS Snowball product page end-of-support notice (31 December 2026, commercial Regions; GovCloud/ADC exception), the DataSync User Guide pages on bandwidth limits and data verification, the botocore datasync model (VerifyMode and TaskMode enums), and the transfer-time arithmetic recomputed by hand.
Removed: "Snowcone and older models discontinued" and "restricted for new customers" wording, the Direct Connect 10/100 Gbps, Data Transfer Terminal, S3 Transfer Acceleration, Storage Gateway and partner-service rows, agent sizing and small-file advice (no readable source), and the prose-only `sources`.
Method: documentation only; no commands were run.
