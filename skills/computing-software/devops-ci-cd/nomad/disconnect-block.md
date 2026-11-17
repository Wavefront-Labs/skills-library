---
id: computing-software.devops-ci-cd.nomad.disconnect-block
name: disconnect-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, disconnect-block, disconnect, lost-after, stop-on-client-after, replace, reconcile, heartbeat-grace, network-partition, edge, unknown-allocations, hcl]
level: advanced
status: docs-checked
description: "Control Nomad behaviour in client network partitions with the disconnect block: lost_after, stop_on_client_after, replace and reconcile strategies."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/disconnect.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad disconnect block

`disconnect` (group level) defines what happens when a node misses heartbeats. Without it the allocation is marked `lost` and replaced. It only governs lost or disconnected nodes: drained nodes use `migrate`, and task failures use `restart` then `reschedule`.

```hcl
group "example" {
  disconnect {
    lost_after = "6h"
    replace    = false
    reconcile  = "keep_original"
  }
}
```

## Parameters
- `lost_after` - how long a disconnected client keeps its allocations before they become lost, counted after the server's `heartbeat_grace`. Default `""` equals no block.
- `stop_on_client_after` - the client stops its own allocations after this long without server contact (the Nomad client process must be running). You **cannot combine** it with `lost_after`. Setting it shorter than `lost_after` with `replace = false` is a validation error.
- `replace` (`true`) - schedule a replacement elsewhere immediately (counts as a reschedule and obeys `reschedule`). If `false`, the allocation is reported `unknown` until the node returns or you run `nomad alloc stop <alloc ID>`.
- `reconcile` (`"best_score"`) - which allocation survives when the node returns: `keep_original` (may have crashed meanwhile), `keep_replacement`, `best_score`, `longest_running`.

## lost_after semantics
With `lost_after`, the server marks a silent client `disconnected` (not `down`) and its allocations `unknown` (not `lost`), so they can reconnect without restarting; replacements are scheduled per `replace`. After reconnection the `reconcile` strategy picks winners. If the duration expires first, allocations become `lost` and the node `down`. A client stays `disconnected` until the longest `lost_after` among its groups elapses. Fits edge sites and stateful tasks with slow restarts. Example server setting: `heartbeat_grace = "2m"` in the `server` block.

## stop_on_client_after example
`stop_on_client_after = "90s"` with the default 10 second `heartbeat_grace`: the server replaces the allocation after 90 more seconds, the client sends `SIGTERM` after 90s and `SIGKILL` after the task's `kill_timeout` (15s in the example). A group without it is replaced after the grace period but never stopped on the client.

## Risks
- Keep server clocks closely synchronised, or the server may replace a group before the client has stopped it.
- A group using `stop_on_client_after` is also stopped if the whole server cluster fails, since the client cannot reach any server.

## Checked

2026-11-03. Confirmed against the disconnect job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
