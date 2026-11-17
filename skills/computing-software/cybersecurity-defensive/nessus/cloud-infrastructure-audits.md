---
id: computing-software.cybersecurity-defensive.nessus.cloud-infrastructure-audits
name: cloud-infrastructure-audits
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, cloud-infrastructure-audit, compliance-audit, cis-benchmarks, aws, azure, gcp, scan-configuration]
level: practitioner
status: draft
description: "Run Nessus/Tenable cloud infrastructure audits against AWS, Azure and GCP configuration using cloud audit files and credentials, and interpret pass/fail results."
sources: ["https://docs.tenable.com/nessus/Content/CloudServices.htm", "https://docs.tenable.com/nessus/Content/ScanAndPolicyTemplates.htm", "https://www.tenable.com/audits"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cloud infrastructure audits with Nessus

The Audit Cloud Infrastructure scan template checks cloud provider configuration against CIS
Foundations Benchmarks via provider APIs. It audits accounts/subscriptions/projects, not hosts.

## Credentials (Cloud Services)
- **AWS**: IAM user access key or role with `SecurityAudit` managed policy (read-only); select
  regions to audit. Use a dedicated audit principal per account.
- **Azure**: app registration (tenant ID, client ID, secret) with Reader (and Security Reader) on
  subscriptions.
- **GCP**: service account JSON key with Viewer / Security Reviewer roles.
- **Microsoft 365, Salesforce, Rackspace** also supported in the same credential type.

## Configure
1. New scan > Audit Cloud Infrastructure; target can be `localhost`-like placeholder (target is the
   API).
2. Credentials > Cloud Services > provider credentials.
3. Compliance > choose audit files, e.g. "CIS Amazon Web Services Foundations L1", "CIS Microsoft
   Azure Foundations L1/L2".
4. Run; results appear as compliance checks (PASSED/FAILED/WARNING) with remediation text.

## Interpreting
- WARNING means manual verification needed (the check cannot be automated).
- Map FAILED checks to owners by account; prioritise identity (root MFA, access keys age),
  logging (CloudTrail all regions), and public exposure (S3 public access block, open security groups).
- For continuous posture use a CSPM (Tenable Cloud Security, Defender for Cloud, Security Hub);
  Nessus audits are point-in-time snapshots useful for audits and smaller estates.

## Gotchas
- API rate limits on large accounts make scans slow; limit regions to those in use.
- Secrets in scan credentials: restrict who can edit the scan; rotate keys.
- Audit file versions lag new benchmark releases; note benchmark version in reports.

## Verify
Intentionally misconfigure a sandbox account (e.g. disable a CloudTrail trail); the next audit
reports the matching FAILED check.
