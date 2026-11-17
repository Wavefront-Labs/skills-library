---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.systematic-problem-isolation
name: systematic-problem-isolation
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, troubleshooting, comptia, comptia-a-plus, seven-step-method, problem-isolation, root-cause-analysis, five-whys, half-splitting, divide-and-conquer, osi-model, bottom-up, top-down, known-good, baseline, hypothesis, test-plan, change-one-variable, reproduce, scope, escalation, time-box, documentation, preventive-measures, service-desk, half-split]
level: practitioner
status: draft
description: "A professional helpdesk troubleshooting method: CompTIA-style seven steps, scoping, reproduction, half-splitting, OSI order, known-good comparison, hypothesis log, 5 Whys and time-boxed escalation."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Systematic problem isolation

**Goal:** find the actual cause in the fewest moves, prove it, fix it without collateral
damage, and leave a record good enough that nobody has to rediscover it. This is the
professional counterpart of
computing-software.general-digital-literacy.basic-troubleshooting.everyday-troubleshooting-method
(the end-user ladder); it assumes admin tools and a ticket system.

## The seven-step frame (CompTIA A+ style, adapted)
1. **Identify the problem** — gather facts, question the user, check logs, ask what
   changed, back up data before making changes.
2. **Establish a theory of probable cause** — question the obvious; list several
   candidates, not one.
3. **Test the theory** — confirmed → plan; refuted → new theory or escalate.
4. **Plan the fix and implement it** — consider side effects, change windows and policy.
5. **Implement or escalate.**
6. **Verify full functionality** — with the user, and add preventive measures.
7. **Document** findings, actions and outcomes.
The rest of this skill is how to do steps 1-3 well.

## 1. Gather information
- **Who** is affected (one user, a role, a site, everyone)? **What** exactly fails —
  exact error text, error code, screenshot? **When** did it start and is it constant,
  intermittent or time-of-day? **Where** — device, network, location, app version?
- **What changed?** Updates, deployments, password changes, moves, new hardware. Check
  the change calendar and Reliability Monitor; recent changes cause most incidents.
- **Scope** before depth: if three users at one site fail, stop debugging one laptop.
  Check monitoring and open incidents for an existing outage.

## 2. Reproduce
Get the steps that make it happen, on the user's device and ideally on yours. If it
can't be reproduced, collect timestamps and logs for next occurrence (ask the user to
note the exact time). A fix for a fault you never reproduced is a guess.

## 3. Isolate
- **Half-splitting / divide and conquer:** pick a test that rules out half the
  remaining path (works on wired but not Wi-Fi? works for another user on the same PC?
  works in a private browser window?). Each answer halves the search space.
- **OSI order:** **bottom-up** (cable/link light › IP address › gateway ping › DNS ›
  app) when nothing works or the fault is new hardware; **top-down** (app › auth ›
  service › network) when one app fails and others are fine. Starting in the middle
  (e.g. `ping` gateway then `nslookup`) is legitimate half-splitting.
- **Known-good comparison:** compare against a working device, account, config or
  baseline image. Diff the settings, versions, group memberships, GPO/MDM results.
- **Change one variable at a time** and revert anything that made no difference.
  Shotgun changes fix things nobody can explain and break things nobody notices.

## 4. Keep a hypothesis log
In the ticket work notes, a short table per attempt:

| # | Hypothesis | Test | Expected if true | Result | Next |
|---|---|---|---|---|---|
| 1 | DNS cache stale | `ipconfig /flushdns`, retry | site loads | still fails | test DNS server |

It stops loops, lets a colleague pick up, and becomes the escalation package.

## 5. Root cause, not symptom
Restarting the spooler fixes the symptom; the bad driver is the cause. Use **5 Whys**:
"printing fails" › spooler crashed › driver faulted › auto-updated driver v2 › driver
updates not ring-tested. The last "why" is usually a process gap, and that is the
preventive measure. Stop when the answer is actionable, not literally at five.

## 6. Time-box and escalate
A typical guideline (set by your service desk, not a universal rule): at L1, if you have
no confirmed theory after roughly **15-30 minutes**, or the fix needs rights or access you
lack, escalate. Escalate immediately for security indicators, data loss risk, or
anything looking like a wider outage. Escalation must include the hypothesis log;
see computing-software.it-support-helpdesk.user-support-communication.ticket-communication-and-escalation.

## 7. Document and prevent
Record cause, fix, and how it was verified. If it could recur: raise a problem record,
write/update a KB article, propose the change (driver ring, monitoring alert, policy).

## Gotchas
- Users report their interpretation ("the internet is down") — verify the literal symptom.
- Intermittent faults: correlation in time is not causation; collect several occurrences.
- "Works on my machine" is a data point: find what differs.
- Clearing caches and rebooting destroys evidence; capture logs first when the issue is
  serious or recurring.

## Verify
- [ ] Scope and "what changed" are recorded before any fix.
- [ ] The fault was reproduced, or the reason it couldn't be is noted.
- [ ] Each change was tested alone and reverted if ineffective.
- [ ] Root cause is stated separately from the symptom fix.
- [ ] User confirmed the fix; ticket has hypothesis log and preventive action.
