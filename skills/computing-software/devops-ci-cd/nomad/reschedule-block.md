---
id: computing-software.devops-ci-cd.nomad.reschedule-block
name: reschedule-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, reschedule-policy, reschedule, delay-function, exponential, fibonacci, max-delay, unlimited, failed-allocations, hcl]
level: practitioner
status: docs-checked
description: "Tune the Nomad reschedule block with attempts, interval, delay, delay_function constant exponential or fibonacci, max_delay, unlimited and the service and batch defaults."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/reschedule.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad reschedule block (reschedule-policy)

`reschedule` defines what happens after local restarts are used up: Nomad creates a replacement allocation, preferring a node that did not host a previous attempt. It also fires when the agent fails to set up the allocation. It is valid at `job` and `group` level; if both exist they merge, group wins over job. It does **not** apply to `system` or `sysbatch` jobs (they run on every node).

Drained nodes use `migrate` and lost nodes use the disconnect/replace behaviour; both ignore `reschedule`.

```hcl
reschedule {
  attempts       = 15
  interval       = "1h"
  delay          = "30s"
  delay_function = "exponential"
  max_delay      = "120s"
  unlimited      = false
}
```

## Parameters
- `attempts` / `interval` - allowed attempts within a sliding window that starts at the first reschedule attempt; beyond it Nomad stops rescheduling.
- `delay` - wait before rescheduling; cannot be less than 5 seconds.
- `delay_function` - `constant` (always `delay`), `exponential` (doubles each time), `fibonacci` (sum of the two latest delays; from 5s: 5s, 5s, 10s, 15s, 25s).
- `max_delay` - cap on growth, used only with exponential or fibonacci.
- `unlimited` - when `true`, `attempts` and `interval` are ignored. The update block's `progress_deadline` is still honoured, so no further attempts occur once it is reached.

## Defaults
- Batch: `attempts = 1`, `interval = "24h"`, `unlimited = false`, `delay = "5s"`, `delay_function = "constant"`.
- Service: `delay = "30s"`, `delay_function = "exponential"`, `max_delay = "1h"`, `unlimited = true`.

## Disable
```hcl
reschedule {
  attempts  = 0
  unlimited = false
}
```

## Notes
Reschedule history is visible in the CLI and API for the allocation. Pair this block with `restart` (`computing-software.devops-ci-cd.nomad.restart-block`): restart with `mode = "fail"` is what pushes a failing task into rescheduling.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 reschedule job specification page: job and group merge, system and sysbatch exclusion, delay minimum 5s, delay functions including the fibonacci sequence, max_delay, unlimited and progress_deadline, batch and service defaults, disabling. Nothing removed.

Method: documentation only; no commands were run.
