---
id: computing-software.cloud-infrastructure-engineering.kubernetes.api-version-lifecycle-and-kubectl-convert
name: api-version-lifecycle-and-kubectl-convert
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, api-groups, beta-api-policy, api-deprecation, kubectl-convert, api-versions, manifest-migration]
level: practitioner
status: docs-checked
description: "Understand API groups and alpha/beta/GA guarantees (deprecation windows, beta-off-by-default policy) and migrate manifests to current versions with the kubectl convert plugin."
sources: ["https://kubernetes.io/docs/reference/using-api/#api-groups", "https://kubernetes.io/docs/reference/deprecation-policy/", "https://kubernetes.io/docs/reference/using-api/deprecation-guide/#migrate-to-non-deprecated-apis", "https://kubernetes.io/docs/reference/using-api/deprecation-guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API version lifecycle and kubectl convert

## Groups and versions
`apiVersion: <group>/<version>`; core group has no prefix (`v1`). Discover what a server serves:
```bash
kubectl api-resources -o wide      # group/version, namespaced, kind, verbs
```
The deprecation policy requires API objects to round-trip between API versions in a release
without information loss, and the "preferred" and "storage" versions of a group may not advance
until a release supports both the new and the previous version.

## Stability guarantees (deprecation policy)
| Level | Removal after deprecation | Notes |
|---|---|---|
| Alpha (`v1alpha1`) | any release, without prior deprecation notice | built-in alpha versions are disabled by default |
| Beta (`v1beta1`) | deprecated no more than 9 months or 3 minor releases after introduction, and no longer served 9 months or 3 minor releases after deprecation (whichever is longer in each case) | built-in beta versions are disabled by default, except beta APIs introduced before 1.22 |
| GA (`v1`) | may be deprecated, but not removed within a major version | |
Use of a deprecated API returns a `Warning` header and sets the gauge
`apiserver_requested_deprecated_apis` (labels `group`, `version`, `resource`, `subresource`,
`removed_release`) to 1 in kube-apiserver.
Notable removals: extensions/v1beta1 Ingress (1.22), policy/v1beta1 PSP & PDB (1.25),
batch/v1beta1 CronJob (1.25), autoscaling/v2beta2 HPA (1.26), flowcontrol v1beta2 (1.29).

## Migrate manifests with kubectl convert
`kubectl convert` is a separate kubectl plugin; install it from the "Install kubectl convert plugin"
section of the kubectl install page for your OS (kubernetes.io/docs/tasks/tools/).
```bash
kubectl convert -f ./old-ingress.yaml --output-version networking.k8s.io/v1
```
Review the output. For Ingress in `networking.k8s.io/v1`, `spec.backend` becomes `spec.defaultBackend`,
`serviceName` becomes `service.name`, a numeric `servicePort` becomes `service.port.number` (a
string one becomes `service.port.name`), and `pathType` is required for each path (`Prefix`,
`Exact` or `ImplementationSpecific`; use `ImplementationSpecific` to match undefined `v1beta1`
behaviour). Templated manifests (Helm, Kustomize) must be edited by hand.

## Also migrate stored objects
After a CRD storage version change, objects stay stored at their old version until rewritten.
Before removing a version from a CRD, either run Storage Version Migration for the resource
(a `StorageVersionMigration` object; on success the old version is removed from the CRD's
`status.storedVersions`) or rewrite every object with the same content, then remove the old
version from `status.storedVersions` (see the CRD versioning page on kubernetes.io).

## Verify
- [ ] No manifest uses an API version that the target release no longer serves (compare against the
      Deprecated API Migration Guide).
- [ ] `apiserver_requested_deprecated_apis` has no series with `removed_release` at or below the target.

## Checked
Checked 2026-10-24 against the kubernetes/website sources for the Deprecation Policy (rules 4a/4b,
deprecated-API warning and metric), "Kubernetes API" overview (alpha/beta defaults), the
Deprecated API Migration Guide (Ingress v1 changes; removal releases: Ingress 1.22, PSP and PDB 1.25,
CronJob 1.25, HPA autoscaling/v2beta2 1.26, flowcontrol v1beta2 1.29) and the CRD versioning page
(Storage Version Migration, `status.storedVersions`).
Method: documentation only; no commands were run.
