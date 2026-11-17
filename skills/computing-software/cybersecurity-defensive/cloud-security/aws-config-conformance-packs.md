---
id: computing-software.cybersecurity-defensive.cloud-security.aws-config-conformance-packs
name: aws-config-conformance-packs
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [conformance-packs, aws-config, config-rules, organization-conformance-packs, compliance-as-code, cspm]
level: practitioner
status: docs-checked
description: "Deploy AWS Config conformance packs org-wide: sample templates (CIS, operational best practices), custom rules, remediation actions, aggregator reporting and cost control."
sources: ["https://docs.aws.amazon.com/config/latest/developerguide/conformance-packs.html", "https://docs.aws.amazon.com/config/latest/developerguide/conformancepack-sample-templates.html", "https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Config conformance packs

A conformance pack is a YAML template bundling Config rules (and optional remediation actions) deployed
as one unit to an account or the whole organisation.

## Prerequisites
- AWS Config recorder on in every account and region, delivery channel to the log archive account.
- Delegated administrator for Config in the organisation.

## Deploy
```
aws configservice put-organization-conformance-pack \
  --organization-conformance-pack-name cis-aws-v3 \
  --template-s3-uri s3://<BUCKET>/<PACK_TEMPLATE>.yaml \
  --excluded-accounts 111122223333
```
Start from the AWS sample templates (the sample templates page lists Operational Best Practices packs, for example for CIS AWS Foundations Benchmark and CIS Critical Security Controls). Copy into your repo and trim/parameterise rules rather than deploying unchanged.

## Custom rules
- A pack template can contain AWS Config managed or custom rules.
- Parameters per environment (e.g. allowed instance types).

## Remediation
Remediation actions can be part of the pack template; manual first, automatic only for low-risk fixes (see cspm-auto-remediation).

## Reporting
Config aggregator in the security account: compliance by pack, account, rule.

## Cost
See the AWS Config pricing page for what is billed.

## Gotchas
- Enable Config recording before deploying a pack; monitor deployment status per account.

## Checked

2026-10-28: confirmed on the conformance packs and sample templates pages: a pack is a collection of Config managed or custom rules and remediation actions deployed as one entity to an account or organization; sample templates include CIS AWS Foundations and CIS Critical Security Controls packs. The `put-organization-conformance-pack` command and `--excluded-accounts` flag passed the botocore command check. Removed: template file name, NIST/PCI template names, Guard/Lambda rule claim, SSM document name, Control Tower note, Security Hub export, Security Hub duplication claim, cost advice, status literal CREATE_SUCCESSFUL.

Method: documentation only; no commands were run.

## Verify
- [ ] Organization pack deployment status shows success in all accounts.
- [ ] Aggregator dashboard shows compliance trend.
