---
id: computing-software.devops-ci-cd.argo-workflows.resource-duration
name: resource-duration
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [resource-duration, cpu-seconds, memory-base-amount, request-defaults, workflow-cost]
level: intro
status: docs-checked
description: "Interpret the indicative resource duration reported per workflow, including base amounts, request fallbacks and the rounding of short pods."
sources: ["https://argo-workflows.readthedocs.io/en/latest/resource-duration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource duration
Resource duration is an indicative, not accurate, usage estimate stored with the Workflow. It is computed from container run time and the pod's requests, limits or defaults, then divided by a base amount per resource:
- CPU: `1`
- Memory: `100Mi`
- Storage and ephemeral storage: `10Gi`
- anything else: `1`

The requested fraction of the base times run time is the duration. A `50Mi` request running 120s gives `60s * (100Mi memory)`.

If `requests` are missing, Kubernetes falls back to `limits`; if those are missing too, Argo uses `100m` CPU and `100Mi` memory. These are Argo's defaults, not Kubernetes', so set requests or limits on all containers for meaningful numbers.

Worked example: 3 minutes with CPU limit `2000m`, memory `1Gi`, and `nvidia.com/gpu: 1` gives CPU 6min*(1 cpu), memory 30min*(100Mi memory), GPU 3min*(1 nvidia.com/gpu).

The web UI and CLI show abbreviated values like `9m10s*cpu,6s*memory,2m31s*nvidia.com/gpu`; here `memory` means time a resource requested 100Mi. A container using 10Mi counts a tenth of a second per second.

Rounding: a pod under 10s with a small memory request (such as `10Mi`) can show memory as 0s because the denominator is 100Mi.

## Checked

2026-11-08. Read the Argo Workflows resource duration page in full (raw markdown) and confirmed base amounts, request fallbacks, the worked examples, UI and CLI abbreviations, and rounding of short pods. Nothing removed.

Method: documentation only; no commands were run.
