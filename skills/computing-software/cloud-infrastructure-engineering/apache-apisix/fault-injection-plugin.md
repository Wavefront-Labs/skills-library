---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.fault-injection-plugin
name: fault-injection-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, fault-injection, chaos, abort, delay, percentage, plugin]
level: practitioner
status: docs-checked
description: "Inject failures into APISIX traffic with fault-injection: abort http_status, body and headers, delay duration, percentage, and AND/OR vars logic."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/fault-injection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fault-injection plugin

At least one of `abort` or `delay` is required.

`abort`:
- `http_status` (required when abort is set): integer, 200 or higher.
- `body`: supports NGINX variables. `headers`: object, values can use variables.
- `percentage`: 0-100. `vars`: lua-resty-expr rules. If both are set, both must match.

`delay`:
- `duration` (required when delay is set): seconds, decimals allowed.
- `percentage`: 0-100. `vars`: lua-resty-expr rules.

```json
"fault-injection": {
  "delay": { "duration": 2.5, "percentage": 50, "vars": [ [ ["arg_name", "==", "john"] ] ] },
  "abort": { "http_status": 503, "body": "Injected fault for $remote_addr\n", "headers": { "X-Fault": "injected" }, "percentage": 10, "vars": [ [ ["arg_region", "==", "eu"] ] ] }
}
```

Vars logic: expressions inside one inner group are ANDed; separate groups in the outer array are ORed, so `[[A, B], [C]]` means (A AND B) OR C.

The plugin executes before other configured plugins, and `abort` skips all subsequent plugins.

## Checked

2026-11-04: read the fault-injection plugin page; attributes table (abort and delay fields, http_status >= 200, percentage 0-100, duration in seconds and decimal, required-when rules), the vars AND/OR tip and the execution-order statement match. The JSON example is illustrative.

Method: documentation only; no commands were run.
