---
id: computing-software.cloud-infrastructure-engineering.keda.cooldown-period-and-initial-cooldown
name: cooldown-period-and-initial-cooldown
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [cooldownperiod, initialcooldownperiod, scale-to-zero, scale-down-delay]
level: practitioner
status: docs-checked
description: "Control how long KEDA waits after the last active trigger before scaling to zero, and add a grace window after a ScaledObject is first created."
sources:
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.cooldownPeriod` (default 300 seconds) is the wait after the last trigger reported active before KEDA scales the resource back to 0. Three details from the specification matter in practice:

- It only applies to scaling to 0. Scaling from 1 to N and back down to 1 is the HPA's job, governed by its own behaviour settings.
- It starts counting only after a trigger has been active. When you first create the workload and ScaledObject, KEDA immediately scales it to `minReplicaCount` rather than waiting.
- The effective delay also depends on `pollingInterval`, because KEDA can only notice that the queue is empty when it polls.

`spec.initialCooldownPeriod` (default 0 seconds) delays the start of that cooldown after the ScaledObject is created. With a value of 120, KEDA will not scale the resource to 0 until 120 seconds have passed since creation, regardless of trigger activity. The page presents it as a grace period for cases where scaling down immediately after creation is not desirable, and notes that this setting is independent of `pollingInterval`.

`cooldownPeriod` applies only when scaling to 0.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledObject specification: cooldownPeriod 300 and initialCooldownPeriod 0 defaults, behaviour. Removed: unsupported usage advice and a claim about minReplicaCount of 1 or more.

Method: documentation only; no commands were run.
