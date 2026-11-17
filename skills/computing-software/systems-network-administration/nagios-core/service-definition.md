---
id: computing-software.systems-network-administration.nagios-core.service-definition
name: service-definition
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, service-definition, define-service, service-description, check-command, hostgroup-name, notification-options, flap-detection-options, is-volatile]
level: practitioner
status: docs-checked
description: "Write a Nagios Core service object: host_name or hostgroup_name, service_description, check_command, intervals, notification and flap options, URLs."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service definition

Typical required set (per the page's example): `host_name` (or `hostgroup_name`), `service_description`, `check_command`, `max_check_attempts`, `check_interval`, `retry_interval`, `check_period`, `notification_interval`, `notification_period`, `notification_options`, `contact_groups`.

## Notes
- `service_description` may contain spaces, dashes, colons; avoid semicolons, apostrophes, quotes. Must be unique per host.
- `host_name` accepts comma lists; `hostgroup_name` may be used instead of or in addition.
- `check_command` runtime is capped by `service_check_timeout`; `event_handler` by `event_handler_timeout`.
- `initial_state`: `o`,`w`,`u`,`c` (default OK).
- `is_volatile` 0/1 (see volatile services skill).
- `active_checks_enabled`, `passive_checks_enabled`, `obsess_over_service`, `check_freshness` default to 1; `freshness_threshold` 0 = auto.
- `notification_options`: `w,u,c,r,f,s,n`; omitted = all. `notification_interval` 0 = one notification.
- `stalking_options`: `o,w,u,c,N`.
- `flap_detection_options`: `o,w,c,u`; `low_flap_threshold`/`high_flap_threshold` 0 = use global.
- Presentation: `display_name` (defaults to description), `notes`, `notes_url`, `action_url`, `icon_image`.
- `servicegroups` as alternative to group `members`.

```
define service {
    use                   generic-service
    host_name             web01
    service_description   HTTP
    check_command         check_http
}
```

## Checked

2026-11-04. Confirmed against the Service Definition section of the object definitions page: directive list, service_description rules, host_name and hostgroup_name lists, initial_state o/w/u/c, is_volatile, the default of 1 for active/passive checks, obsess and freshness, freshness_threshold 0 auto, notification_options w/u/c/r/f/s/n, notification_interval 0, stalking_options with N, flap options and thresholds, display_name default, servicegroups. Removed the claim that contacts and notification period are inherited from the host, which the page does not state.

Method: documentation only; no commands were run.
