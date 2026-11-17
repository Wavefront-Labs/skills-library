---
id: computing-software.systems-network-administration.icinga-2.library-functions-match-regex-cidr-and-accessors
name: library-functions-match-regex-cidr-and-accessors
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, library-reference, match, regex, cidr-match, get-objects, macro, parse-performance-data]
level: practitioner
status: docs-checked
description: Use Icinga 2 library functions in assign where and lambdas - match, regex, cidr_match with MatchAll or MatchAny, macro(), get_objects, get_service, parse_performance_data.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/18-library-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library functions
**match(pattern, value, mode):** wildcard (`?` and `*`) match against a string or an array of strings. `mode` is `MatchAll` (default; every element must match) or `MatchAny`.
```
match("*prod-sfo*", "db-prod-sfo-657")   // true
match("web-*", host.vars.application_types, MatchAny)
```
**regex(pattern, value, mode):** regular expression, same value types and modes. Escape backslashes: `regex("^db-prod\\d+", host.vars.databases, MatchAny)`.

**cidr_match(pattern, ip, mode):** `cidr_match("192.168.56.0/24", host.address)`. IPv4 addresses are converted to IPv4-mapped IPv6 before matching; same `mode` argument.

**macro("$name$"):** resolves a runtime macro inside runtime-evaluated functions only, such as custom variables using the `{{ ... }}` syntax:
```
vars.snmp_address = {{
  var addr_v4 = macro("$address$")
  if (addr_v4) { return addr_v4 } else { return "udp6:[" + macro("$address6$") + "]" }
}}
```
**Object accessors:** `get_objects(Type)` returns all objects of a type object; `get_service(host_name, service_name)` returns the Service or `null`; related getters exist such as `get_host`, `get_host_group`, `get_user`, `get_time_period`, `get_template`, `get_templates`.

**parse_performance_data("'time'=1480074205.197363;;;")** returns a PerfdataValue with label, value, unit, warn, crit, min, max and counter.

Other globals include `len`, `keys`, `union`, `intersection`, `range`, `glob`, `path_exists`, `getenv`, `get_time`, `log`, `typeof`, plus `Json.encode`/`Json.decode` and `Math`.

## Checked

2026-11-04. Confirmed against the Icinga 2 library reference: match, regex, cidr_match with MatchAll default and MatchAny, IPv4-mapped IPv6, macro(), get_objects, get_service, get_template, parse_performance_data. Corrected the regex example to the documented double backslash.

Method: documentation only; no commands were run.
