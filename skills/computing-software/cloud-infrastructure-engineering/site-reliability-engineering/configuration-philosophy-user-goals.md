---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.configuration-philosophy-user-goals
name: configuration-philosophy-user-goals
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [configuration-philosophy, user-goal-questions, configuration-design, sane-defaults, toil-reduction]
level: advanced
status: docs-checked
description: "Design configuration surfaces per the Workbook: ask questions close to the user's goals, not infrastructure details; minimise mandatory knobs; provide safe, documented defaults."
sources: ["https://sre.google/workbook/configuration-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration philosophy: questions close to user goals

SRE Workbook chapter 14, "Configuration Design and Best Practices": the ideal configuration is no
configuration at all, and the desirable direction is away from many tunables and toward simplicity.
Configuration ultimately boils down to an interface that **asks users questions**. Every knob is a
question the user must answer before getting back to their real business goal.

## Infrastructure-centric vs user-centric
- Infrastructure-centric view: offer as many knobs as possible so users can tune to perfection.
- User-centric view: fewer knobs are better, because answering configuration questions is a chore.
  The chapter favours this view, which needs software designed for a defined audience (user research).
- Limited options can lead to better adoption than very versatile software, because the software
  mostly works out of the box. Systems can move toward the user-centric view as they mature by
  removing knobs.

Illustration (ours, not from the page): prefer `expected_qps` and a latency target over
`threads` and `heap_mb`, and let the system derive the infrastructure-level answers.

## Practical rules (from the chapter)
- **Questions close to user goals**: on one end the user describes needs in their own terms, on the
  other exactly how to implement them. Goal-level input lets the system improve its implementation over time.
- **Mandatory vs optional**: mandatory questions must be answered for any function (for example who to
  charge); optional ones improve quality (for example worker count). Minimise mandatory ones by turning
  them into optional ones with defaults that apply safely to most users.
- **Defaults matter**: most users use the default, so a wrong default does a lot of harm.
- **Escape hatches**: treat configuration as optional overrides of high-level default behaviour, so power
  users can fine-tune without burdening everyone.
- **Add knobs only when motivated by a real need**; remove optional questions with no clear use case.
- If more than a small subset of users need complex configuration, revisit your assumptions about common use cases.

## Gotchas
- Dynamic defaults can stop matching your user base; if a significant portion report problems, improve the
  decision logic broadly rather than adding knobs.
- Optimise the total hours spent configuring across the organisation, including decision paralysis and
  correcting wrong turns, not just the keystrokes.

## Verify
- [ ] Count of mandatory fields per configuration surface; justify each.

## Checked
2026-11-01. Confirmed against SRE Workbook chapter 14 (sre.google/workbook/configuration-design/): ideal of no configuration, user-centric vs infrastructure-centric views, closeness to user goals, mandatory vs optional questions, defaults, escaping simplicity, and the cost of knobs.
Removed: the infrastructure vs user table values, the YAML platform example (kept only as a labelled illustration in prose), "version the defaults" and "removing knobs later is hard" advice, and the effective-config claim, because the chapter does not state them.
Method: documentation only; no commands were run.
