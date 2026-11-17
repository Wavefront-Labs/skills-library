---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.toil-reduction
name: toil-reduction
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, toil-reduction, sre, automation, runbook-automation, operational-load]
level: practitioner
status: docs-checked
description: "Measure and cut toil the SRE way: define toil, sample time spent, cap it at 50%, rank by cost, and automate or eliminate the top items with tracked payback."
sources: ["https://sre.google/sre-book/eliminating-toil/", "https://learn.microsoft.com/azure/well-architected/operational-excellence/automate-tasks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toil measurement and reduction

## Steps
1. **Define toil** as the SRE book does: work tied to running a production service that tends to be manual,
   repetitive, automatable, tactical (interrupt-driven, reactive), devoid of enduring value, and that scales linearly
   (O(n)) with service growth. Not every toil task has all attributes; the closer work matches, the likelier it is
   toil. Overhead (team meetings, goal setting, HR paperwork) is not toil. Grungy work with long-term value is not
   toil. Running a script by hand is still toil time (hands-on time counts). Doing a task for the first or second time
   is not toil. If human judgment is essential it is probably not toil, but check whether better design could remove
   the need for judgment.
2. **Measure.** Google runs quarterly surveys of SREs; the book reports an average of about 33% time spent toiling,
   with outliers from 0% to 80%. Top reported sources: interrupts (non-urgent messages and email), then on-call
   (urgent) response, then releases and pushes. Combine surveys with ticket and page data.
3. **Set a cap.** Google SRE's goal is toil below 50% of each SRE's time, with at least 50% on engineering project
   work, averaged over a few quarters or a year (toil is spiky). Persistent shortfall means the team should step back
   and find what is wrong. A person on a rotation has a floor: with one primary and one secondary week per cycle, a
   6-person rotation gives at least 2/6 = 33% and an 8-person rotation 2/8 = 25%.
4. **Rank** candidates and weigh automation by return on investment (Azure Well-Architected OE:10): prioritise
   straightforward procedural tasks expected to stay relevant, favour automation needing little maintenance, keep
   automated tasks focused on discrete jobs with few dependencies, and use off-the-shelf tools matched to team skills
   rather than building in-house.
5. **Pick the right fix.** Redesign so the task disappears where possible; automation need not be all-or-nothing
   (keep human judgment at key decision points). Areas the Azure page lists include deployments via IaC, and
   monitoring and alerting with alert-triggered remediation actions.
6. **Report** time reclaimed and residual toil each quarter.

## Gotchas
- Too much toil causes career stagnation, low morale, slower feature velocity, and sets a precedent of Dev teams
  shifting operational work onto SRE. Some toil is unavoidable and fine in small doses.
- When individual engineers report excessive toil, spread the load more evenly and give them engineering projects.
- Complex automation that needs heavy maintenance is hard for operations teams to troubleshoot.

## Verify
- [ ] Toil percentage measured per team, trending down or under 50%.
- [ ] Top toil sources each have an elimination or automation item scheduled.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the SRE book chapter "Eliminating Toil" and the Azure Well-Architected automation strategies page.
Removed: the SRE workbook source (not read), named tools (SSM Automation, Azure Automation, Rundeck), the
frequency x minutes x people formula, the 2-4 week tagging window, and the "do not automate a yearly 10-minute job"
advice, none of which the read pages state.
