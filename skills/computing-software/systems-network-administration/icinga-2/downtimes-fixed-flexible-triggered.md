---
id: computing-software.systems-network-administration.icinga-2.downtimes-fixed-flexible-triggered
name: downtimes-fixed-flexible-triggered
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, downtime, fixed-downtime, flexible-downtime, triggered-downtime, schedule-downtime, maintenance]
level: practitioner
status: docs-checked
description: "Schedule Icinga 2 downtimes via Icinga Web or schedule-downtime: fixed vs flexible windows, triggered downtimes, overlap behaviour."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# downtimes: fixed, flexible, triggered
Downtimes cover planned maintenance. They suppress notifications, can trigger other downtimes, and can be cancelled manually. Schedule them in Icinga Web (select several objects with shift) or with the API action `schedule-downtime`, for example from a backup script or a cron job.

Multiple downtimes on one object may overlap, which helps when maintenance overruns; the downtime depth then exceeds 1. If a downtime is scheduled after a critical hard state already sent a problem notification and the service recovers during the window, the recovery notification is not suppressed. Planned downtimes count in SLA reports built from state and downtime history.

**Fixed**: active from start to end time. When the object changes to NOT-OK inside that window the downtime is "in effect" and the depth counter rises. Example: a known 23:00 to 24:00 window.

**Flexible**: a window (start to end) in which a NOT-OK state change triggers the downtime, which then lasts for the given duration in minutes. It ends at trigger time plus duration, which may be after the window end. Example: window 07:30-08:00, duration 15 minutes.

**Triggered**: optional. A downtime can be triggered by an already scheduled downtime, for instance a child host downtime triggered by the parent's downtime on NOT-OK.

**Recurring**: use ScheduledDowntime objects (separate skill).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Icinga 2 Advanced Topics chapter: the Downtimes section (scheduling, fixed and flexible, triggered, recurring pointer) was read in full; other sections were not. Confirmed: Icinga Web multi-select with shift, schedule-downtime API action, overlap and downtime depth, recovery notification not suppressed when scheduled after the problem notification, SLA reporting, fixed 23:00 to 24:00 example, flexible 07:30-08:00 with 15 minutes example, trigger time plus duration, and triggered child downtimes.
