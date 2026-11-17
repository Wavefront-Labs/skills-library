---
id: computing-software.cybersecurity-defensive.identity-access-management.access-reviews-and-certification
name: access-reviews-and-certification
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [identity-lifecycle, access-reviews, access-certification, user-access-review, entra-access-reviews, iga, sox-access-review, privileged-access-review]
level: practitioner
status: draft
description: "Run access reviews that remove access rather than rubber-stamp it: scope, reviewers, review data quality, decisions, auto-remediation and audit evidence."
sources: ["CIS Control 5.1 and 6.x (account inventory and access management)", "NIST SP 800-53 AC-2(3) and AC-6(7) review of privileges", "Microsoft Learn - Microsoft Entra access reviews"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Access reviews and certification

**Goal:** periodically confirm that every account and entitlement is still needed, and remove
what is not, with evidence for auditors.

## Scope and frequency (risk-based)
| Access | Frequency | Reviewer |
|---|---|---|
| Privileged roles (domain/global admin, cloud admin, PAM) | Quarterly or monthly | Role owner / security |
| Access to regulated systems (SOX financial apps, PCI, PHI) | Quarterly | Application owner and manager |
| Guest / external users | Quarterly | Sponsor |
| Standard business apps | Annually or semi-annually | Manager |
| Service accounts | Semi-annually | Technical owner |

## Make reviews meaningful
- Give reviewers context: last sign-in date, entitlement description in plain language, peer
  comparison ("90% of this person's team does not have this").
- Recommend decisions (Entra access reviews: "deny if no sign-in in 30 days").
- Keep reviews small: per application or per role, not 2,000 lines in one spreadsheet.
- Default for non-response: escalation, and for low-risk access, removal after the deadline.
- **Auto-apply** results (Entra/IGA removes denied access); manual tickets get lost.

## Microsoft Entra example
Identity Governance > Access reviews > New: scope group/app/role, reviewers (managers or
owners), recurrence, "If reviewers don't respond: Remove access", "Auto apply results",
decision helpers on. For Entra roles use PIM access reviews.

## Evidence for audit
Population snapshot at review start, reviewer decisions with timestamps, removals executed,
exceptions approved. Keep per review cycle.

## Gotchas
- Rubber-stamping: 100% approve rates and reviews completed in seconds are red flags; report them.
- Reviews of group membership miss access granted directly in the application; review the app's own entitlements too.
- Reviewer is the person being reviewed (self-review) for managers' own access: route to their manager.

## Verify
- [ ] Each cycle removes some access (a 0% removal rate means the review is not working).
- [ ] Removed access verified absent in the target system after the cycle.
