---
id: computing-software.cybersecurity-defensive.cloud-security.iam-access-analyzer
name: iam-access-analyzer
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, iam-access-analyzer, external-access-findings, unused-access, policy-generation, policy-validation]
level: advanced
status: docs-checked
description: "Use AWS IAM Access Analyzer to find external and unused access, generate least-privilege policies from CloudTrail activity and validate policies with custom checks."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-create-unused.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-custom-policy-checks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM Access Analyzer

**Goal:** know which resources are shared outside your trust zone, which permissions are unused, and stop over-broad policies before deployment.

## Analyzers
- **External access analyzer** with zone of trust = organisation: `aws accessanalyzer create-analyzer --analyzer-name org-external --type ORGANIZATION` from the delegated admin account. Resource types analysed include S3 buckets and directory buckets, IAM roles, KMS keys, Lambda functions and layers, SQS queues, Secrets Manager secrets, SNS topics, EBS snapshots, RDS DB and cluster snapshots, ECR repositories, EFS file systems, and DynamoDB streams and tables.
- **Unused access analyzer** (`--type ORGANIZATION_UNUSED_ACCESS`, or `ACCOUNT_UNUSED_ACCESS`; charged per IAM role and user analyzed per analyzer per month): findings for unused roles, access keys and passwords, and unused services and actions of active roles. Set a tracking period of 1 to 365 days; only permissions that existed for the whole period are evaluated. Findings do not vary by Region, so one analyzer per account or organisation is enough, and extra Regions are charged separately.
- **Internal access analyzer** (`ACCOUNT_INTERNAL_ACCESS` / `ORGANIZATION_INTERNAL_ACCESS`) identifies internal access to selected business-critical resources.
- Findings from the three analyzer types appear in a summary dashboard.

## Triage findings
For each external finding: intended (partner account, public website bucket) -> archive with an archive rule (`aws accessanalyzer create-archive-rule`); unintended -> fix the resource policy.

## Least-privilege policy generation
`aws accessanalyzer start-policy-generation --policy-generation-details principalArn=arn:aws:iam::111122223333:role/app --cloud-trail-details file://trail.json` generates a policy from CloudTrail activity over a range of up to 90 days; the docs recommend the shortest period that covers the workload to reduce generation time. Review the output before replacing the broad policy; standard S3 rates apply for reading your CloudTrail logs.

## Policy validation in CI
- `aws accessanalyzer validate-policy --policy-document file://p.json --policy-type IDENTITY_POLICY` returns errors (policy will not work), warnings (best-practice issues that are not security risks) and suggestions (no permission impact). Policy types are `IDENTITY_POLICY`, `RESOURCE_POLICY`, `SERVICE_CONTROL_POLICY` and `RESOURCE_CONTROL_POLICY`.
- Custom policy checks (each check is charged): `check-no-new-access` (compare an updated policy to the existing one), `check-access-not-granted` (confirm specified access, for example `iam:PassRole`, is not allowed), and `check-no-public-access` (whether a resource policy can grant public access to a resource type). Equivalent API operations are `CheckNoNewAccess`, `CheckAccessNotGranted` and `CheckNoPublicAccess`.

## Verify
- [ ] Analyzer active in each Region where you have resources (external and internal) and at organisation scope.
- [ ] Active external findings are either archived with justification or fixed within SLA.
- [ ] CI pipeline fails a test change that adds `"Action":"*"`.

## Checked
Checked 2026-11-09 against the IAM User Guide pages in `sources` and the botocore Access Analyzer model (analyzer `Type` and `PolicyType` enums; commands via the command checker). Removed unconfirmed claims: Security Hub/EventBridge routing, `cfn-policy-validator` and `tf-policy-validator`, the "newer" label on internal analyzers, and the Security Reference Architecture source.
Method: documentation only; no commands were run.
