---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-batching-parameters
name: karpenter-batching-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [batching, batch-idle-duration, batch-max-duration, provisioning, pending-pods, tuning]
level: advanced
status: docs-checked
description: "Tuning pod batching with BATCH_IDLE_DURATION (default 1s) and BATCH_MAX_DURATION (default 10s): trade-off between launch speed and fewer larger nodes, and when to change them."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/settings.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter batching parameters

Karpenter batches pending pods into a window before computing nodes. Two settings (environment variable and CLI flag):

| Setting | Flag | Default |
|---|---|---|
| `BATCH_IDLE_DURATION` | `--batch-idle-duration` | `1s` |
| `BATCH_MAX_DURATION` | `--batch-max-duration` | `10s` |

- Idle duration: the longest gap with no new pending pod before the window ends. Each new pod arriving within this gap extends the window, up to the max duration. Pods arriving slower than the idle duration land in separate batches.
- Max duration: the cap on a batching window. Longer windows gather more pods, usually giving fewer but larger nodes, at the cost of delay from the first pending pod.

Values are Go duration strings such as `10s`, `1m`, `2h45m` (units `ns`, `us`, `ms`, `s`, `m`, `h`).

Trade-off: lowering the values makes pod-to-node launch slightly faster but yields smaller nodes; raising them does the opposite.

When to change: for ordinary Deployment scale-ups pods arrive at the kube-controller-manager QPS and the defaults are fine. Tune only when other systems create many pods over many seconds or minutes and you want them batched together.

## Checked

2026-11-04. Confirmed against the Settings reference (v1.13) (identifiers, defaults, limits and prose). Removed invented example values (5s / 60s).

Method: documentation only; no commands were run.
