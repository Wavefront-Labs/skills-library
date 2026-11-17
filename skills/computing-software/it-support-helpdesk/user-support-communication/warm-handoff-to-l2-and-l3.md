---
id: computing-software.it-support-helpdesk.user-support-communication.warm-handoff-to-l2-and-l3
name: warm-handoff-to-l2-and-l3
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, escalation, warm-handoff, warm-transfer, escalation-package, cold-transfer, call-transfer, l2, l3]
level: practitioner
status: draft
description: "Hand over to L2/L3 without the user repeating themselves: the escalation package, warm transfers on calls and chats, confirming acceptance, and next steps."
sources:
  - "https://www.thinkhdi.com/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# warm-handoff-to-l2-and-l3

Goal: the next person can start working within a minute of receiving the
ticket, and the user never hears "can you explain the problem again?".

## Escalation package (in the ticket, before handing over)
1. **Problem statement**: what's failing, exact error text, since when.
2. **Scope/impact**: one user or many, business impact, deadline.
3. **Environment**: device/asset, OS build, app version, location/network
   (VPN, office), user's role.
4. **What was tried** with **results** (not just "rebooted"): "Cleared
   Teams cache — no change; works on web — yes; works for colleague on same
   desk — yes".
5. **Evidence**: screenshots, log excerpts, event IDs, timestamps of
   repro.
6. **Hypothesis** (if any) and why.
7. **User availability** and preferred contact.

## Warm transfer on a call
1. Ask the user's permission to put them on hold.
2. Call/chat the L2 engineer, summarise in 30 seconds using the package,
   confirm they'll take it.
3. Introduce: "Alex, I have Sam from Finance, Outlook crashes on opening
   shared calendars since this morning; I've tried X and Y." Then drop off
   (or stay briefly).
Cold transfer (no introduction) only when the team's process says so and
the ticket has the package.

## Chat and ticket handoffs
- Assign the ticket to the group/person and @mention in the team channel
  for urgent ones.
- Confirm acceptance (assigned to a person, or acknowledgement) for P1/P2 —
  don't assume.

## Tell the user
Who has it, what they'll do next, expected contact time, ticket number.
Keep owning updates if your desk owns the incident lifecycle.

## Gotchas
- Escalating with "please investigate" and no package gets it bounced back.
- Don't promise L2's timeline unless their OLA supports it.

## Verify
L2 doesn't need to re-contact the user for basic facts (QA sample), and
user CSAT comments don't mention repeating themselves.
