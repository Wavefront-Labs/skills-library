---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.postmortem-writing-review-and-action-items
name: postmortem-writing-review-and-action-items
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [postmortem, blameless-postmortem, postmortem-template, postmortem-document-structure, postmortem-review-process, postmortem-publishing, postmortem-action-items, action-item-tracking, blameless-language, counterfactual-language]
level: practitioner
status: docs-checked
description: "Write a blameless postmortem from a solid template, run the review and publishing process, and make action items actually get done; with language rules that keep it blameless."
sources: ["https://sre.google/sre-book/postmortem-culture/", "https://sre.google/workbook/postmortem-culture/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Postmortem writing, review and action items

## When
The SRE Book lists common triggers: user-visible downtime or degradation beyond a threshold, data loss of any kind,
on-call intervention (release rollback, rerouting traffic), resolution time above a threshold, and a monitoring failure.
Define the criteria before an incident happens, and let any stakeholder request one.

## Template
Sections in the Workbook's example postmortem:
```
Header             owner, shared with, status, incident date, published date
Executive summary
Problem summary    duration, products affected, user, revenue and team impact
Background, glossary (so readers outside the team can follow)
Root causes and trigger
Timeline / recovery efforts
Lessons learned    what went well / what went poorly / where we got lucky
Action items       table: item, type (prevent/mitigate), priority, owner, tracking bug
Supporting data    graphs and links back to the sources
```

## Review and publish
1. Share the first draft internally and ask senior engineers to assess it. The Book's review questions: was key incident
   data collected, are impact assessments complete, was the root cause sufficiently deep, is the action plan and bug
   priority appropriate, and were stakeholders told the outcome.
2. Hold regular review sessions so no postmortem is left unreviewed; close open comments and finalise.
3. Share widely (the Workbook says the default should be everyone at the company) and add it to a repository of past
   incidents. Never include information that identifies an end user.
4. Publish promptly. The Workbook's good example went out in under a week; its bad example took four months, and the
   incident recurred in between.

## Action items that get done
Workbook characteristics of good items:
- Each has one owner and a tracking bug; one owner for the postmortem too, with others as collaborators.
- Each has a priority, so teams know what to tackle first.
- Each has a verifiable end state; avoid vague verbs such as "improve" or "make better".
- Include preventative items, not only mitigations. Changing automated systems and processes is more reliable than
  trying to change human behaviour.
- Group items by theme when there are many.
Ben Treynor Sloss is quoted: every postmortem after a user-affecting outage must have at least one P0 or P1 bug.

## Blameless language
- Focus on what went wrong, not who caused it; name no individual or team as the culprit.
- Keep the text factual: no personal judgments or dramatic wording, and back severity claims with data.
- Assume everyone involved had good intentions and did the right thing with the information they had (SRE Book).
- Aim action items at improving the system rather than people.

## Gotchas
- A postmortem that names individuals leads people to hide facts that matter for preventing recurrence.
- Empty Background and Glossary sections make a postmortem unreadable to other teams.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Postmortem Culture: Learning from Failure" (triggers, review
questions, review sessions, repository, blameless principle) and the SRE Workbook chapter "Postmortem Culture" (template
sections, action item characteristics, sharing, promptness, P0 or P1 quote, blameless language). Removed: the 2-5 day
drafting window, the P0-P2 scale, the "Detection" and UTC timeline rows, the "human error" and counterfactual language
table, the 80 percent closure target, the production-meeting tracking advice and the example-postmortem source (not read).
Method: documentation only; no commands were run.
