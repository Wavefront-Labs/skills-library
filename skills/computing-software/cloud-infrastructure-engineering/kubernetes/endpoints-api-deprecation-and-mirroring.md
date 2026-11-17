---
id: computing-software.cloud-infrastructure-engineering.kubernetes.endpoints-api-deprecation-and-mirroring
name: endpoints-api-deprecation-and-mirroring
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, endpointslice, endpoints-deprecation, endpointslice-mirroring, service-discovery]
level: practitioner
status: docs-checked
description: "Move off the deprecated v1 Endpoints API: what still uses it, the 1000-endpoint truncation, EndpointSlice mirroring for manual Endpoints, and migrating tools."
sources: ["https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/#endpointslice-mirroring", "https://kubernetes.io/docs/concepts/services-networking/service/#over-capacity-endpoints", "https://kubernetes.io/blog/2025/04/24/endpoints-deprecation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Endpoints API deprecation

## Status
The core `v1 Endpoints` API is deprecated since Kubernetes 1.33. EndpointSlices are the supported
discovery API, and newer features such as `trafficDistribution` are not available in Endpoints.

## Limits of Endpoints
- Over 1000 backing endpoints for a Service: the Endpoints object is truncated to at most 1000
  addresses and annotated `endpoints.kubernetes.io/over-capacity: truncated`; the control plane
  removes the annotation when the count drops below 1000. A Service can have several
  EndpointSlices, so the limit affects only the legacy API.
- The legacy object cannot carry information needed by newer features.

## Mirroring
The control plane mirrors most user-created Endpoints objects to EndpointSlices, so older
controllers keep working; the feature is itself deprecated. Mirroring is skipped when the Endpoints
object has label `endpointslice.kubernetes.io/skip-mirror: "true"`, has the
`control-plane.alpha.kubernetes.io/leader` annotation, its Service does not exist, or its Service
has a selector. At most 1000 addresses per subset are mirrored. Mirrored slices are labelled
`endpointslice.kubernetes.io/managed-by: endpointslicemirroring-controller.k8s.io`.

For selector-less Services, create EndpointSlices directly:
```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: legacy-db-1
  labels:
    kubernetes.io/service-name: legacy-db
    endpointslice.kubernetes.io/managed-by: platform-team
addressType: IPv4
ports: [{name: pg, port: 5432, protocol: TCP}]
endpoints:
- addresses: ["10.20.0.15"]
```

## Find remaining users
Use the API server's deprecated-API request metric and audit logs filtered on the `endpoints`
resource to find the clients. Candidates: older ingress controllers, meshes, monitoring that
discovers targets through Endpoints, and scripts that run `kubectl get endpoints`.

## Migration of scripts
`kubectl get endpoints web` becomes
`kubectl get endpointslices -l kubernetes.io/service-name=web`.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the EndpointSlice concept page (mirroring conditions, 1000 per subset, deprecation in 1.33), the Service page (over-capacity truncation and annotation) and the kubernetes/kubernetes source (mirroring controller managed-by value). Removed the PromQL grep, the claim about whole-object rewrites to all watchers and the named Prometheus role switch.

Method: documentation only; no commands were run.
