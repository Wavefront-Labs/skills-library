---
id: computing-software.systems-network-administration.nagios-core.wildcards-and-exclusion
name: wildcards-and-exclusion
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, wildcards, exclusion, object-tricks, hostgroup-name, comma-lists, servicegroup-name, bang-exclude]
level: advanced
status: docs-checked
description: "Nagios Core object-definition shortcuts: comma lists, * wildcards for hosts and services, ! exclusion, and same-host dependency and escalation patterns."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objecttricks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time-saving patterns

## Lists and wildcards
The page's examples require `use_regexp_matching` to be disabled.
- Comma lists work in `host_name`, `hostgroup_name`, `service_description`, `servicegroup_name`.
- `host_name *` = all hosts. `members *` in a hostgroup = all hosts. `service_description *` = all services on the host(s). Both `*` = every service.

## Exclusion with `!`
```
host_name      HOST1,HOST2,!HOST3
hostgroup_name HG1,!HG3
```
Works for services, service escalations, host escalations; dependencies use `dependent_service_description *,!SERVICE1`.

## Services
List hosts, use `hostgroup_name`, or `host_name *`, with `!` to exclude.

## Escalations
Same patterns; `servicegroup_name` selects all services in groups.

## Dependencies
- Host/hostgroup lists on both sides (`host_name`/`dependent_host_name`, hostgroup equivalents).
- Same-host dependency: leave `dependent_host_name` and `dependent_hostgroup_name` empty.
- Master-service wildcard pattern: master (e.g. an agent version check) with `dependent_service_description *,!SERVICE1` so the master does not depend on itself.
- Servicegroups: `servicegroup_name` / `dependent_servicegroup_name`.

Regex alternative: `computing-software.systems-network-administration.nagios-core.regexp-matching`.

## Checked

2026-11-04. Confirmed against the Object Tricks page: supported object types, comma lists, * wildcards, ! exclusion, same-host dependencies with empty dependent_host_name, the NCPA agent_version wildcard pattern with *,!SERVICE1, servicegroup forms, and the use_regexp_matching requirement.

Method: documentation only; no commands were run.
