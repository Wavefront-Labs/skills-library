---
id: computing-software.cloud-infrastructure-engineering.aws.security-hub-asff-batch-import-findings
name: security-hub-asff-batch-import-findings
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-hub, batch-import-findings, asff, findings-integration]
level: advanced
status: docs-checked
description: "Send custom findings into Security Hub with BatchImportFindings in ASFF: required fields, product ARN, batch limits and BatchUpdateFindings."
sources: ["https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html", "https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_BatchImportFindings.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/finding-update-batchimportfindings.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Security Hub ASFF and BatchImportFindings

## 1. Minimal custom finding
```json
[{"SchemaVersion":"2018-10-08",
  "Id":"scanner/i-0abc/open-port-23",
  "ProductArn":"arn:aws:securityhub:<REGION>:<ACCOUNT_ID>:product/<ACCOUNT_ID>/default",
  "GeneratorId":"port-scanner",
  "AwsAccountId":"<ACCOUNT_ID>",
  "Types":["Software and Configuration Checks/Vulnerabilities"],
  "CreatedAt":"2026-10-18T09:00:00Z","UpdatedAt":"2026-10-18T09:00:00Z",
  "Severity":{"Label":"HIGH"},
  "Title":"Telnet open","Description":"Port 23 reachable from 0.0.0.0/0",
  "Resources":[{"Type":"AwsEc2Instance","Id":"arn:aws:ec2:<REGION>:<ACCOUNT_ID>:instance/i-0abc"}]}]
```
```bash
aws securityhub batch-import-findings --findings file://findings.json
```
With the default product ARN, the account calling `BatchImportFindings` must be the same account as `AwsAccountId` in the finding.

## 2. Limits and errors
- Up to 100 findings per call, each up to 240 KB (larger findings return an error).
- The response reports `FailedCount` and `FailedFindings`.

## 3. Updating
- `RecordState` is `ACTIVE` or `ARCHIVED`; set `ARCHIVED` when the issue is gone.
- Customers, SIEMs, ticketing and SOAR tools use `BatchUpdateFindings` for investigation updates
  (workflow status `NEW`, `NOTIFIED`, `RESOLVED` or `SUPPRESSED`, notes); finding providers use `BatchImportFindings`.
```bash
aws securityhub batch-update-findings --finding-identifiers Id=scanner/i-0abc/open-port-23,ProductArn=<ARN> \
  --workflow Status=RESOLVED --note Text="closed SG rule",UpdatedBy=secops
```

## Verify
- [ ] `aws securityhub get-findings --filters '{"GeneratorId":[{"Value":"port-scanner","Comparison":"EQUALS"}]}'` returns the finding.

## Checked

2026-10-28. Confirmed against AWS documentation: 100 findings per request, 240 KB limit, FailedCount/FailedFindings response, default-product-ARN account match, BatchUpdateFindings vs BatchImportFindings roles; RecordState and WorkflowStatus enums via the botocore securityhub model.
Removed: enable-import-findings-for-product requirement, same-Id re-import and UpdatedAt rule, HTTP 200 claim, per-Region and member-account gotchas, built-in product ARN claim.
Method: documentation only; no commands were run.
