---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.secure-by-default
name: secure-by-default
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, security-foundations, secure-by-default, paved-road, guardrails, golden-paths]
level: practitioner
status: draft
description: "Make the secure path the default for developers: hardened IaC modules and templates, preventive policies, safe defaults in platforms, and fast exception paths."
sources: ["https://www.cisa.gov/securebydesign", "https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/secure/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure-by-default guardrails for developers

## Steps
1. **Paved-road modules**: IaC modules and templates with encryption, private networking,
   logging, least-privilege roles and tags built in; teams get security by using them.
2. **Preventive guardrails** at the organisation level: deny public storage, unencrypted
   volumes, public IPs outside approved accounts, disabled logging (SCPs, Azure Policy deny,
   org policy constraints).
3. **Account/environment defaults**: block public access settings on, default EBS/disk
   encryption on, IMDSv2 required, default security groups emptied.
4. **Shift-left checks**: IaC scanning in CI (Checkov, tfsec/Trivy, cfn-guard) with the same
   rules as runtime policy; fail on high severity.
5. **Secure pipeline defaults**: OIDC workload identity instead of long-lived keys, signed
   artefacts, secret scanning.
6. **Exceptions**: fast, documented and time-boxed; frequent exceptions signal a bad default.
7. **Measure**: percent of resources from paved-road modules, policy denials per week, time
   to remediate.

## Gotchas
- Guardrails that block without explanation create workarounds; return clear error messages.
- Different rules in CI and runtime confuse teams; share one rule set.

## Verify
- [ ] Organisation-level deny policies active for the core baseline.
- [ ] CI scanning uses the same rules as runtime policy.
