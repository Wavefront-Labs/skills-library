---
id: computing-software.ai-ml-engineering.kserve.kserve-config-deploy-resources-sidecars
name: kserve-config-deploy-resources-sidecars
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [defaultdeploymentmode, servingkserveiodeploymentmode, serviceannotationdisallowedlist, logger-config, batcher-config, maxbatchsize, maxlatency, router-headers-propagate, servingkserveioautoscaler-class, servingkserveiodisable-auto-update]
level: advanced
status: docs-checked
description: "inferenceservice-config keys for deployment mode, default resources, annotation disallow lists, logger/batcher/agent/router sidecars, autoscaler-class and runtime auto-update."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/configurations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# inferenceservice-config: deploy, resources and sidecars

**deploy**: `defaultDeploymentMode` is `Knative` (default), `Standard` or `ModelMesh`. Per service: annotation `serving.kserve.io/deploymentMode: "Standard"`.

**inferenceService**: default container `resource` cpuLimit "1", memoryLimit "2Gi", cpuRequest "1", memoryRequest "2Gi". Set a value to `null`, `""` or remove it to leave it unbounded. `serviceAnnotationDisallowedList` (default: `autoscaling.knative.dev/min-scale`, `autoscaling.knative.dev/max-scale`, `internal.serving.kserve.io/storage-initializer-sourceuri`, `kubectl.kubernetes.io/last-applied-configuration`) and `serviceLabelDisallowedList` (default empty) list keys that are not propagated to Knative revisions, which prevents a reconciliation loop being triggered. Neither has a per-service override.

**logger**: image `kserve/agent`, 100Mi/1Gi memory, 100m/1 cpu, `defaultUrl` `http://default-broker`.

**batcher**: image `kserve/agent`, 1Gi memory and 1 cpu (request and limit), `maxBatchSize` "32", `maxLatency` "5000" (ms). Both are strings.

**agent**: image `kserve/agent`, 100Mi/1Gi, 100m/1.

**router** (InferenceGraph): image `kserve/router`, same resources, `imagePullPolicy` IfNotPresent, `imagePullSecrets`, and `headers.propagate`, a list of header names or Go regex patterns (for example `["Authorization", "*Trace-Id*"]`) forwarded to every graph step; others are dropped. Default empty.

**explainers**: `art.image` `kserve/art-explainer`, `art.defaultImageVersion` latest.

**service**: `serviceClusterIPNone` (headless Services, Standard only). **security**: `autoMountServiceAccountToken` true.

Per-service annotations: `serving.kserve.io/autoscaler-class` (Standard only: `hpa` default, `keda`, `external`, `none`; use `none` to disable KServe autoscaling, `external` only when another controller owns the HPA) and `serving.kserve.io/disable-auto-update: "true"` to control whether the deployment is updated automatically when the ServingRuntime spec changes (default false; there is no global key for either annotation).

## Checked
Confirmed against the KServe Configurations admin guide: deploy mode values and annotation, inferenceService resource defaults and unbounded options, both disallow lists with defaults, logger, batcher, agent, router (including headers.propagate, imagePullPolicy, imagePullSecrets), ART explainer, serviceClusterIPNone, autoMountServiceAccountToken, autoscaler-class values and the disable-auto-update annotation. Reworded the disallow-list rationale and the auto-update description to what the page states.

Method: docs-only read of cited pages, 2026-11-08
