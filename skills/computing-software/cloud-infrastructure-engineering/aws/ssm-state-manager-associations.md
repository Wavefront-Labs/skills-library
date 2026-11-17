---
id: computing-software.cloud-infrastructure-engineering.aws.ssm-state-manager-associations
name: ssm-state-manager-associations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, systems-manager, ssm, state-manager, state-manager-association, desired-state, association-compliance]
level: practitioner
status: docs-checked
description: "Keep instances in a desired state with SSM State Manager associations: schedules, targets that pick up new instances, rate control, compliance reporting and association versions."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/state-manager-about.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/reference-cron-and-rate-expressions.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-compliance-about.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSM State Manager associations

**Goal:** a document is applied to every matching managed node on a schedule, with compliance reported centrally.

## Create
```bash
aws ssm create-association --association-name keep-agent-current \
  --name AWS-UpdateSSMAgent --targets Key=tag:Env,Values=prod \
  --schedule-expression "rate(14 days)" \
  --max-concurrency 20% --max-errors 5% \
  --compliance-severity HIGH \
  --output-location 'S3Location={OutputS3BucketName=ops-ssm-out,OutputS3KeyPrefix=assoc/}'
```
`AWS-ConfigureAWSPackage` installs Distributor packages; browse the SSM document list for other
AWS-owned documents, or use your own.

## Scheduling
- Use a `rate(...)` or `cron(...)` expression; State Manager needs an interval of at least 30 minutes,
  so shorter rate or cron intervals are rejected. Rate units are singular for 1 and plural above 1
  (`rate(1 hour)`, `rate(5 hours)`).
- By default an association runs **immediately when created**, then on schedule. Add
  `--apply-only-at-cron-interval` to skip the immediate run and run only at the next cron interval.
- `aws ssm start-associations-once --association-ids "$ID"` runs it now.
- `--schedule-offset` applies to cron expressions only: the number of days to wait after the cron date
  (the API accepts 1 to 6).

## Compliance and status
```bash
aws ssm describe-association-executions --association-id "$ID"
aws ssm list-compliance-items --resource-ids i-0abc --resource-types ManagedInstance \
  --filters Key=ComplianceType,Values=Association
```
- Systems Manager Compliance reports State Manager association status alongside patch and custom compliance.
- `--compliance-severity` accepts `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` or `UNSPECIFIED`; `--sync-compliance` accepts `AUTO` or `MANUAL`.

## Versions
You can create multiple versions of an association (see "Editing and creating a new version of an
association" in the guide). Pin the document version with `--document-version` so that a new default
document version does not silently change the association, which follows `$DEFAULT` when created with it.

## Gotchas
- Targets can be tags, node IDs or Resource Groups; tag new nodes so they match the association.
- Use `--max-concurrency` and `--max-errors` so a broken document does not hit the whole fleet at once.

## Verify
- [ ] Association status `Success` on all targets; a newly tagged node picks the association up.
- [ ] Compliance dashboard shows the association with no non-compliant resources.

## Checked
2026-10-28: Confirmed against the Systems Manager User Guide pages state-manager-about, systems-manager-state, reference-cron-and-rate-expressions and sysman-compliance-about, and the botocore ssm CreateAssociation model: immediate run on create by default, ApplyOnlyAtCronInterval, 30-minute minimum interval, rate unit grammar, schedule offsets for cron only (1 to 6 in the API), tag/node ID/Resource Group targets, association versions and $DEFAULT, compliance reporting of associations, ComplianceSeverity and SyncCompliance enums, MaxConcurrency/MaxErrors. All commands passed check_commands.py. Read end to end. Removed as unconfirmed: the list of other AWS-owned documents, "runs when a new instance matches", calendar-names behaviour, the Config rule name, PutComplianceItems claim, update-association/list-association-versions description, and Quick Setup/StackSets advice.

Method: documentation only; no commands were run.
