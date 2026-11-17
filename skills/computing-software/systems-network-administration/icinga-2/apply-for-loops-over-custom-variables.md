---
id: computing-software.systems-network-administration.icinga-2.apply-for-loops-over-custom-variables
name: apply-for-loops-over-custom-variables
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, apply-for, dictionary-iteration, snmp-oid, vars, service-generation]
level: advanced
status: docs-checked
description: Generate Icinga 2 services by iterating a dictionary custom variable with apply for, using key and value and ignore where filters.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apply for loops over custom variables
`apply for` creates one object per element of an array or dictionary custom variable.

Host with a dictionary of SNMP OIDs:
```
object Host "router-v6" {
  check_command = "hostalive"
  address6 = "2001:db8:1234::42"
  vars.oids["if01"] = "1.1.1.1.1"
  vars.oids["temp"] = "1.1.1.1.2"
  vars.oids["bgp"] = "1.1.1.1.5"
}
apply Service for (identifier => oid in host.vars.oids) {
  check_command = "snmp"
  display_name = identifier
  vars.snmp_oid = oid
  ignore where identifier == "bgp"
}
```
The rule is evaluated for every object that has `oids` set, so no `assign where` for the existence check is needed. The loop variable can be used in `assign`/`ignore where` (for example `ignore where regex(..., oid)`).

To iterate with `key => value`, the custom variable must be a dictionary. A value that is itself a dictionary can be merged into the service vars with `vars += config`, as in `apply Service for (customer => config in host.vars.hosting)`. This moves attribute specification from the service to the host, saving multiple apply rules.

For interface-style services, put a per-interface nested dictionary on the host and build `display_name`, notes and URLs dynamically inside the rule. Define the SNMP community as a global constant in constants.conf.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Using Apply For Rules, Apply For and Custom Variable Override and Use Object Attributes in Apply Rules sections of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page). Confirmed the SNMP OID example, evaluation for every object with the variable, the ignore where and regex options, the key => value dictionary requirement, vars += config, the interface example and the constants.conf tip. Replaced the loose phrase shared secrets with the page's wording. No commands were run.
