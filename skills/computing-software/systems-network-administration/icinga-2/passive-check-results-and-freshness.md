---
id: computing-software.systems-network-administration.icinga-2.passive-check-results-and-freshness
name: passive-check-results-and-freshness
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, passive-checks, process-check-result, freshness, dummy, check-source, ttl]
level: practitioner
status: docs-checked
description: "Feed passive check results into Icinga 2 with process-check-result and use freshness checks with a dummy command to flag stale results."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# passive check results and freshness
Hosts or services that do not run a plugin themselves receive "passive" or external check results from a client or script. Transport methods: the `process-check-result` REST API action (remote and local) or an external command via the command pipe (local only). The API action accepts `check_source` to identify the sender, visible in Icinga Web 2 and API queries.

Each received result updates the next expected check time. If none arrives, Icinga 2 runs a freshness check.

**Freshness** is enabled by default for active checks and based on `check_interval`:
- active: (last check execution time + check interval) > current time
- external source: (last result time + check interval) > current time

`process-check-result` can overrule the interval with a TTL (docs: v2.9+). On failure Icinga runs the defined check command unless active checks are disabled. Best practice is a `dummy` check command:
```
apply Service "external-check" {
  check_command = "dummy"
  check_interval = 1m
  vars.dummy_state = 3
  vars.dummy_text = {{
    var service = get_service(macro("$host.name$"), macro("$service.name$"))
    var lastCheck = DateTime(service.last_check).to_string()
    return "No check results received. Last result time: " + lastCheck
  }}
  assign where "external" in host.vars.services
}
```
`vars.dummy_state = 3` sets UNKNOWN when freshness fails.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Icinga 2 Advanced Topics chapter: the External Passive Check Results and Check Result Freshness sections were read in full; other sections were not. Confirmed: process-check-result API action (remote and local) versus the command pipe (local only), check_source, next expected check time updates, both freshness formulas, TTL override from v2.9, running the check command on freshness failure unless active checks are disabled, and the dummy check command example with dummy_state 3.
