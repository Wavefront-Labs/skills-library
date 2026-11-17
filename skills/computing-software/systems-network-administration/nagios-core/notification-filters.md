---
id: computing-software.systems-network-administration.nagios-core.notification-filters
name: notification-filters
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, notifications, notification-filters, notification-interval, notification-period, enable-notifications, minimum-importance, why-no-notification]
level: practitioner
status: docs-checked
description: "Why a Nagios Core notification was or was not sent: the ordered program, host/service and contact filters, and when notifications fire."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/notifications.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notification logic

## When
Only when a check result is processed, never on elapsed time alone: on a HARD state change, or while in a hard non-OK state once `notification_interval` has passed. Services get no notifications while their host is in a problem state.

## Filters, in order
1. **Program-wide:** `enable_notifications` must be on.
2. **Host/service:**
   - scheduled downtime (service notices also suppressed during host downtime)
   - flapping
   - `notification_options` (service w/u/c/r; host d/u/r). Recovery notices only follow a sent problem notice
   - `notification_period` (non-OK notices reschedule to next valid time)
   - `notification_interval` (applies only if already notified and state unchanged)
3. **Per contact** (each evaluated independently):
   - the contact's notification options
   - importance: service importance must be >= the contact's `minimum_importance`; for hosts, host importance plus its services' (both default 0)
   - the contact's notification period

## Recipients
Contacts of the object's `contact_groups`; duplicates removed.

Escalations: `computing-software.systems-network-administration.nagios-core.notification-escalations`.

Debug: set `debug_level` bit 32 for notifications.

## Checked

2026-11-04. Confirmed on the Notifications page: notifications are evaluated only when a check result is processed, hard state change or interval elapsed in a hard non-OK state, service notices suppressed when the host is non-OK, the filter order (program-wide, downtime, flapping, options, period with rescheduling, interval) and per-contact filters (options, importance vs minimum_importance with host plus services, period), duplicates removed. Debug bit 32 for notifications confirmed on the main configuration page. Nothing removed.

Method: documentation only; no commands were run.
