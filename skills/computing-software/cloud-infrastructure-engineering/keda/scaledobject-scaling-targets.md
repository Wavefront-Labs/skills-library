---
id: computing-software.cloud-infrastructure-engineering.keda.scaledobject-scaling-targets
name: scaledobject-scaling-targets
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [scaledobject, scaletargetref, deployment, statefulset, custom-resource, scale-subresource]
level: intro
status: docs-checked
description: "Point a KEDA ScaledObject at a Deployment, StatefulSet or any custom resource with a /scale subresource, and pick the container used for secret env lookups."
sources:
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A ScaledObject (apiVersion `keda.sh/v1alpha1`) tells KEDA which workload to scale and which triggers drive it. KEDA watches the event source and feeds the numbers to a Horizontal Pod Autoscaler it creates, so each replica keeps its own connection and processing semantics with the source (in-order processing, retries, dead-letter, checkpointing). With a Kafka topic as the source, the flow is: no pending messages, so scale to zero; a message arrives and KEDA activates the workload; one container connects and pulls; more messages push metrics to the HPA for scale-out.

The target lives under `spec.scaleTargetRef`. Only `name` is mandatory and the target must be in the ScaledObject's namespace. `apiVersion` defaults to `apps/v1` and `kind` to `Deployment`; set both to scale a StatefulSet or any custom resource, for example an Argo Rollout. The sole constraint on a custom resource is that it defines the `/scale` subresource.

`envSourceContainerName` names the container from which KEDA tries to get environment properties holding secrets. If omitted, KEDA reads the first container, `.spec.template.spec.containers[0]`.

The generated HPA is named `keda-hpa-<scaled-object-name>` unless overridden under `advanced.horizontalPodAutoscalerConfig.name`.

## Checked

2026-11-03. Confirmed on the 2.17 Scaling Deployments and ScaledObject specification pages: scaleTargetRef defaults, /scale subresource, envSourceContainerName, HPA name. Removed: the FromEnv wording and multi-container advice.

Method: documentation only; no commands were run.
