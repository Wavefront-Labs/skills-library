---
id: computing-software.cloud-infrastructure-engineering.cilium.clustermesh-global-services
name: clustermesh-global-services
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, clustermesh, global-services, service-cilium-io-global, shared, endpointslice-sync]
level: practitioner
status: docs-checked
description: "Make a Kubernetes Service global across ClusterMesh with service.cilium.io/global, stop sharing local backends, and sync EndpointSlices (beta)."
sources:
  - https://docs.cilium.io/en/stable/network/clustermesh/global-services/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ClusterMesh global services

Prerequisite: a working Cluster Mesh.

Define a Service with identical name and namespace in each cluster and annotate `service.cilium.io/global: "true"`. Cilium load-balances to pods in all clusters.

## Stop sharing local endpoints
Global implicitly means `service.cilium.io/shared: "true"`. Set `service.cilium.io/shared: "false"` to consume remote endpoints without exposing local ones.

## EndpointSlice sync (beta)
Off by default for non-headless global services; enabled by default for global headless ones unless opted out with `service.cilium.io/global-sync-endpoint-slices: "false"`. Enable per service with `service.cilium.io/global-sync-endpoint-slices: "true"` so Cilium creates EndpointSlices for remote-cluster endpoints, needed only for third-party controllers or DNS discovery (the Cilium ingress controller works without it). Needs the feature flag `clustermesh.enableEndpointSliceSynchronization=true` (Helm), and on an existing install restart the operator: `kubectl -n kube-system rollout restart deployment/cilium-operator`.

Limitation: hostnames sync as is with no conflict resolution, so StatefulSets behind a governing Service in several clusters must have distinct names (for example `cluster1-my-statefulset`).

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/network/clustermesh/global-services/. 

Method: documentation only; no commands were run.
