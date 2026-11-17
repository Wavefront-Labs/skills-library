---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.ticket-queue-hygiene
name: ticket-queue-hygiene
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, toil, ticket-queue-hygiene, interrupts, triage, kanban]
level: practitioner
status: docs-checked
description: "Keep an SRE ticket queue healthy: intake rules, triage rotation, priorities and SLAs, closing stale tickets, and mining tickets for toil to automate."
sources: ["https://sre.google/sre-book/dealing-with-interrupts/", "https://sre.google/workbook/eliminating-toil/", "https://sre.google/sre-book/eliminating-toil/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ticket queue hygiene

**Goal:** tickets get handled predictably, nobody drowns, and repeated work becomes automation.

## Intake
- One queue per team, one intake path (form/template) with required fields: service, impact, urgency, desired date, links.
- Route requests that need no human (access grants, quota bumps) to self-service; ticket only exceptions.
- Distinguish **pages** (urgent, on-call), **tickets** (days), **project work** (weeks).

## Triage
- Tickets are a full-time role for a manageable period, never assigned at random across the team (SRE Book, Dealing with Interrupts). If tickets exceed what primary and secondary on-call can close, staff two ticket handlers rather than spreading the load; everyone else gets uninterrupted project time.
- Triage within one business day: priority, owner, or reject/redirect with reason.
- Priority definitions with response targets that your team sets and publishes.

## Keep it clean
- Regular scrub of tickets and pages (the Book's term): look at classes of interrupts for a root cause, merge duplicates, re-prioritise, and close stale tickets after asking the requester.
- WIP limit per person; tickets older than N days get escalated or explicitly deferred.
- Handoff notes when the ticket handler rotates; open tickets stay with the queue, not with the departing person. The Book notes many teams hand off on-call but few hand off tickets.

## Mine for toil
- Tag every ticket with a category; monthly count by category and time spent.
- Top categories by hours become automation or self-service projects (toil reduction backlog).
- Track the ratio of ticket time to project time against the 50% toil cap.

## Metrics
Inflow vs outflow per week, age distribution (p50/p90), reopen rate, time per category. The Book gives measurable overload goals such as fewer than 5 daily tickets and fewer than 2 paging events per shift.

## Verify
- [ ] No untriaged tickets older than your triage target; monthly toil report produced from ticket categories.

## Checked
2026-11-01. Confirmed in the SRE Book chapters Dealing with Interrupts (full-time ticket role, no random assignment, two handlers when needed, regular scrub, ticket handoff, root-cause analysis) and Being On-Call (example goals of fewer than 5 daily tickets and fewer than 2 paging events per shift), and Eliminating Toil (50% cap). Removed the invented priority response times and the 14-day stale rule.
Method: documentation only; no commands were run.
