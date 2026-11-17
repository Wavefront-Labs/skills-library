---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-pod-spec-fields
name: opentelemetry-operator-collector-pod-spec-fields
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, probes, topologyspreadconstraints, volumeclaimtemplates, healthcheck-extension, pod-scheduling]
level: practitioner
status: docs-checked
description: "Reference the pod-shaping fields of the v1beta1 Collector spec: probes tied to the health extension, scheduling, env, volumes, ConfigMaps and config version retention."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pod-level fields on OpenTelemetryCollector

The v1beta1 `OpenTelemetryCollector` spec mirrors many pod options. Notable ones documented in the API reference:

Probes. `livenessProbe`, `readinessProbe` and `startupProbe` configure everything except the probe handler, which is generated from the Collector's health check extension. They only take effect when `healthcheckextension` is configured in the Collector pipeline. A gRPC probe can set `mode` to `TLS` or `Plaintext`.

Scheduling and placement: `nodeSelector`, `affinity`, `tolerations`, `topologySpreadConstraints`, `priorityClassName`.

Container: `image`, `imagePullPolicy`, `imagePullSecrets`, `command` (overrides the entrypoint; the image ENTRYPOINT is used when omitted), `args` (map of binary arguments), `env`, `envFrom`, `resources`, `lifecycle`, `terminationGracePeriodSeconds`.

Storage: `volumes`, `volumeMounts`, and for statefulset mode `volumeClaimTemplates` plus `persistentVolumeClaimRetentionPolicy`. `serviceName` sets the StatefulSet service name and defaults to `<name>-headless`; a custom name is not created by the operator.

Config delivery: `configmaps` mounts ConfigMaps from the same namespace into the pods, and `configVersions` (default 3) keeps that many generated config ConfigMaps.

Networking: `hostNetwork`, `shareProcessNamespace`, `dnsPolicy`, `ipFamilies`, `ipFamilyPolicy` (default SingleStack).

Because host-level fields are passed through unfiltered, review the security notes before granting create rights.

## Checked

2026-11-04. Confirmed in the generated OpenTelemetryCollector API reference (docs/api/opentelemetrycollectors.md, read as raw Markdown because the GitHub page view is a stub) (v1beta1 spec table): the probes and their health-extension note, scheduling fields, `command` and `args` (map), `env`, `envFrom`, `lifecycle`, `terminationGracePeriodSeconds`, `volumeClaimTemplates` and `persistentVolumeClaimRetentionPolicy` for statefulset, `serviceName` default `<name>-headless` with the custom Service not created, `configmaps`, `configVersions` default 3, `hostNetwork`, `shareProcessNamespace`, `dnsPolicy`, `ipFamilies` and `ipFamilyPolicy` default SingleStack, and the gRPC probe `mode` of TLS or Plaintext. Nothing removed.

Method: documentation only; no commands were run.
