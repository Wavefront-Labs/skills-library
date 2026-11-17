---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-endpointslice-migration
name: prometheus-operator-endpointslice-migration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [endpointslice, endpoints-deprecated, servicediscoveryrole, kubelet-endpointslice, k8s-1-33]
level: advanced
status: docs-checked
description: "Migrate kubelet and ServiceMonitor discovery from the deprecated Endpoints API to EndpointSlice in ten steps."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Kubernetes 1.33 the `v1 Endpoints` API is deprecated. If operator logs say `v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice`, the operator still reconciles the kubelet Endpoints object.

## Migration steps
1. Grant the operator ServiceAccount RBAC to manage EndpointSlice resources (a Role on `discovery.k8s.io` `endpointslices` with verbs get, create, list, update, delete).
2. Grant the Prometheus ServiceAccount `get`/`list`/`watch` on EndpointSlices.
3. Start the operator with `--kubelet-endpoints=true --kubelet-endpointslice=true`.
4. Check the kubelet Endpoints object has the annotation `endpointslice.kubernetes.io/skip-mirror=true`.
5. Check the kubelet EndpointSlice objects are current.
6. Set `.spec.serviceDiscoveryRole: EndpointSlice` on every ServiceMonitor pointing at the kubelet Service.
7. Verify Prometheus discovers the expected targets.
8. Restart the operator with `--kubelet-endpoints=false --kubelet-endpointslice=true`.
9. Delete the kubelet Endpoints resource.

## Other ServiceMonitors
To move all monitors, give the Prometheus ServiceAccount read access to EndpointSlices in every watched namespace and set `serviceDiscoveryRole: EndpointSlice` per monitor (or at the Prometheus level).

kube-prometheus release-0.16 runs in dual mode, supporting Endpoints and EndpointSlice in parallel, with full removal planned for a later release.

## Checked

2026-11-08. Read the troubleshooting page in full. Replaced an invented Role namespace remark with the verbs listed in the docs.

Method: documentation only; no commands were run.
