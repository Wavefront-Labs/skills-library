---
id: computing-software.systems-network-administration.nagios-core.host-definition
name: host-definition
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, host-definition, define-host, host-name, address, parents, max-check-attempts, check-interval, notification-options, initial-state]
level: practitioner
status: docs-checked
description: "Write a Nagios Core host object: host_name, address, parents, check_command, max_check_attempts, intervals, notification_options letters, freshness and map coordinates."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host definition

Key directives (`define host { ... }`):

- `host_name`: short name, becomes `$HOSTNAME$`. `alias`: longer text. `address`: IP or FQDN; if omitted, `host_name` is used (DNS failure breaks checks).
- `parents`: comma-separated host names; blank when on the same segment as the Nagios host. Order is irrelevant.
- `hostgroups`: alternative to hostgroup `members`.
- `check_command`: must return OK (0) for UP. Blank disables active checks (host may show PENDING).
- `initial_state`: `o`, `d`, `u` (default UP).
- `max_check_attempts`: minimum 1 even with no check command; 1 alerts without retry.
- `check_interval` / `retry_interval`: time units (minutes unless `interval_length` is changed).
- `active_checks_enabled`, `passive_checks_enabled`, `obsess_over_host`, `check_freshness`: default 1.
- `freshness_threshold`: seconds; 0 means auto.
- `notification_interval`: 0 sends one notification only. `first_notification_delay`: 0 notifies immediately.
- `notification_options`: `d`, `u`, `r`, `f`, `s`, `n`; omitted means all.
- `stalking_options`: `o,d,u` and `N` (4.4.0+).
- `importance` defaults to 0.
- Map: `statusmap_image`, `2d_coords x,y`, `3d_coords x,y,z`.

Directives marked in the docs as runtime-changeable may be read from the retention file instead of config after a change.

Example
```
define host {
    use         generic-host
    host_name   web01
    address     192.0.2.10
    parents     switch1
}
```

Self-check: `nagios -v` passes; host shows UP in the web UI.

## Checked

2026-11-04. Checked every directive, default and option letter against the Host Definition section of the object definitions page (directive list, initial_state o/d/u, max_check_attempts minimum 1, interval_length minutes, freshness_threshold 0 auto, notification_interval 0, first_notification_delay 0, notification_options d/u/r/f/s/n, stalking_options N from 4.4.0, importance default 0, statusmap_image and 2d/3d_coords). Nothing removed.

Method: documentation only; no commands were run.
