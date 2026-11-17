---
id: computing-software.cloud-infrastructure-engineering.netdata.alert-precedence-ordering
name: alert-precedence-ordering
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, alert-precedence, file-shadowing, health-config]
level: advanced
status: docs-checked
description: "Predict which Netdata alert definition wins: user alarm over stock alarm over user template over stock template, same-name rules and file shadowing."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/alert-configuration-ordering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alert files load from the user `health.d/` first, then stock. Precedence, highest first:
1. Alarm, user config
2. Alarm, stock config
3. Template, user config
4. Template, stock config

Rules:
- Precedence applies only between alerts with the same name; different names coexist.
- One alert per (instance, alert name): the first matching definition wins and later same-name ones are skipped for that instance.
- A file with the same filename in both directories shadows the stock one entirely; only the user file loads.
- A malformed static rule is logged and skipped; valid same-name rules stay.
- UI or API changes replace any same-name definition, the only case of overwrite.
- Keep all definitions for one alert name in one file; load order within a directory depends on the filesystem.

Example: stock template `disk_space_usage` on `disk.space` (warn below 20) plus a user alarm of the same name on `disk_space._mnt_data` (warn below 5). Result: `/mnt/data` warns at 5, other disks at 20.

Apply with `sudo netdatacli reload-health`. Verify the `source` field in `curl -s "http://localhost:19999/api/v1/alarms?all"`, and check `/var/log/netdata/error.log` for errors.

## Checked

2026-11-04: precedence order, same-name rule, first-match-wins, file shadowing, malformed-rule handling, dynamic configuration exception, load order within a directory, the disk_space_usage example and the alarms API check confirmed against the Netdata alert-configuration-ordering page.

Method: documentation only; no commands were run.
