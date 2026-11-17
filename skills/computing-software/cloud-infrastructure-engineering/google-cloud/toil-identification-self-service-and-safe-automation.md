---
id: computing-software.cloud-infrastructure-engineering.google-cloud.toil-identification-self-service-and-safe-automation
name: toil-identification-self-service-and-safe-automation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, toil-reduction, toil-identification, toil-survey, automation-service-accounts, self-service-provisioning, automation-testing, automation-rollback, sre]
level: practitioner
status: docs-checked
description: "Identify and measure ops toil using Google SRE's definition, a toil budget and surveys, then decide what to automate or design away."
sources: ["https://sre.google/sre-book/eliminating-toil/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toil identification

## 1. Define it
Per the Google SRE book, toil is work tied to running a production service that tends to be manual, repetitive,
automatable, tactical, devoid of enduring value, and that scales linearly (O(n)) with service growth. The more of those
attributes a task has, the more likely it is toil.
- **Manual**: running a script by hand is still toil time, even if quicker than the steps.
- **Repetitive**: a first or second time is not toil; novel problem solving is not toil.
- **Automatable**: a machine could do it as well, or the need could be designed away. Be careful about excusing a task as
  "needs human judgment" if better design could remove the need; until then it is toil.
- **Tactical**: interrupt-driven and reactive (handling pager alerts).
- **No enduring value**: the service is in the same state afterwards.
- **O(n)**: work grows with service size, traffic or users.
Not toil: overhead (meetings, HR paperwork), and grungy work with lasting value (cleaning up alerting configuration).

## 2. Measure it
- Survey engineers regularly. Google's SRE reports quarterly surveys; their average toil was about a third of time, but
  averages hide outliers, and a person reporting excessive toil usually signals the load needs spreading and that
  person needs engineering projects.
- The SRE book's goal is to keep toil below 50% of each SRE's time, averaged over a few quarters or a year, because toil
  expands if unchecked. On-call carries a floor: in a 6-person rotation with one primary and one secondary week per cycle,
  at least 2/6 of time is on-call and interrupt handling.
- Top reported sources of toil in the book: interrupts (non-urgent messages), then urgent on-call response, then releases
  and pushes.
- Track the percentage per quarter and turn the biggest categories into engineering projects.

## 3. Engineering vs toil
Engineering work is novel, needs human judgment, produces a permanent improvement and is guided by a strategy. Software
engineering (automation, tools, frameworks) and systems engineering (lasting configuration improvements) both count.

## Gotchas
- Toil is not always bad in small doses; it becomes toxic in large quantities (career stagnation, low morale, slower
  feature velocity, setting a precedent for more toil).
- Automating a broken process just speeds up the breakage; simplify the process first.

## Verify
- [ ] Toil percentage is reported quarterly and trending down.

## Checked
2026-11-09: read the SRE book chapter "Eliminating Toil" in full (definition, 50% goal, on-call floor, survey result,
engineering categories). Removed unread specifics: ticket-analysis numbers, GCP toil examples, service-account and
keyless automation guidance, PR-based self-service, dry-run and rollback practice (their sources were not read).
Method: documentation only; no commands were run.
