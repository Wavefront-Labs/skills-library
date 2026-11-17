---
id: computing-software.systems-network-administration.icinga-2.troubleshooting-checks-late-results-and-notifications
name: troubleshooting-checks-late-results-and-notifications
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, troubleshooting, checks-not-executed, late-check-results, notifications-not-sent, check-source]
level: practitioner
status: docs-checked
description: Diagnose Icinga 2 checks that do not run, find the executed command, late results via the console, wrong thresholds on agents, and notifications not sent.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting checks and notifications
**Executed command:** query `last_check_result` (field `command`) via the API, via `icinga2 console --connect ... --eval 'get_service("host", "http").last_check_result.command'`, or `grep "notice/Process"` in the debug log.

**Checks not executed:** decide whether execution is local or remote (move analysis to the satellite); check the debug log; check dependencies are not blocking; confirm the plugin is executable by the Icinga user; confirm the `checker` feature is enabled. Test plugins as the daemon user (for example `sudo -u icinga`), never root: environment and permissions differ and the daemon reads no `.bashrc`.

**Check source:** the `check_source` attribute shows where a check actually ran.

**Wrong thresholds with command endpoints:** an agent that keeps `conf.d` and the `checker` feature runs its own default `disk` service and sends those results back. Disable `checker` on the agent and remove the `conf.d` include.

**Late results:** from `icinga2 console`, filter `get_objects(Service)` for `s.last_check < get_time() - 2 * s.check_interval`. In HA zones group the result by `s.paused`; non-inverted counts across two nodes hint at split-brain.

**Notifications not sent:** check the debug log; `enable_notifications`; Notification and User `states`, `types`, `period`; `begin`/`end` times; the `notification` feature; that the NotificationCommand (and mail program) runs as the Icinga user. Live stream: POST to `/v1/events` with `types=Notification` and a `queue` name.

## Checked

2026-11-04. Confirmed against the Icinga 2 troubleshooting chapter: late result console query, paused attribute, check_source, command endpoint checker advice. Corrected the event stream call to the documented POST with a queue parameter.

Method: documentation only; no commands were run.
