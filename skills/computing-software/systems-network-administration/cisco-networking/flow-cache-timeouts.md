---
id: computing-software.systems-network-administration.cisco-networking.flow-cache-timeouts
name: flow-cache-timeouts
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, flexible-netflow, flow-cache-timeout, active-timeout, inactive-timeout, cache-type, netflow]
level: practitioner
status: docs-checked
description: "Read and tune Flexible NetFlow cache timeouts: defaults of 15 s inactive and 1800 s active, cache types, and the aged-flow counters in show output."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fnetflow/configuration/xe-16/fnf-xe-16-book/fnf-fnetflow.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow cache timeouts

## What the Cisco guide states
- The default cache type is `normal`: entries are aged out according to the `timeout active` and `timeout inactive`
  settings. An aged-out entry is removed from the cache and exported through any configured exporters.
- Default values in the guide's `show flow monitor` output: Inactive Timeout 15 secs, Active Timeout 1800 secs
  (the output also lists an Update Timeout of 1800 secs).
- A `permanent` cache type exists (the guide shows `cache type permanent` with `cache entries` in an example).
- Timeouts are set in flow monitor configuration mode with `cache timeout active <seconds>` (the guide's step is
  `cache {timeout {active} seconds | {normal}`; take the full inactive/update syntax from the command reference for
  your release).
- To modify the `record` of a flow monitor, first remove the monitor from all interfaces with `no ip flow monitor`.

## Reading the cache
`show flow monitor name <monitor> cache format record` shows the cache type, Current entries, High Watermark,
Flows added, and Flows aged, broken down as Active timeout, Inactive timeout, Event aged, Watermark aged and Emergency
aged. Use the breakdown to see which mechanism is removing flows.

## Collector side
Flexible NetFlow exports records using the template-based Version 9 format. Choose timeouts with your collector's
aggregation interval in mind, and check the collector's documentation for the values it expects.

## Checked
Checked 2026-11-08 against the Cisco Flexible NetFlow configuration guide (cache type, flow monitor modification
steps, `show flow monitor` examples). Removed: RFC 7011 as a source (it does not define these timers), the TCP
FIN/RST immediate-export claim, `immediate` cache type, cache sizing byte estimates, 60 s tuning advice, and the
full configuration example, which the guide does not state.
Method: documentation only; no commands were run.
