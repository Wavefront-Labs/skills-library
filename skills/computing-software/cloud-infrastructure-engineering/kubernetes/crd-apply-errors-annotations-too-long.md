---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crd-apply-errors-annotations-too-long
name: crd-apply-errors-annotations-too-long
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crds, annotations-too-long, server-side-apply, strict-field-validation, helm]
level: practitioner
status: docs-checked
description: "Fix CRD and large-object apply errors: annotations too long from last-applied-configuration, and unknown or duplicate field errors from strict validation."
sources: ["https://kubernetes.io/docs/reference/using-api/server-side-apply/", "https://kubernetes.io/docs/reference/using-api/api-concepts/#field-validation", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiextensions-apiserver/pkg/apis/apiextensions/validation/validation.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD apply errors

## metadata.annotations: Too long
```
The CustomResourceDefinition "prometheuses.monitoring.coreos.com" is invalid:
metadata.annotations: Too long: must have at most 262144 bytes
```
Client-side `kubectl apply` stores the applied configuration in the
`kubectl.kubernetes.io/last-applied-configuration` annotation; large CRDs exceed the 256 KiB (262144-byte)
annotation limit.

Fix with server-side apply (no annotation needed):
```bash
kubectl apply --server-side -f crds/
kubectl apply --server-side --force-conflicts -f crds/    # when another manager owns fields
```
Or `kubectl create` first then `kubectl replace` for updates.

## unknown field / duplicate field
```
Error from server (BadRequest): error when creating "x.yaml": Foo in version "v1" cannot be
handled as a Foo: strict decoding error: unknown field "spec.replcas"
```
kubectl defaults to strict server-side field validation (`--validate=true`), so typos and fields from a newer CRD version
fail instead of being dropped.
- Typo: fix it.
- Field exists only in a newer CRD version: upgrade the CRD before the custom resources.
- Temporary bypass: `kubectl apply --validate=warn` (or `ignore`); the API server's own default level is `Warn`; never use it as a permanent fix.

## Other common CRD errors
- `must have exactly one version marked as storage version`.
- Removing a version that is still listed in `status.storedVersions` is rejected: it must remain in `spec.versions` until a storage migration removes it from `status.storedVersions`.

## Verify
`kubectl get crd <name> -o jsonpath='{.metadata.managedFields[*].manager}'` shows your SSA field
manager, and re-applying is a no-op.

## Checked
Checked 2026-10-24 against the API concepts and Server-Side Apply pages (website main, v1.37) and the apimachinery and apiextensions source: 262144-byte (256 KiB) total annotation limit, `--server-side` and `--force-conflicts`, `kubectl --validate` values ignore, warn, strict (true is strict), server default level Warn, one storage version per CRD, storedVersions rule. Removed the Argo CD and Helm claims and the unconfirmed schema-required message.
Method: documentation only; no commands were run.
