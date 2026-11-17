---
id: computing-software.ai-ml-engineering.litellm.litellm-prod-sizing-autoscaling
name: litellm-prod-sizing-autoscaling
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, uvicorn-workers, num-workers, autoscaling]
level: advanced
status: docs-checked
description: "Size LiteLLM pods (1 vCPU and 4Gi per worker), autoscale on CPU, and choose workers per pod."
sources:
  - https://docs.litellm.ai/docs/proxy/prod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Machine sizing: give each pod 1 vCPU and 4Gi of memory as both requests and limits, and scale both with the worker count if you run more than one worker per container.

```
resources:
  requests:
    cpu: "1"       # 1 * num_workers
    memory: "4Gi"  # 4 * num_workers
  limits:
    cpu: "1"
    memory: "4Gi"
```

The figures are per worker: a container with 8 workers wants 8 vCPU and 32Gi. 4Gi is a floor, not a target. If you enable `store_prompts_in_spend_logs`, each row carries a full prompt and response, so treat 4Gi as the minimum.

Autoscaling: scale on CPU and leave the memory target unset. The query engine's resident memory reflects the largest write a pod has ever done, so it is not a usable signal.

```
targetCPUUtilizationPercentage: 60
```

The litellm-helm startup probe allows up to 300 seconds for the first readiness check, so a replica added at a higher threshold arrives too late.

Workers: on Kubernetes (or where a pod-level autoscaler reads CPU) run one Uvicorn worker per pod and scale horizontally:

```
CMD ["--port", "4000", "--config", "./proxy_server_config.yaml", "--num_workers", "1"]
```

On a single VM or bare container with nothing scaling it, set `NUM_WORKERS` to the machine's vCPU count.

Failure mode: do not combine `--num_workers 1` with `--max_requests_before_restart`. With one worker the flag recycles nothing; once the limit is hit the whole pod stops serving.

Connections multiply: 3 instances x 4 workers x 10 pool connections = 120 database connections.

## Checked

2026-11-03. Confirmed on the LiteLLM production page (docs.litellm.ai/docs/proxy/prod): 1 vCPU and 4Gi per worker as requests and limits, 4Gi as a floor with store_prompts_in_spend_logs, CPU-only autoscaling with targetCPUUtilizationPercentage 60, the 300 second litellm-helm startup probe, one Uvicorn worker per pod, the --num_workers 1 plus --max_requests_before_restart failure, and the 3 x 4 x 10 = 120 connection example.

Method: documentation only; no commands were run.
