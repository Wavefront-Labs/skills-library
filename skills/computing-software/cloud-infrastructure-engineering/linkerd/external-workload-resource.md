---
id: computing-software.cloud-infrastructure-engineering.linkerd.external-workload-resource
name: external-workload-resource
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, externalworkload, mesh-expansion, non-kubernetes]
level: advanced
status: docs-checked
description: "Describe a workload outside Kubernetes with an ExternalWorkload resource so Services can select it as an endpoint."
sources:
  - https://linkerd.io/2.19/reference/external-workload/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An `ExternalWorkload` is a namespaced resource that tells Linkerd about a workload living outside Kubernetes, for discovery and policy. Linkerd translates it into `EndpointSlice`s attached to Service objects.

Spec:

- `meshTLS` (required): identity information needed for encrypted connections.
  - `identity` (required): the TLS identity of the workload, which proxies need to establish TLS.
  - `serverName` (required): the value the workload's proxy expects in the `ClientHello` SNI extension.
- `workloadIPs` (required, at most one): an IP address the workload is reachable on.
- `ports`: list of port definitions, each with `name` (unique within the set, so Services can refer to it), `port` (required) and `protocol`.

Status holds `conditions`, each with `type` (`Ready` indicates discoverability), `status` (True, False or Unknown), `reason`, `message`, `lastProbeTime` and `lastTransitionTime`.

The resource uses `apiVersion: workload.linkerd.io/v1beta1` and `kind: ExternalWorkload`. Fill in `spec.meshTLS`, `spec.workloadIPs` and `spec.ports` as above, and have a Service select it.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/reference/external-workload/.

Removed or reworded: Closing advice not on the page.

Method: documentation only; no commands were run.
