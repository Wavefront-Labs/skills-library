---
id: computing-software.cloud-infrastructure-engineering.aws.dms-premigration-assessments
name: dms-premigration-assessments
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dms, premigration-assessment, task-assessment, data-type-validation]
level: advanced
status: docs-checked
description: "Run DMS premigration assessments before starting a task: choose individual assessments, read results in S3, and fix unsupported types, missing keys and source settings."
sources: ["https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.AssessmentReport.html", "https://docs.aws.amazon.com/cli/latest/reference/dms/start-replication-task-assessment-run.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMS premigration assessments

## 1. Run one
The task must already exist (the assessment run takes `--replication-task-arn`).
```bash
aws dms describe-applicable-individual-assessments --replication-task-arn <TASK_ARN> \
  --query 'IndividualAssessmentNames'
aws dms start-replication-task-assessment-run --replication-task-arn <TASK_ARN> \
  --service-access-role-arn arn:aws:iam::<ACCOUNT_ID>:role/dms-assessments \
  --result-location-bucket dms-assessments-<ACCOUNT_ID> --result-location-folder orders/ \
  --assessment-run-name orders-pre-1
aws dms describe-replication-task-assessment-runs --filters Name=replication-task-arn,Values=<TASK_ARN>
aws dms describe-replication-task-individual-assessments --filters Name=replication-task-assessment-run-arn,Values=<RUN_ARN>
```
The service access role must allow `iam:PassRole` and let DMS write results to the result bucket (`--result-location-bucket` and `--service-access-role-arn` are required; the folder is optional).

## 2. What it catches
Each individual assessment evaluates one element of a supported source and/or target from the
perspective of the migration type, supported objects and similar criteria; for example which
source data types or primary key formats can or cannot be migrated, possibly depending on the DMS
engine version. The list of available assessments grows over time: use
`describe-applicable-individual-assessments` for your task. A premigration assessment run already
includes data type results, so no separate (legacy) data type assessment is needed.

## 3. Act on results
The run status is `passed` (no individual assessment failed), `warning` (at least one warning, or all
were skipped) or `failed` (at least one failed); internal problems show as `error-provisioning`,
`error-executing` or `invalid state`. Results are stored in the S3 bucket you chose. Fix what
the failed assessments report, re-run, then start the task.

## Verify
- [ ] Final assessment run has no `failed` items and warnings are accepted in writing.

## Checked

2026-10-28. Confirmed against the DMS premigration assessment page and the start-replication-task-assessment-run CLI reference: required flags, result bucket and folder, run status values (passed, warning, failed, error-provisioning, error-executing, invalid state), iam:PassRole requirement, data type assessments included in a run, assessment list growing over time. Removed (unconfirmed): task-state precondition, the exact S3 permission list, the itemised list of what is checked. Read end to end.

Method: documentation only; no commands were run.
