---
id: computing-software.it-support-helpdesk.servicenow.zendesk-sla-policies
name: zendesk-sla-policies
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, zendesk, zendesk-sla, sla-policies, first-reply-time, next-reply-time, requester-wait-time, business-hours, sla]
level: practitioner
status: docs-checked
description: "Set up Zendesk SLA policies: first reply, next reply, periodic update, requester and agent wait time targets, policy order, business-hours schedules, reopen behaviour."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408829459866-Defining-and-using-SLA-policies"
  - "https://support.zendesk.com/hc/en-us/articles/4408842938522-Setting-your-schedule-with-business-hours-and-holidays"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zendesk-sla-policies

A Zendesk SLA policy has **conditions** (which tickets) and **targets** that measure metrics. Targets are always based on the system Priority field (Low, Normal, High, Urgent); custom fields, even ones named "Priority", cannot be used for targets. Manage policies in Admin Center > Objects and rules > Business rules > Service level agreements.

## Metrics
| Metric | Starts / runs | Stops or pauses |
|---|---|---|
| First reply time | Ticket creation (or first customer public comment if an agent created it with an internal note) | First public agent comment (or autoreply) |
| Next reply time | Oldest unanswered customer comment | Next public agent comment |
| Periodic update | Each public agent comment | Resets at the next public agent comment |
| Pausable update | First public agent comment in New, Open or On-hold | Pauses in Pending; resumes in Open or On-hold |
| Requester wait time | Ticket creation; time in New, Open, On-hold | Stops at Solved; pauses in Pending |
| Agent work time | Time in New and Open | Pauses in On-hold and Pending |
| Total resolution time | Ticket creation to Solved, including Pending | Only Solved stops it |

Best practices from the page: start with first reply time if unsure, pick only one resolution metric (requester wait time, agent work time or total resolution time), and you do not need a target for every metric. Next reply time and periodic update can both be active; the target status shows the one closest to breach.

## Setting up a policy
1. Create policy, name it, choose conditions (standard and custom fields allowed).
2. Add targets for the metrics you want and enter a time target per priority. The minimum target is 15 seconds; hours, minutes or seconds can be used.
3. Optionally choose calendar hours or business hours for each priority, then save.

The ticket must have a system Priority value or no SLA applies, even if all other conditions match; a trigger can set a default priority at creation. New policies are added at the bottom of the list and the order determines how policies are applied: put the most restrictive policies at the top and the least restrictive at the bottom.

## Business hours
Admin Center > Objects and rules > Business rules > Schedules: time zone, weekly hours and holidays (whole days only, up to two years ahead; holidays count as outside business hours). Professional plans allow one schedule; Enterprise allows several, the first in the list is the default for all tickets, and triggers can apply other schedules to tickets. Schedules do not apply to Chat operating hours.

## Reopened tickets
- First and next reply: a reopen with a public end-user comment activates new targets.
- Periodic and pausable update: a reopen with an end-user comment does nothing; a public agent comment (or autoreply) activates new targets.
- Requester wait time, agent work time: the same target reactivates with the same elapsed time, treating time in Solved as a pause.
- Total resolution time: continues counting from ticket creation, excluding time in Solved.

## Gotchas
- Policy order matters; a broad policy above a specific one can take precedence.
- If an agent creates a ticket with a public comment, first reply time is satisfied immediately and records no achievement.
- Reply metrics are not the same as the native Zendesk reply time metric.

## Verify
Create a test ticket per priority, confirm the SLA appears on it, reply publicly and confirm the first reply target is achieved.

## Checked

Confirmed against the Zendesk articles Defining SLA policies and Setting your schedule with business hours and holidays: metric definitions and pause behaviour, the 15-second minimum, system Priority requirement, policy ordering advice, Admin Center locations, schedule limits by plan, holidays and reopen behaviour. Removed the example policy figures, the claims about breach columns, Explore SLA datasets, automation SLA conditions, mid-life priority re-targeting and retroactive edits, which the pages do not state. The third cited page (Understanding SLA metrics) now redirects to the native reply time article and was not relied on.

Method: docs-only read of cited pages, 2026-11-08
