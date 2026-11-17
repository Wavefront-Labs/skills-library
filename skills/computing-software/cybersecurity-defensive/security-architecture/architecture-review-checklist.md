---
id: computing-software.cybersecurity-defensive.security-architecture.architecture-review-checklist
name: architecture-review-checklist
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [architecture-review-checklist, security-architecture-review, design-review, nfr-security, review-gate, threat-model-input]
level: practitioner
status: draft
description: "Run a security architecture review with a structured checklist: identity, data, network, secrets, logging, resilience and third parties, producing risk-rated findings."
sources: ["https://owasp.org/www-project-application-security-verification-standard/", "https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html", "https://learn.microsoft.com/en-us/azure/well-architected/security/checklist", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security architecture review checklist

Use at design gate (before build) and again before go-live. Inputs: architecture diagram with trust
boundaries, data flow, data classification, threat model if available.

## Checklist
**Identity and access**
- [ ] Users authenticate via the corporate IdP (SSO), MFA enforced, no local accounts.
- [ ] Service-to-service auth uses workload identity / mTLS, not shared static keys.
- [ ] Authorisation model documented (roles, object-level checks), admin functions separated.

**Data**
- [ ] Data classified; regulated data identified with residency requirements.
- [ ] Encryption in transit (TLS 1.2+) everywhere including internal hops; at rest with defined key ownership.
- [ ] Retention and deletion defined; non-prod uses masked data.

**Network**
- [ ] Only intended endpoints internet-facing, behind WAF/CDN where web.
- [ ] Private connectivity to PaaS; egress restricted.

**Secrets**
- [ ] Secrets in a vault, rotated, never in code/images/env files in repos.

**Logging and detection**
- [ ] Security events defined and shipped to SIEM (see security-logging-requirements).

**Resilience**
- [ ] RTO/RPO stated and backup/DR design meets them; backups immutable.

**Supply chain and third parties**
- [ ] Vendors/SaaS assessed; integrations least-privilege; dependencies scanned.

**Operations**
- [ ] Patch ownership, vulnerability scanning, runbooks, on-call.

## Output
Findings table: ID, description, risk (likelihood x impact), recommendation, owner, due date, accepted
risk sign-off if not fixed. Re-review if architecture changes materially.

## Gotchas
- Reviewing a diagram that no longer matches reality; ask for the deployed IaC or cloud inventory.
- Checklists miss business-logic abuse; pair with a threat model for high-risk systems.

## Verify
- [ ] Every high finding has an owner and date or signed risk acceptance.
