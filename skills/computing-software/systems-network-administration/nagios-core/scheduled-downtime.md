---
id: computing-software.systems-network-administration.nagios-core.scheduled-downtime
name: scheduled-downtime
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, downtime, scheduled-downtime, fixed-downtime, flexible-downtime, triggered-downtime, maintenance-window, downtimestart]
level: practitioner
status: docs-checked
description: "Schedule Nagios Core downtime from the extinfo CGI: fixed versus flexible, triggered downtime for child objects, notification behaviour and overlapping windows."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/downtime.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled downtime

Create it in the web UI: open the host or service in `extinfo.cgi` and use "Schedule downtime". Nagios adds a comment for the window and removes it afterwards.

## Types
- **Fixed:** runs exactly from start to end time.
- **Flexible:** for outages with unknown start. Begins when the object first enters a problem state between your start and end times and lasts for the specified duration, even if it recovers sooner.
- **Triggered:** starts when another downtime entry starts; use for children of a host going down.

## Notifications
- Normal notifications are suppressed during downtime.
- DOWNTIMESTART sent at the start, DOWNTIMEEND at the end, DOWNTIMECANCELLED if cancelled early.
- Overlapping windows keep notifications suppressed until the last ends (7:30pm-9:30pm plus 9:20pm-1:30am suppresses until 1:30am).

## Macros
`$HOSTDOWNTIME$` / `$SERVICEDOWNTIME$` >0 in downtime.

## Commands
Script it with external commands (separate reference): `computing-software.systems-network-administration.nagios-core.external-commands`.

## Checked

2026-11-04. Confirmed against the Scheduled Downtime page (extinfo CGI, automatic comment, fixed, flexible and triggered behaviour, DOWNTIMESTART / DOWNTIMEEND / DOWNTIMECANCELLED notifications, overlapping windows) and the Macro list page ($HOSTDOWNTIME$ greater than zero in downtime). Removed an unconfirmed self-check.

Method: documentation only; no commands were run.
