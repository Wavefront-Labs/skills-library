---
id: computing-software.cloud-infrastructure-engineering.kubernetes.downward-api-and-projected-volumes
name: downward-api-and-projected-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, downward-api, downwardapi, projected-volumes, fieldref, resourcefieldref, ckad]
level: practitioner
status: docs-checked
description: "Expose pod metadata and resource limits to containers with the Downward API (env fieldRef/resourceFieldRef, downwardAPI volumes) and combine sources with projected volumes."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/downward-api/", "https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/", "https://kubernetes.io/docs/concepts/storage/projected-volumes/", "https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Downward API and projected volumes

## Env vars (fieldRef / resourceFieldRef)
```yaml
env:
- name: POD_NAME
  valueFrom: {fieldRef: {fieldPath: metadata.name}}
- name: POD_NAMESPACE
  valueFrom: {fieldRef: {fieldPath: metadata.namespace}}
- name: POD_IP
  valueFrom: {fieldRef: {fieldPath: status.podIP}}
- name: NODE_NAME
  valueFrom: {fieldRef: {fieldPath: spec.nodeName}}
- name: SA
  valueFrom: {fieldRef: {fieldPath: spec.serviceAccountName}}
- name: GOMAXPROCS
  valueFrom: {resourceFieldRef: {resource: limits.cpu, divisor: "1"}}   # divisor 1 means cores for cpu
- name: GOMEMLIMIT
  valueFrom: {resourceFieldRef: {resource: limits.memory}}
```
Available as env vars but not as a `downwardAPI` volume `fieldRef`: `status.podIP`, `status.podIPs`,
`status.hostIP`, `status.hostIPs`, `spec.nodeName`, `spec.serviceAccountName`. Available through either:
`metadata.name`, `metadata.namespace`, `metadata.uid`, `metadata.labels['<KEY>']` and
`metadata.annotations['<KEY>']`. If a CPU or memory limit is not set and you expose it, the kubelet
exposes the node's maximum allocatable value for CPU and memory.

## downwardAPI volume (updates live)
```yaml
volumes:
- name: podinfo
  downwardAPI:
    items:
    - {path: labels, fieldRef: {fieldPath: metadata.labels}}
    - {path: annotations, fieldRef: {fieldPath: metadata.annotations}}
    - path: mem_limit
      resourceFieldRef: {containerName: app, resource: limits.memory, divisor: 1Mi}
```
The whole-object `metadata.labels` and `metadata.annotations` fields work only in a `downwardAPI`
volume (one `key="value"` per line), not as env vars. A downward API volume is updated when those
values change and when CPU or memory resources are resized in place; env vars are not updated
unless the container restarts. A container using a projected volume source through `subPath` does not
receive updates.

## Projected volumes: several sources, one directory
```yaml
volumes:
- name: bundle
  projected:
    defaultMode: 0440
    sources:
    - configMap: {name: app-config, items: [{key: app.yaml, path: app.yaml}]}
    - secret: {name: app-secret, items: [{key: password, path: creds/password}]}
    - downwardAPI: {items: [{path: pod/name, fieldRef: {fieldPath: metadata.name}}]}
    - serviceAccountToken: {path: token, audience: vault, expirationSeconds: 3600}
    - clusterTrustBundle: {signerName: example.com/internal, path: ca.pem}   # feature gate ClusterTrustBundleProjection
```
`serviceAccountToken` projections deliver audience-scoped tokens: `audience` defaults to the API
server's identifier, `expirationSeconds` defaults to 1 hour and must be at least 600, and the API
server flag `--service-account-max-token-expiration` can cap it. The kubelet rotates the token
once it is older than 80% of its TTL or older than 24 hours, so apps must re-read the file.
`clusterTrustBundle` projection is gated by `ClusterTrustBundleProjection` (beta from 1.33 and
off by default, stable from 1.37 per the feature gate page); by default the pod will not start if the
selected bundle is not found, unless `optional: true`.

## Gotchas
- `defaultMode` can only be set at the projected-volume level; set `mode` per item to override.
- Giving a runtime its CPU and memory limits via `resourceFieldRef` env vars is an explicit way to
  pass them on; check how your runtime consumes such variables.

## Verify
- [ ] `kubectl exec <pod> -- env` and a listing of the mount path show the expected values.

## Checked
Checked 2026-10-24 against the kubernetes/website Downward API page (field lists, env-only and
volume-only fields, fallback to node allocatable, resize behaviour), the Projected Volumes page
(`defaultMode`, `serviceAccountToken` defaults and minimum, `subPath`, `clusterTrustBundle`), the
Configure Service Accounts task (rotation at 80% of TTL or 24 hours), the `ClusterTrustBundleProjection`
feature gate page and the `ResourceFieldSelector.divisor` field in kubernetes/api.
Method: documentation only; no commands were run.
