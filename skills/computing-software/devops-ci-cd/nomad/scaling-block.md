---
id: computing-software.devops-ci-cd.nomad.scaling-block
name: scaling-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, scaling-block, scaling, autoscaler, horizontal-scaling, dynamic-application-sizing, min-max, policy, hcl]
level: practitioner
status: docs-checked
description: "Declare Nomad scaling policies for external autoscalers with the scaling block at group level for count or at task level for cpu and mem, with min, max, enabled and policy."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/scaling.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad scaling block

`scaling` publishes bounds and a policy for external autoscalers (the Nomad Autoscaler) and for scaling from the UI. Not supported in `system` jobs.

## Group level - horizontal scaling
Controls the group `count`.
```hcl
group "cache" {
  count = 1
  scaling {
    enabled = true
    min     = 0
    max     = 10
    policy {
      # autoscaler-specific
    }
  }
}
```

## Task level - Dynamic Application Sizing
Controls task `resources`. The block takes a label naming the resource, `cpu` or `mem`.
```hcl
task "redis" {
  resources { cpu = 100 memory = 256 }
  scaling "cpu" {
    enabled = true
    min     = 100
    max     = 500
    policy {}
  }
  scaling "mem" {
    enabled = true
    min     = 64
    max     = 512
    policy {}
  }
}
```

## Parameters
- `max` (required) - upper bound; honoured by the autoscaler and by Nomad itself during job updates and scale operations.
- `min` - lower bound; defaults to the group `count`; also enforced by Nomad.
- `enabled` (`false`) - lets you pause a policy; the autoscaler must honour it. Note the default is false, so a policy does nothing until set to true.
- `policy` - opaque to Nomad, parsed only by the autoscaler; see that project's policy docs for contents.

## Checked

2026-11-03. Confirmed against the scaling job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: the pointer to `nomad job scale` and `nomad scaling policy list` (commands pages not read).

Method: documentation only; no commands were run.
