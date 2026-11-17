---
id: computing-software.software-engineering.code-review.choosing-reviewers
name: choosing-reviewers
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, choosing-reviewers, codeowners, review-latency, reviewer-assignment, knowledge-sharing]
level: intro
status: draft
description: "Choose the right reviewers and get timely attention: owners vs domain experts, how many reviewers, CODEOWNERS and auto-assignment, and polite nudging."
sources: ["https://google.github.io/eng-practices/review/developer/", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners", "https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team", "https://docs.gitlab.com/user/project/codeowners/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing reviewers and getting attention

## Who
- **Owner** of the code being changed (CODEOWNERS): required for approval in most setups.
- **Domain expert** for risky parts (security, database, concurrency, payments, accessibility).
- **Someone who should learn** this area (spreading knowledge; reduces bus factor).
- Usually **one** primary reviewer who reviews everything, plus targeted reviewers for specific
  files ("@dba please review the migration only"). Many reviewers = diffusion of responsibility.
- Avoid always picking the same senior person; it bottlenecks them and keeps others from learning.

## Automating
- `CODEOWNERS` (`/db/migrations/ @acme/dba`, `*.tf @acme/platform`) auto-requests and can be required
  by branch protection/approval rules. Last matching pattern wins (GitHub).
- GitHub team review settings: round-robin or load-balanced auto-assignment, "never assign certain
  members", notify team.
- GitLab: CODEOWNERS sections with required approvals; Reviewer Roulette in some setups.

## Getting attention
- Make it easy: small PR, clear description with "how to review" pointers, CI green before
  requesting review, self-review done.
- Ask in the right channel with a link and size estimate ("~120 lines, needs DB eyes, blocking the
  release Thursday").
- Agree on team norms: first response within one business day (Google's guideline: respond within
  one business day at most), then follow up politely if no response.
- If blocked: ask the reviewer if someone else should take it; escalate to the team lead only after
  that.
- Time zones: pick a reviewer awake during your overlap for urgent changes.

## Re-requesting
After addressing comments, reply to each thread, push, and re-request review (GitHub button /
GitLab "re-request"), so the reviewer gets notified.
