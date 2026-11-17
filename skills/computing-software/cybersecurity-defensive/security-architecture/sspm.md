---
id: computing-software.cybersecurity-defensive.security-architecture.sspm
name: sspm
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [sspm, saas-security-posture-management, saas-misconfiguration, oauth-app-governance, m365-secure-score, cis-microsoft-365-benchmark, shadow-saas]
level: practitioner
status: draft
description: "Manage SaaS security posture: inventory SaaS and OAuth integrations, baseline configs (CIS M365, Google Workspace, Salesforce), SSPM tooling, drift alerts and owner remediation."
sources: ["https://www.cisa.gov/resources-tools/services/secure-cloud-business-applications-scuba-project", "https://github.com/cisagov/ScubaGear", "https://www.cisecurity.org/benchmark/microsoft_365", "https://learn.microsoft.com/en-us/defender-cloud-apps/security-saas"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SaaS security posture management (SSPM)

## Scope
Tenant-level settings of business SaaS (M365, Google Workspace, Salesforce, Slack, GitHub, Okta,
ServiceNow, Zoom) plus the third-party OAuth apps and integrations connected to them.

## Steps
1. **Inventory**: sanctioned SaaS (IdP app catalogue), shadow SaaS (CASB/SWG discovery, expense reports, OAuth grants).
2. **Baseline** each critical tenant:
   - M365/Entra: CISA ScubaGear (`Invoke-SCuBA -ProductNames aad,exo,defender,sharepoint,teams`) produces a report against CISA SCuBA baselines; CIS M365 benchmark.
   - Google Workspace: ScubaGoggles.
   - Salesforce: Health Check score; GitHub: org settings (2FA required, base permissions read, fork policy).
3. **Tooling**: an SSPM (Defender for Cloud Apps SSPM, AppOmni, Adaptive Shield, Obsidian) continuously evaluates and alerts on drift.
4. **OAuth/integration governance**: review high-privilege third-party apps (Mail.ReadWrite, Drive full access), unverified publishers, apps unused for 90 days -> revoke.
5. **Ownership**: each SaaS has a business owner and technical admin accountable for findings.

## High-value checks
External sharing defaults, guest access, MFA/SSO enforcement with local login disabled, admin count,
audit logging enabled and exported, legacy auth/API tokens, public links, data export permissions.

## Gotchas
- SSO enforced but local password login still possible for "break-glass" users in many SaaS - list them.
- SaaS audit logs often have short retention on lower licence tiers; export to SIEM.

## Verify
- [ ] ScubaGear/benchmark run with failures tracked to closure.
- [ ] OAuth app review completed this quarter.
