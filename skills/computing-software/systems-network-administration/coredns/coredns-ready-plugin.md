---
id: computing-software.systems-network-administration.coredns.coredns-ready-plugin
name: coredns-ready-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, ready, readiness, kubernetes, endpoint]
level: practitioner
status: docs-checked
description: "Expose the /ready endpoint that returns 503 until every readiness-aware plugin is ready, with until-ready or continuously monitoring."
sources:
  - https://coredns.io/plugins/ready/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: gate traffic on all plugins reporting readiness.

Syntax:

```
ready [ADDRESS] {
    monitor until-ready|continuously
}
```

Behaviour:
- An HTTP endpoint on port 8181 (the default address is `:8181`, path fixed to `/ready`) returns 200 and OK when every plugin that can signal readiness has done so. Otherwise it returns 503 with a body listing the plugins that are not ready.
- Each server block that enables ready adds its plugins to the same `/ready` endpoint on that port. The same plugin configured differently in several blocks is reported as the union of their readiness.
- `monitor until-ready` is the default: once a plugin signals ready it is never checked again, which assumes stability after the first confirmation.
- `monitor continuously` keeps checking, so a plugin may move between ready and not ready.
- A plugin takes part by implementing `Ready() bool` in the ready.Readiness interface. Plugins that do not implement it are not waited on.
- Example: with `ready` in both the `.` and `example.org` blocks, both blocks' plugins report to the one endpoint. A different address such as `ready localhost:8091` moves it to another port.

## Checked

2026-11-08. Checked in full against the ready plugin README. Removed unsupported claims about the kubernetes plugin's readiness and about lame duck mode (those belong to other pages); added the multi-block and alternate-address examples.

Method: documentation only; no commands were run.
