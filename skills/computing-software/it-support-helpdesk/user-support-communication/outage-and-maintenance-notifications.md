---
id: computing-software.it-support-helpdesk.user-support-communication.outage-and-maintenance-notifications
name: outage-and-maintenance-notifications
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, written-communication, outage-notification, maintenance-notice, status-page, major-incident-communication, ivr-message, service-restoration-notice, status-updates]
level: practitioner
status: draft
description: "Write outage and planned maintenance notices: who is affected, impact in user terms, workaround, next update time, channels (status page, banner, IVR) and the all-clear."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.atlassian.com/incident-management/incident-communication"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# outage-and-maintenance-notifications

Goal: users hear about an outage from IT before they call, know what to do
meanwhile, and get told when it's over.

## Outage notice template
> **[Investigating] Email delays for some staff — 09:40**
> **Who's affected:** staff using Outlook on laptops and phones. Teams is
> working normally.
> **What you'll notice:** new emails may arrive up to 30 minutes late.
> Sending works.
> **What to do:** nothing — mail is queued, not lost. For urgent messages,
> use Teams chat.
> **Next update:** by 10:15, or sooner if fixed.
States: Investigating → Identified → Monitoring → Resolved.

## Rules
- First notice fast (target ≤ 15 minutes after a major incident is
  declared) even if the cause is unknown — say so.
- Impact in **user terms** (what they can't do), not component names
  ("Exchange hybrid connector").
- Always give a **next update time** and meet it, even with "no change".
- No blame, no speculation on cause until known; no security details
  during a security incident (coordinate with security/comms).
- One source of truth (status page or intranet), others link to it:
  service desk portal banner, IVR pre-recorded message, Teams/Slack
  announcement channel, email for long outages. Agents get the same text
  to read out.

## Planned maintenance
- Notice lead time per change policy (e.g. 5 business days; 24 h for
  minor).
- What/when (with time zone)/duration/impact/what users must do (save work,
  restart laptop, expect sign-out).
- Reminder shortly before; completion notice after.
> **Planned: VPN maintenance Saturday 12 Oct 22:00–23:30 BST.** VPN will
> disconnect for up to 15 minutes during this window. Office Wi-Fi is not
> affected. Nothing to do beforehand.

## Resolution notice
What was affected, when it was restored, whether users need to do anything
(restart Outlook), how to report lingering issues, and (later) a brief
cause summary for significant incidents.

## Gotchas
- Silent resolution makes users keep calling — always send the all-clear.
- Too many notices for minor blips trains people to ignore them; set
  thresholds (number of users/critical services).

## Verify
After each major incident: time from declaration to first notice, updates
on schedule, call volume drop after the banner — review in the PIR.
