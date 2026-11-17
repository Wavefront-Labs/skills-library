---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.toil-reduction-and-automation
name: toil-reduction-and-automation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, toil, toil-reduction, toil-budget, automation, runbook-automation, self-service, interrupts, ticket-ops, on-call-load, pages-per-shift, automation-roi, xkcd-1205, auto-remediation, aws-systems-manager, ssm-automation, azure-automation, rundeck, stackstorm, chatops, operators, kubernetes-operators, eliminate-dont-automate, operational-load]
level: practitioner
status: docs-checked
description: "Measure toil, cap it with a toil budget, then eliminate, self-serve or automate the biggest sources in ROI order, with guardrails so auto-remediation can't make incidents worse."
sources: ["https://sre.google/sre-book/eliminating-toil/", "https://sre.google/workbook/eliminating-toil/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toil reduction and automation — measure it, cap it, delete it

**Goal:** operational work that is manual, repetitive and scales with traffic stays below an
agreed share of the team's time (Google's guideline: under 50%), and engineering time goes to
changes that make the service need less operating.

## 1. Recognise toil
Toil is work that is: **manual**, **repetitive**, **automatable**, **tactical** (interrupt-driven),
**no enduring value**, and **grows linearly with the service**. Examples: resizing disks by
ticket, rotating certificates by hand, restarting a leaky worker, approving routine access
requests, copying data between environments.
Not toil: solving a novel problem, design work, writing postmortems, and overhead such as team meetings or HR paperwork. The SRE Book counts handling pager alerts as toil, and says first-time or second-time work is not toil.

## 2. Measure before fixing
- Tag tickets and interrupts by category for 2-4 weeks (label in the ticket system or a simple log: task, minutes, frequency).
- Track pages per on-call shift and after-hours pages; the SRE Book's upper bound is 2 incidents per 12-hour on-call shift (about 6 hours each, including follow-up).
- Survey the team (Google runs quarterly SRE surveys on time spent toiling): "What did you do this week that a computer should have done?" catches unticketed work.
Output: a ranked table — task, occurrences/month, minutes each, total hours/month, trend.

## 3. Choose the fix, in this order
1. **Eliminate** — remove the cause: fix the memory leak instead of automating restarts; use managed certificates instead of a rotation script; enable storage autoscaling.
2. **Self-service** — give requesters a safe interface: a PR template, an internal portal, an IaC module with policy checks. Moves the work to the person who wants it, without a queue.
3. **Automate** — scripts → runbook automation → closed-loop controllers (operators, auto-remediation from alerts). The Book notes that running a script by hand is still toil time.
4. **Accept** — rare, cheap tasks; automating them costs more than they do.

## 4. ROI check
Hours saved per year = frequency × minutes × 12 / 60. Compare to build + maintenance time
(maintenance is easy to underestimate; budget for it). Weigh also:
error rate of the manual task, time-to-complete for the requester, and on-call sleep.
A task done twice a year but taking 3 hours and failing half the time is worth automating for risk, not time.

## 5. Safe auto-remediation
- Make actions **idempotent** and bounded: restart at most N pods per 10 minutes; never act on > X% of a fleet.
- **Rate limit and circuit-break** the automation itself; disable it if it fires repeatedly and page a human.
- Log every automated action into the incident/ops channel with a link to what triggered it.
- Dry-run mode first; promote after it would have been right for several weeks.
- Keep a manual runbook for when the automation is broken.

## 6. Cap it
Agree a toil budget (the Book's goal is below 50% of each SRE's time, averaged over a few quarters
since toil is spiky). When the measured share stays over it, reliability/automation work takes
priority over new operational commitments.

## Gotchas
- Automating a broken process just breaks it faster — fix the process first.
- Scripts living on one engineer's laptop are toil with extra steps; version, test and run them from a shared runner.
- Auto-remediation that masks a growing problem (restarting a leak hourly) hides signals — still alert on the frequency.
- Self-service without guardrails turns into an incident generator; pair with policy checks.

## Verify
- [ ] A toil log exists with hours/month per task for the last month.
- [ ] Toil share is reported each quarter against the agreed budget.
- [ ] Top 3 toil sources each have an eliminate/self-serve/automate decision and owner.
- [ ] Every auto-remediation has rate limits, a kill switch and logged actions.
- [ ] Pages per shift trend is tracked.

## Checked
2026-11-01. Confirmed in SRE Book Eliminating Toil: the toil attributes (manual, repetitive, automatable, tactical, no enduring value, linear growth), handling pager alerts counted as toil, overhead listed separately, the 50% goal, quarterly surveys; and Being On-Call: 2 incidents per 12-hour shift at about 6 hours each. Removed the vendor tool names, the 20-30% maintenance figure and the stop-accepting-services rule, which the sources do not support. The Workbook page was fetched but not read line by line.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.observability.alert-fatigue-reduction
