---
id: computing-software.devops-ci-cd.flagger.flagger-canary-finalizers-and-suspend
name: flagger-canary-finalizers-and-suspend
category: computing-software
field: devops-ci-cd
product: flagger
tags: [canary, finalizer, suspend, revertondeletion, skipanalysis]
level: advanced
status: docs-checked
description: "Use revertOnDeletion, skipAnalysis and suspend on a Flagger Canary to control what happens when you stop using Flagger or pause a release."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default, deleting a Canary leaves resources Flagger does not own as they are. If the canary adopted existing resources (a service, a virtual service), they remain mutated. Set `spec.revertOnDeletion: true` to have Flagger revert on deletion: target replicas set to the primary replica count, the service selector reverted, and mesh/ingress traffic routing to the target restored. Expect a delay on delete, and enable it only when you will no longer rely on Flagger.

To simply stop analysing, the recommended approach is `skipAnalysis: true`, which needs less reconciliation. Flagger then checks that the canary deployment is healthy and promotes it without analysis; an analysis already running is cancelled and promotion runs.

`spec.suspend: true` pauses reconciliation completely: changes to targets and tracked ConfigMaps or Secrets do not trigger a run, and changes to generated resources are not corrected. A suspend during an active run pauses it without disturbing workloads or traffic weights.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
