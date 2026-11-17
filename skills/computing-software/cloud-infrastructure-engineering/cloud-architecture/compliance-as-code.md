---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.compliance-as-code
name: compliance-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, compliance-as-code, policy-as-code, opa, azure-policy, aws-config-rules, conftest, architecture-conformance-automation]
level: practitioner
status: draft
description: "Turn architecture standards into automated checks: policy-as-code in CI (OPA/Conftest, Checkov) and at runtime (Azure Policy, AWS Config, Org Policy) with reporting."
sources: ["https://www.openpolicyagent.org/docs/latest/", "https://www.conftest.dev/", "https://learn.microsoft.com/azure/governance/policy/overview", "https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated architecture compliance-as-code

## Where checks run
1. **IDE / pre-commit**: fast feedback (tflint, checkov).
2. **CI on IaC plans**: `terraform show -json plan.out | conftest test -p policy/ -`; Checkov or
   Trivy config scans; fail on violations of mandatory standards.
3. **Admission** (Kubernetes): Gatekeeper/Kyverno policies.
4. **Runtime cloud policy**: Azure Policy (deny/audit/modify/deployIfNotExists), AWS Config rules +
   conformance packs + SCPs, Google Organization Policy constraints - catches console changes.

## Turning a standard into policy
| Standard | Check |
|---|---|
| Storage not public | Deny public access settings; Config rule s3-bucket-public-read-prohibited |
| Approved regions only | SCP / Azure Policy allowed locations / org policy resourceLocations |
| Mandatory tags | Policy with deny or modify (inherit from resource group) |
| Encryption with CMK for confidential data | Policy audit on key source |
| Private endpoints for PaaS data stores | Deny public network access |

## Steps
1. Classify each standard: mandatory (deny), recommended (audit), informational.
2. Write the policy with tests (`opa test`), include an exemption mechanism with expiry.
3. Roll out in audit mode, measure violations, fix, then enforce.
4. Report compliance per team; feed dispensations into the governance log.

## Gotchas
- Enforcing deny before auditing breaks pipelines across the org.
- Exemptions without expiry dates accumulate.
- Same rule implemented differently in CI and runtime; generate from one source where possible.

## Verify
- [ ] Each mandatory standard has CI and runtime enforcement.
- [ ] Compliance dashboard per team, trending.
