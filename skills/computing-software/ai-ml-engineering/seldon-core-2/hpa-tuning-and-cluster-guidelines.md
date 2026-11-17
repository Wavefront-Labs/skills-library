---
id: computing-software.ai-ml-engineering.seldon-core-2.hpa-tuning-and-cluster-guidelines
name: hpa-tuning-and-cluster-guidelines
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, hpa, scaling-policy, stabilization-window, load-testing, cluster-autoscaler, capacity-planning]
level: advanced
status: docs-checked
description: "Tune HPA for Seldon Core 2: default scale up and down behaviour, setting averageValue from a load test, minReplicas and maxReplicas, stabilization windows and cluster capacity."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/model-hpa-autoscaling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HPA tuning and cluster guidelines

## Default HPA behaviour
Scale up is aggressive: up to 4 replicas every 15 seconds or 100 percent of existing replicas, whichever is higher. Scale down is gradual: HPA uses the highest recommended replica count over the most recent 5 minutes. With RPS metrics, the replicas added depend on the policy limits, the `averageValue` per replica target, and how fast load changes.

## Sizing the target
- Estimate peak load per model with a margin. If you know the minimum number of replicas to serve peak without breaching latency SLAs, use it as HPA `maxReplicas` and set `target.averageValue` to peak RPS divided by that number.
- Otherwise run an open-loop load test on one replica with no scaling and a slowly ramping request rate. Find the RPS where latency SLAs break (or where latency starts to rise) and set `averageValue` from that.
- Set `minReplicas` from the low-load RPS, balancing cost against ready capacity for a sudden rise.

## Policies
- Stabilization window: with a 60 second scale-up window and 4 samples, only the smallest recommendation in the window is applied; use it to absorb short spikes.
- Check that the scale-up rate keeps up with expected sustained ramps, such as moving traffic in a blue-green rollout.

## Cluster capacity
The cluster must have room for the total server replicas that all HPAs may request at once, especially with aggressive scale-up, or SLAs may be breached. Models with correlated peaks need enough nodes for every pod concurrently; use the Kubernetes Cluster Autoscaler or, in the cloud, the provider's cluster autoscaling service.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/scaling/model-hpa-autoscaling.md (cluster operation guidelines section read in full). Replaced unsupported "overprovisioning" with the provider autoscaler the page names.
