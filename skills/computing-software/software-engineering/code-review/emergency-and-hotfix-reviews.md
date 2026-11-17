---
id: computing-software.software-engineering.code-review.emergency-and-hotfix-reviews
name: emergency-and-hotfix-reviews
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, emergency-review, hotfix-review, incident-response, break-glass, post-merge-review]
level: practitioner
status: docs-checked
description: "Review emergency fixes during incidents: what counts as an emergency, what to prioritise, hard versus soft deadlines, and the thorough review afterwards."
sources: ["https://google.github.io/eng-practices/review/emergencies.html", "https://google.github.io/eng-practices/review/reviewer/looking-for.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Emergency and hotfix reviews

## Is it an emergency? (Google's definition)
A small change that: allows a major launch to continue instead of rolling back, fixes a bug
significantly affecting users in production, handles a pressing legal issue, or closes a major
security hole.

**Not** emergencies: wanting to launch this week rather than next (unless there is a real hard
deadline such as a partner agreement); a developer who has worked long on a feature and wants it
in; reviewers being in another timezone or off-site; Friday end of day; a manager's soft
deadline; rolling back a change that is causing test failures or build breakages.

## Hard versus soft deadlines
A hard deadline is one where something disastrous happens if it is missed (a contractual
obligation, a product that fails completely in the market, a once-a-year hardware submission
window). Delaying a release for a week is not disastrous. Most deadlines are soft, and you should
not sacrifice code health for them. If large changes routinely arrive at the end of a long
release cycle with only superficial review, change the process so big features land early
enough for good review.

## Reviewing the emergency change
In an emergency, the whole review process must be fast, not just the first response. The
reviewer cares most about speed and about correctness: does the change actually resolve the
emergency? Emergency reviews take priority over all other reviews. Emergency changes may include
their tests later: tests normally go in the same change except when it is an emergency.

## After the emergency
Look over the emergency change again and give it a more thorough review.

## Checked

2026-11-08. Read in full: Google eng-practices "Emergencies" (definition, not-emergencies list, hard deadlines, speed and correctness priority, follow-up review) and the tests-with-code line in "What to look for in a code review". Removed: the roll-back-first advice, the six-point fast checklist, break-glass and post-merge-within-one-business-day rules, back-porting and postmortem steps, and the SRE workbook and branch-protection sources, which were not confirmed from the pages used.

Method: documentation only; no commands were run.
