---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.automation-hierarchy-toward-autonomous-systems
name: automation-hierarchy-toward-autonomous-systems
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, toil, automation-hierarchy, autonomous-systems, automation-evolution]
level: advanced
status: docs-checked
description: "Evolve operational tasks along the automation hierarchy, from manual runbooks to externally maintained scripts, generic automation and finally autonomous systems."
sources: ["https://sre.google/sre-book/automation-at-google/", "https://sre.google/workbook/eliminating-toil/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automation hierarchy

**Goal:** know where each operational task sits and what the next step up looks like.

## The evolution (SRE Book, database failover example)
1. **No automation**: the database master is failed over manually between locations.
2. **Externally maintained, system-specific automation**: an SRE has a failover script in their home directory.
3. **Externally maintained, generic automation**: the SRE adds database support to a generic failover script that everyone uses.
4. **Internally maintained, system-specific automation**: the database ships with its own failover script.
5. **Systems that do not need any automation**: the database notices problems and fails over without human intervention (an autonomous system).

The book's argument: external glue logic suffers bit rot because it is maintained separately from the core system and does not change when the system does; tighter coupling often fails because product developers resist a test deployment requirement for every change; and automation that runs rarely (cluster failover happens maybe every few months) is fragile because of the long feedback cycle. So aim to handle first-order manipulations (adding accounts, turnup) directly inside the application.

## Why automate
- Consistency: a human repeating a task hundreds of times will not do it the same way each time; for well-scoped procedures this is the primary value.
- Platform: a platform centralises mistakes (a bug is fixed once), can be extended, can run continuously or at inconvenient times, and exports metrics.
- Faster repairs: automation that resolves common faults reduces mean time to repair.
- Faster action: machines react faster than humans for well-defined failover or traffic switching.
- Time saving: once a task is encapsulated, anyone can execute it, decoupling operator from operation.

## Cautions
- Automation is a force multiplier, not a panacea; done thoughtlessly it creates as many problems as it solves. Scope automatic procedures over well-defined domains.
- Higher-level abstractions are easier to reason about, but when one leaks you fail systemically and repeatedly. Few abstractions model partial outcomes such as a push that is staged but not restarted; good automation halts and calls for intervention.
- Diskerase incident: a decommission re-run found an empty set of machines to erase, the empty set was interpreted as meaning everything, and almost all CDN machines in all colos were wiped. The fixes were more sanity checks including rate limiting, and making the workflow idempotent.
- Workbook safety guidance: validate input carefully even from upstream systems, add safeguards such as command timeouts and checks of current metrics, remember that naive read operations can spike load, and default to human operators when an unsafe condition is met.
- An interim step from the Workbook: start with a human-backed interface (a defined request interface while engineers still handle operations behind it), then move toward full automation.
- Not everything should be automated, and the time saved is often less immediately calculable than expected; the book says automation is worth implementing in more cases than a simple time-expended versus time-saved calculation suggests.

## Verify
- [ ] Inventory of top operational tasks with current level and next target level; each automated task has safety limits and handles the empty-input case.

## Checked
Method: docs-checked 2026-11-09 against the SRE Book chapter "Automation at Google" (value of automation, hierarchy of automation classes, Diskerase case and recommendations) and the SRE Workbook chapter "Eliminating Toil" (human-backed interfaces and the automation risk guidance). The SRE Book "Eliminating Toil" source was not used and was dropped. Removed the how-to-climb sequence (runbook then script then idempotent then monitoring-triggered) and the frequency x time x risk prioritisation as not stated there.
