---
id: computing-software.devops-ci-cd.nomad.check-restart-block
name: check-restart-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, check-restart, check-restart-block, limit, grace, ignore-warnings, service-health, unhealthy, restart-policy, hcl]
level: practitioner
status: docs-checked
description: "Restart Nomad tasks on failing service checks with check_restart limit, grace and ignore_warnings, including consecutive-failure counting and hand-off to the restart policy."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/check_restart.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad check_restart block

`check_restart` makes Nomad restart a task whose service health check stays unhealthy. It sits in a `check` or directly in a `service` (applies to all its checks); when both exist they merge with the check's values winning. The restart itself is governed by the group's `restart` policy (`computing-software.devops-ci-cd.nomad.restart-block`).

```hcl
check {
  type     = "script"
  name     = "check_table"
  command  = "/usr/local/bin/check_mysql_table_status"
  args     = ["--verbose"]
  interval = "60s"
  timeout  = "5s"

  check_restart {
    limit           = 3
    grace           = "90s"
    ignore_warnings = false
  }
}
```

## Parameters (defaults)
- `limit` (`0`) - restart after this many failures; `1` restarts on the first. `0` disables check-based restarts. Failures must be **consecutive**; one pass resets the count, so a flapping service may never be restarted.
- `grace` (`"1s"`) - wait after start or restart before checking health, so slow starters are not killed.
- `ignore_warnings` (`false`) - treat `warning` as passing. Only available with the Consul service provider.

## Timeline for the example
Nothing is checked for 90s after start. After that a failing script check (interval 60s) has `60s x 3 = 180s` to pass before a restart is triggered. Then the `restart` block applies (`delay = "10s"` between stop and start), the grace period starts again, and after `attempts` restarts within `interval` the `mode` decides (`fail` stops restarting).

## Gotcha
Restarts caused by this block count against the same `restart` attempts, so a permanently failing check ends in a failed allocation and, depending on `reschedule`, a new placement.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 check_restart job specification page: limit, grace and ignore_warnings defaults, consecutive-failure rule, merge of service and check blocks, the 90s grace and 180s (60s x 3) timeline, hand-off to the restart policy. Nothing removed.

Method: documentation only; no commands were run.
