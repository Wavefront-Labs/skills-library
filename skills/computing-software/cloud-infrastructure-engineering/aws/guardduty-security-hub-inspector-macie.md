---
id: computing-software.cloud-infrastructure-engineering.aws.guardduty-security-hub-inspector-macie
name: guardduty-security-hub-inspector-macie
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, guardduty, security-hub, inspector, inspector-v2, macie, detective, security-services, threat-detection, findings, asff, security-standards, fsbp, cis-benchmark, delegated-administrator, auto-enable, suppression-rules, automation-rules, finding-aggregation, vulnerability-scanning, sensitive-data-discovery, eventbridge, cloud-security-posture, guardduty-protection-plans, malware-protection, runtime-monitoring]
level: practitioner
status: draft
description: "Enable and tune AWS security services org-wide: GuardDuty sources, Security Hub standards and automation, Inspector, Macie and Detective, with cost levers and finding routing."
sources: ["Amazon GuardDuty User Guide - Managing multiple accounts and protection plans", "AWS Security Hub User Guide - Security standards, cross-Region aggregation and automation rules", "Amazon Inspector User Guide - Scanning Amazon EC2, ECR and Lambda", "Amazon Macie User Guide - Automated sensitive data discovery", "Amazon Detective Administration Guide", "AWS Security Hub User Guide - AWS Security Finding Format (ASFF)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GuardDuty, Security Hub, Inspector, Macie, Detective — the detective layer, org-wide

**Goal:** every account in the organisation is covered automatically the moment it is
created, findings land in one place with one severity scale, noise is suppressed by
rule rather than by habit, and the monthly bill is predictable. Preventive controls
(SCPs, Control Tower) are in `...aws.organizations-and-control-tower`; audit logging is
in `...aws.cloudtrail-and-config-audit`.

## 1. Delegate once, auto-enable forever
From the management account, for each service:
```
aws organizations enable-aws-service-access --service-principal guardduty.amazonaws.com
aws guardduty enable-organization-admin-account --admin-account-id <AUDIT_ACCT>
```
then in the Audit account, per region:
```
aws guardduty update-organization-configuration --detector-id <ID> --auto-enable-organization-members ALL
```
Security Hub, Inspector, Macie and Detective have the same shape
(`securityhub enable-organization-admin-account`, `inspector2 enable-delegated-admin-account`,
`macie2 enable-organization-admin-account`, `detective ... `). Do it in **every region
you govern** — these are regional services; an un-enabled region is a blind spot, and
Security Hub's cross-region aggregation only aggregates regions where it is on.
`ALL` vs `NEW`: `ALL` also back-fills existing member accounts; prefer it.

## 2. GuardDuty
- Foundational sources need no configuration: CloudTrail management events, VPC Flow
  Logs and Route 53 DNS logs (GuardDuty reads them internally — you do not need Flow
  Logs enabled yourself, and the bill is by analysed volume, not by your log storage).
- **Protection plans** are separate toggles with separate pricing: S3 Protection (data
  events), EKS Protection (audit logs), **Runtime Monitoring** (EKS/ECS/EC2 agent, the
  one that catches actual execution), Malware Protection for EC2 (snapshot scan on
  finding) and for S3 (scan on upload), RDS Protection (login activity), Lambda
  Protection (network activity). Enable S3 and Runtime first; Malware Protection for S3
  is per-bucket and billed per GB scanned.
- Noise control: **suppression rules** (filter + auto-archive, e.g.
  `Recon:EC2/PortProbeUnprotectedPort` from a known scanner CIDR), a **trusted IP list**
  (one per account, public IPs only) and **threat intel lists**. Suppressed findings
  still exist (archived) and still reach Security Hub unless filtered there too.
- Export findings to S3 (`create-publishing-destination`) with a KMS key for retention
  beyond the 90-day console window.
- Cost drivers: CloudTrail event volume (CI pipelines, Terraform plans) and Flow Log
  GB. The first 30 days are free per account per region — use that to read the
  **usage statistics** (`get-usage-statistics --usage-statistic-type SUM_BY_DATA_SOURCE`)
  before deciding on protection plans.

## 3. Security Hub
- Set an **aggregation region** (`create-finding-aggregator --region-linking-mode ALL_REGIONS`)
  so one console shows everything.
- Standards: **AWS Foundational Security Best Practices** always; **CIS AWS Foundations
  Benchmark v3.0** if you report against it; PCI DSS / NIST 800-53 only when audited
  against them. Each enabled standard runs its own Config-backed checks and is billed
  per check per account per month (first 10,000 checks free), so three standards
  roughly triple the bill — use **consolidated controls** (central configuration) to
  dedupe controls shared between standards.
- Disable controls that do not apply with a documented reason
  (`update-standards-control --control-status DISABLED --disabled-reason "..."`), e.g.
  `EC2.8` IMDSv2 on accounts with no EC2, or `CloudTrail.5` where the org trail lives
  elsewhere. Central configuration from the delegated admin pushes these to all accounts.
- **Automation rules** rewrite findings on arrival: raise severity for prod account
  ids, suppress a known-accepted finding by `ResourceId`, add `UserDefinedFields`.
  Order matters (`RuleOrder`), lowest first.
- Route findings: EventBridge rule on `source: aws.securityhub`,
  `detail-type: Security Hub Findings - Imported` filtered by `Severity.Label` ∈
  {CRITICAL, HIGH} and `Workflow.Status: NEW` → SNS/ChatOps/ticketing. Set
  `Workflow.Status` to `NOTIFIED`/`SUPPRESSED`/`RESOLVED` via `batch-update-findings`
  so the same finding does not page twice.
- Everything arrives as **ASFF** JSON; third-party scanners can `batch-import-findings`
  into the same stream.

## 4. Inspector (v2)
- Enable per resource type: `inspector2 enable --resource-types EC2 ECR LAMBDA LAMBDA_CODE`.
  EC2 scanning uses the SSM agent (agent-based) or **agentless** snapshot scanning —
  agentless covers instances without SSM but adds EBS snapshot churn; hybrid mode
  (default) uses both.
- ECR: continuous rescan of pushed images (configurable duration: lifetime, 180 days,
  30 days, 14 days, or on push only). Pull-through and tag-immutable repos still scan.
- Findings are CVE-based with an **Inspector score** that adjusts CVSS for your context
  (e.g. no network path lowers it) — sort by that, not raw CVSS. Export SBOMs
  (`create-sbom-export`, CycloneDX/SPDX) when a customer asks.
- Billed per instance-month / per image scanned / per Lambda-month; prune ECR with
  lifecycle policies or you scan every old tag forever.

## 5. Macie and Detective
- **Macie**: enable org-wide, then turn on **automated sensitive data discovery** —
  it samples objects across all buckets continuously for a flat per-GB-sampled rate
  rather than a full classification job. Run a targeted **classification job** on a
  bucket only when you must inventory it (billed per GB). Macie's bucket inventory
  (public, unencrypted, shared externally) is free and is worth enabling for that alone.
  Custom data identifiers (regex + keywords) catch internal id formats.
- **Detective** builds a behaviour graph from CloudTrail, Flow Logs, GuardDuty and EKS
  audit logs; use it from a GuardDuty finding ("Investigate with Detective") to see what
  else the principal touched. It needs 48 hours of data before it is useful and bills on
  ingested volume — enable it before the incident, not during.

## Gotchas
- GuardDuty in a region you never use still finds things (credentials used from there);
  enable it everywhere, and pair with an SCP region deny for the rest.
- Security Hub's "Config.1 — Config should be enabled" needs the recorder on **in every
  region**; Control Tower does this for governed regions only.
- Suspending a member account does not stop its findings; disassociate it from the
  delegated admin first or the empty account keeps costing checks.
- Inspector EC2 findings for stopped instances linger until the instance is terminated.
- Macie classification jobs on large buckets can cost thousands of dollars — set a
  sampling depth and object-size filter, and estimate with the job's cost preview.
- Findings older than 90 days (GuardDuty) or with `RecordState: ARCHIVED` (Security
  Hub) vanish from the console; export if you need evidence for audits.

## Verify
- [ ] Each service shows the Audit account as delegated admin and `AutoEnable: ALL` in every governed region.
- [ ] A new member account appears in GuardDuty/Security Hub/Inspector within an hour of creation without manual steps.
- [ ] GuardDuty sample findings (`create-sample-findings`) arrive in Security Hub and trigger the EventBridge → notification path for HIGH/CRITICAL.
- [ ] Security Hub FSBP score is tracked per account and improving; every disabled control has a written reason.
- [ ] Monthly cost per service per account is reviewed against GuardDuty usage statistics and Security Hub check counts.
