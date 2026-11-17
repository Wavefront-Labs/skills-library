---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.security-governance
name: security-governance
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, security-foundations, security-governance, security-raci, risk-register, security-policy]
level: practitioner
status: draft
description: "Establish cloud security governance: accountable roles, security policy and standards, risk register and acceptance, control ownership and executive reporting."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/security.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/secure/", "https://www.nist.gov/cyberframework", "https://cloud.google.com/architecture/framework/security"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security governance and accountability

## Steps
1. **Accountability**: name a single accountable executive (CISO) and per-workload security
   owners; write a RACI across security, platform, workload and compliance teams (NIST CSF 2.0
   added the Govern function for exactly this).
2. **Policy hierarchy**: short policy (intent), standards (cloud security baseline per
   provider, mapped to CIS/NIST), procedures and guardrail code. Version and review yearly.
3. **Control ownership**: every control in the baseline has an owner and an evidence source
   (CSPM rule, config, log); controls without evidence are not controls.
4. **Risk management**: risk register with likelihood/impact, owner, treatment and expiry
   of acceptances; exceptions only with compensating controls and dates.
5. **Metrics to leadership**: critical findings open and age, CSPM compliance score, patch
   SLA attainment, MFA coverage, incidents and time to contain.
6. **Cadence**: monthly security council, quarterly board-level report, annual policy review.

## Gotchas
- Security owning all risk decisions removes business accountability; risk owners accept risk.
- Policies written but not enforced in guardrails are aspirational.

## Verify
- [ ] RACI and control ownership published.
- [ ] Risk acceptances all have owner and expiry.
