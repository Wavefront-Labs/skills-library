---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.access-reviews
name: access-reviews
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, access-reviews, recertification, entitlement-review, privileged-access-review, iam-access-analyzer, unused-access]
level: practitioner
status: docs-checked
description: "Run periodic cloud access reviews: scope, reviewers, evidence from last-used data, automatic removal of unused access, and audit trail for SOC 2 / ISO 27001."
sources: ["https://learn.microsoft.com/entra/id-governance/access-reviews-overview", "https://learn.microsoft.com/entra/id-governance/create-access-review", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-create-unused.html", "https://cloud.google.com/policy-intelligence/docs/role-recommendations-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access reviews and recertification

## Scope and frequency
Example starting cadences (a judgement call; set them from your own risk policy and audit obligations).
Entra access reviews can recur weekly, monthly, quarterly or annually.

| Access | Frequency |
|---|---|
| Privileged / admin roles, break-glass | Quarterly (or monthly) |
| Production data access | Quarterly |
| Standard workforce access to cloud accounts | Semi-annual |
| Service principals / workload identities | Quarterly (owner confirms) |
| External / guest users | Quarterly |

## Steps
1. Generate review campaigns from the identity source (Entra ID Access Reviews, IGA tool) or
   export IAM assignments per account.
2. Attach **evidence**: last sign-in / last used (Entra review recommendations such as "No sign-in within 30
   days", IAM Access Analyzer unused access, Google Cloud IAM recommender), group memberships, justification.
3. Reviewers = resource owner or manager (not the user); require explicit approve/deny. Entra also allows
   group owners, specified reviewers or self-review depending on what is reviewed.
4. **Auto-remove**: in Entra, "Auto apply results to resource" removes denied users when the review ends, and
   "If reviewers don't respond" can be set to Remove access. If both are on, a non-responding reviewer can cause
   all access to be revoked, so choose deliberately. Treat unused access as removal candidates: the AWS unused
   access analyzer takes a tracking period of 1 to 365 days, and the Google Cloud IAM recommender looks at up to
   the last 90 days of permission usage (its minimum observation period defaults to 90 days, settable to 30 or 60).
5. Right-size: replace broad roles with recommended narrower ones. The Google Cloud IAM recommender does not apply
   recommendations automatically; you review and apply or dismiss them.
6. Keep the audit trail (who reviewed, decision, date, removal executed).

## Gotchas
- Rubber-stamping: hundreds of items per reviewer with no evidence. Pre-filter and show usage.
- Reviews on group membership but not on what the group grants.
- Non-human identities skipped because nobody "owns" them.

## Verify
- [ ] Campaign completion rate and removals recorded.
- [ ] Sample shows denied access actually removed.

## Checked
2026-11-08. Confirmed against the Entra access reviews overview and create-access-review pages (recurrence,
reviewer types, auto apply, non-response setting, 30-day sign-in recommendation), the AWS unused access analyzer
creation page (tracking period 1-365 days) and the Google Cloud role recommendations overview (90-day observation,
30/60-day option, no automatic apply). Removed the unsourced fixed "90 days" removal rule and the replaced AWS
source page, which returned an empty stub. The review-cadence table is labelled as judgement, not a vendor claim.
Method: documentation only; no commands were run.
