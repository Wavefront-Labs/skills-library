---
id: computing-software.systems-network-administration.icinga-2.recurring-downtimes-scheduleddowntime
name: recurring-downtimes-scheduleddowntime
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, scheduleddowntime, recurring-downtime, ranges, apply-scheduleddowntime, backup-window]
level: practitioner
status: docs-checked
description: "Create recurring Icinga 2 downtimes with apply ScheduledDowntime and ranges; only the next segment is created; HA duplicate note."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# recurring downtimes (ScheduledDowntime)
ScheduledDowntime objects set up recurring downtimes, typically through an apply rule:
```
apply ScheduledDowntime "backup-downtime" to Service {
  author = "icingaadmin"
  comment = "Scheduled downtime for backup"
  ranges = {
    monday = "02:00-03:00"
    tuesday = "02:00-03:00"
  }
  assign where "backup" in service.groups
}
```
The docs example lists all seven weekdays.

Behaviour:
- Icinga 2 finds the next possible segment from `ranges` and does not create multiple downtimes in the future. If you need all of them visible for the coming days, weeks or months, schedule them via the REST API `schedule-downtime` action from a script or cron job.
- If ScheduledDowntime objects are synced in a distributed HA setup, both nodes create the next downtime on their own. The runtime-generated downtimes are synced between the zone instances, so you may see sort-of duplicate downtimes in Icinga Web 2.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Icinga 2 Advanced Topics chapter: the Recurring Downtimes section was read in full; other sections were not. Confirmed: the apply ScheduledDowntime example with author, comment, ranges and assign where, next-segment-only behaviour with the REST API alternative, and the HA sync note about duplicate downtimes. Removed the claim that the example config ships downtimes.conf and the pointer to the Object Types chapter, neither of which this page states.
