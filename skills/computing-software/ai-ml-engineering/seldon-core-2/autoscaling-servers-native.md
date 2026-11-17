---
id: computing-software.ai-ml-engineering.seldon-core-2.autoscaling-servers-native
name: autoscaling-servers-native
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, autoscaling, server-autoscaling, server-packing, autoscalingserverenabled, enable-server-autoscaling, statefulset]
level: advanced
status: docs-checked
description: "Native Seldon Core 2 server autoscaling driven by model replica needs: Server minReplicas and maxReplicas, scale down policies, and the experimental server packing settings."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/core-autoscaling-servers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Native server autoscaling

Server replicas are long-lived and host multiple models. Core 2 scales them in response to the number of model replicas requested. This is required for multi-model serving, where models load and unload dynamically.

## Enable
1. Set `minReplicas` and `maxReplicas` in the Server CR.
2. Set helm value `autoscaling.autoscalingServerEnabled` to true (default) on `seldon-core-v2-setup`. Without helm, set env `ENABLE_SERVER_AUTOSCALING` to true in the `seldon-scheduler` podSpec through SeldonConfig or a SeldonRuntime override.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Server
metadata:
  name: mlserver
  namespace: seldon
spec:
  replicas: 2
  minReplicas: 1
  maxReplicas: 4
  serverConfig: mlserver
```

Leaving out `minReplicas` or `maxReplicas` disables server autoscaling, so you scale manually through `replicas` or use an external mechanism such as HPA.

## Scale up
The only policy is model replica demand: if a model needs more replicas than servers can host, servers scale up. Existing replicas keep serving during the change.

## Scale down
Servers are StatefulSets, so scale down removes the pod with the largest index. Models on a draining replica are rescheduled elsewhere before removal, with no downtime.

Policies:
1. Empty server replica: remove a replica that hosts no models. Best for single-model serving; with multi-model serving it can pack poorly.
2. Lightly loaded replicas (experimental, may raise latency): enable with `autoscaling.serverPackingEnabled` true and `autoscaling.serverPackingPercentage` between 0 and 100. A lower percentage means fewer packing events. Packing runs only when a model replica is removed.

## Checked

2026-11-04. Confirmed against scaling/core-autoscaling-servers.md (Seldon Core 2 docs, v2 branch): enable steps, ENABLE_SERVER_AUTOSCALING, StatefulSet scale-down, two policies, serverPacking values. Removed or corrected: nothing.

Method: documentation only; no commands were run.
