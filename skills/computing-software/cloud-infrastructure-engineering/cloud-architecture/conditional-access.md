---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.conditional-access
name: conditional-access
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, conditional-access, mfa, phishing-resistant-mfa, fido2, device-compliance, entra-conditional-access, sign-in-risk]
level: practitioner
status: draft
description: "Design MFA and conditional access for cloud admins: phishing-resistant MFA, device compliance, risk conditions, break-glass exclusions and report-only rollout."
sources: ["https://learn.microsoft.com/entra/identity/conditional-access/overview", "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf", "https://cloud.google.com/beyondcorp-enterprise/docs/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MFA and conditional access policy

## Baseline policies (Entra Conditional Access naming; similar in Okta/Google context-aware access)
1. Require MFA for all users; block legacy authentication protocols.
2. **Phishing-resistant MFA** (FIDO2 security keys, passkeys, Windows Hello for Business,
   certificate-based) for admin roles and cloud console access (authentication strengths).
3. Require compliant or hybrid-joined device for privileged access / admin portals.
4. Block or require step-up for high sign-in risk and user risk (Identity Protection).
5. Restrict by location only as a secondary control (named locations), not primary.
6. Session controls: sign-in frequency for admin sessions, no persistent browser sessions.
7. Workload identities: conditional access for service principals where supported (location).

## Rollout
1. Create policies in **report-only** mode; review sign-in logs for impact (What If tool).
2. Exclude break-glass accounts (monitored, FIDO2-protected) from policies that could lock you out.
3. Enable for pilot group -> admins -> all.
4. Document every exclusion with owner and expiry.

## Gotchas
- SMS/voice and push-without-number-matching MFA are phishable/fatigue-prone.
- Excluding service accounts broadly creates a bypass; use workload identities instead of users.
- Locking out all admins with a misconfigured policy - always keep break-glass excluded and tested.

## Verify
- [ ] Sign-in logs show 100% admin sign-ins with phishing-resistant methods.
- [ ] Legacy auth sign-ins at zero.
