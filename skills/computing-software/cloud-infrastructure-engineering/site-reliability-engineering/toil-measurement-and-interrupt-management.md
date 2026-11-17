---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.toil-measurement-and-interrupt-management
name: toil-measurement-and-interrupt-management
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [toil, measuring-toil, toil-survey, toil-tracking, toil-taxonomy, toil-classification, toil-budget-enforcement, fifty-percent-rule, interrupts, interrupt-handling, interrupts-rotation, ticket-rotation, flow-state, polarizing-time, interrupt-shield]
level: practitioner
status: docs-checked
description: "Measure toil (surveys, ticket tagging), classify it, hold the 50% cap, and organise interrupts with dedicated ticket and on-call roles so the rest of the team keeps flow time."
sources: ["https://sre.google/sre-book/eliminating-toil/", "https://sre.google/workbook/eliminating-toil/", "https://sre.google/sre-book/dealing-with-interrupts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measuring toil and managing interrupts

## What counts as toil
The SRE Book: work tied to running a production service that tends to be manual, repetitive, automatable, tactical,
devoid of enduring value, and that scales linearly as the service grows. The more attributes a task has, the more
likely it is toil. Doing something for the first or second time is not toil, and neither is solving a novel problem.
The Book names handling pager alerts as toil.

## Measure (Workbook)
- Identify it; the people best placed are the stakeholders, including those who do the work.
- Pick an objective unit of effort: minutes or hours (account for context switching), or a unit such as a completed
  ticket, a manual production change, or an applied patch.
- Track continuously before, during and after reduction work, using tools or scripts so measuring is not new toil.
- The Book reports Google runs quarterly surveys of SREs, and notes averages hide outliers: when one person reports
  excessive toil, managers should spread the load more evenly.

## Taxonomy (Workbook)
Business processes (ticket-driven requests), production interrupts, release shepherding, migrations, cost engineering
and capacity planning, and troubleshooting for opaque architectures. The Workbook says the list is not exhaustive and
toil is a spectrum rather than a binary classification.

## The 50% goal
The Book's goal: keep operational work (toil) below 50% of each SRE's time, so at least 50% goes to engineering
project work. It is averaged over a few quarters or a year, because toil is spiky. If project time averages
significantly below 50% over the long haul, the team should step back and work out what is wrong.

## Interrupts (SRE Book, "Dealing with Interrupts")
Operational load has three kinds: pages, tickets and ongoing operational responsibilities.
- **Polarise time**: a person should know on arrival whether today is project work only or interrupts only. A 20-minute
  interruption costs two context switches, realistically a couple of hours of productive work. The ideal period is a
  week; a day or half-day may be more practical.
- **On-call**: the primary should focus solely on on-call; treat that week as written off for project work.
- **Tickets**: make it a full-time role for a manageable period. Do not assign tickets randomly across the team. If
  tickets exceed what primary and secondary can close, have two people on tickets instead of spreading the load.
- **Volume too high for one person**: add another person for that class of interrupt.
- **Ongoing responsibilities**: define roles anyone can pick up (for example a push manager) and formalise handover.
- **Hand off tickets as well as pages**, and regularly scrub tickets and pages for root causes; the Book suggests
  silencing a class of interrupts until its fix lands.
- Do not dip into the ticket queue when not assigned to it; it skews the picture of ticket load.

## Checked
2026-11-01. Confirmed against the SRE Book chapters "Eliminating Toil" (definition, 50% goal, quarterly surveys,
averaging) and "Dealing with Interrupts" (categories, polarising time, on-call, tickets, handoff, scrub) and the SRE
Workbook chapter "Eliminating Toil" (measuring steps, taxonomy). Removed: the survey question wording, the "toil" label
scheme, the two-quarter enforcement actions (pause onboarding, push work back to developers), the prioritisation
formula, weekly rotation prescription, the "no quick-question DMs" rule and the verify items; none is on these pages.
Method: documentation only; no commands were run.
