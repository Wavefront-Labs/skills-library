---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crd-versioning-and-conversion-webhooks
name: crd-versioning-and-conversion-webhooks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crd, api-versioning, conversion-webhook, storage-version, served, deprecated, hub-and-spoke, controller-gen, kubebuilder-conversion, apiextensions-v1, multi-version-crd, storage-migration, etcd-storage-migrator]
level: advanced
status: docs-checked
description: "Add v1beta1 -> v1 to a CRD without breaking live objects: served/storage flags, hub-and-spoke conversion webhooks, and the storage migration step people skip."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/", "https://book.kubebuilder.io/multiversion-tutorial/conversion-concepts", "https://github.com/kubernetes-sigs/controller-runtime/tree/main/pkg/conversion", "https://cert-manager.io/docs/concepts/ca-injector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD API versioning and conversion webhooks — changing the contract without breaking what's already stored

**Goal:** ship `v2` of a CRD, deprecate `v1`, and have every existing object — the
ones sitting in etcd written as `v1` — keep working through `kubectl get`,
controllers, and backups, with no downtime and no manual `kubectl edit` sweep.

## 1. served vs storage — the two flags that matter
Each entry in `spec.versions` has:
- `served: true/false` — whether the API server accepts this version in requests.
- `storage: true/false` — **exactly one** version across the whole CRD must have this
  true; it's the shape etcd actually holds.
Multiple versions can be `served` simultaneously (clients pick via the URL path,
e.g. `/apis/example.com/v1` vs `/v2`), but objects are stored at the storage version.
Serving a different version than the stored one needs **conversion** (a request in a
non-storage version, a watch opened in one version while the stored object is in another,
or a PUT in a non-storage version).

## 2. Hub and spoke — the only sane conversion topology
When you have 3+ versions, don't write pairwise converters (`v1<->v2`, `v2<->v3`,
`v1<->v3` — O(n²) and a maintenance nightmare). Pick one version as the **hub**
(usually the storage version); every other version is a **spoke** that only knows
how to convert to/from the hub. The Kubebuilder book describes controller-runtime's
model this way: the `sigs.k8s.io/controller-runtime/pkg/conversion` interfaces `Hub`
(method `Hub()`, a marker) and `Convertible` (`ConvertTo(dst Hub) error` and
`ConvertFrom(src Hub) error`); the hub type implements `Hub()` and every spoke implements
`Convertible`. To convert between two spokes, convert to the hub first.

## 3. The webhook itself
A `CustomResourceConversion` with `strategy: Webhook` points at a Service serving
HTTPS; the API server calls it with a `ConversionReview` containing a list of objects to
convert and expects the converted objects back, in the same order. A request may carry multiple
objects, which the webhook should convert independently. Requirements:
- The Kubernetes docs say a webhook deployed as an in-cluster Service must be exposed on
  port 443 (the server itself can listen on any port).
- Use cert-manager to mint the certificate and inject the CA bundle: cert-manager's `cainjector`
  supports `CustomResourceDefinition` as an injectable, via the `cert-manager.io/inject-ca-from`
  annotation (value `<namespace>/<certificate-name>`). See
  `computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhook-development`
  for the shared cert-injection mechanics — conversion webhooks use the identical pattern.
- A conversion must not mutate anything in `metadata` other than `labels` and `annotations`;
  attempted changes to `name`, `UID` and `namespace` are rejected and fail the request that
  caused the conversion, and other changes are ignored. Keep conversion pure (no side effects,
  no calls to other APIs).
- `conversionReviewVersions` lists which `ConversionReview` versions the webhook understands; the
  first one the API server knows is sent, and the webhook must reply in the same version
  (`["v1"]` is typical).
- If the webhook is unreachable, requests that need conversion fail. Run it with the same HA
  posture as a production admission webhook (2+ replicas, PDB, readiness probe, no dependency
  on the resource it converts).

## 4. When `strategy: None` is enough
The default `conversion.strategy: None` only sets the `apiVersion` field and leaves the rest
of the object unchanged; the Kubernetes docs say to use it when there are no schema changes
between versions. If the conversion involves schema changes and needs custom logic (rename,
retype, restructure, split a field), use `strategy: Webhook`.

## 5. Deprecation and the storage migration step
1. Add the new version as `served: true, storage: false` alongside the old one.
2. Update controllers/clients to read/write the new version.
3. Flip `storage: true` to the new version (old stays `served: true` for now,
   `storage: false`).
4. **Run the storage migration**: flipping the storage flag does NOT rewrite
   existing objects — they stay stored at whatever version they were last written
   at. Either run Storage Version Migration for the resource (a `StorageVersionMigration`
   object naming `group` and `resource`; on success the old version is removed from
   the CRD's `status.storedVersions`) or write every object back with unchanged content,
   then remove the old version from `status.storedVersions` (patch the CRD's `status`
   subresource with `kubectl patch customresourcedefinitions <name> --subresource=status
   --type=merge`). Objects may exist at any version that was ever
   a storage version, so do this before dropping a version.
5. Once all clients use the new version (check the kube-apiserver logs for clients still on
   the old one), set the old version `served: false`; confirm the new version is the
   storage version and the old one is gone from `status.storedVersions`; then remove the old
   version from `spec.versions` and drop its conversion support in the webhook.

## Gotchas
- One and only one version must be marked `storage: true`; keep a single reviewed manifest
  for the CRD during a migration.
- Dropping a served version that CI/CD or Helm charts still emit breaks every
  caller silently — grep manifests and client code for the old `apiVersion` string
  before removing it, not just the CRD.
- `kubectl convert` (client-side) is unrelated and does not substitute for a
  server-side conversion webhook.
- The CRD `conversion.webhook` stanza has `clientConfig` and `conversionReviewVersions`,
  with no rule or selector fields like an admission webhook configuration, so conversion applies
  to the whole CRD.

## Verify
- [ ] Exactly one version has `storage: true`.
- [ ] `kubectl get --raw /apis/<group>/<old-version>/...` and the same path with the new version
      both return the object.
- [ ] With the conversion webhook's pods stopped, a request in a non-storage version fails
      (confirms the webhook is wired in).
- [ ] After flipping `storage`, the migration has completed and `status.storedVersions` no longer
      lists the version you are about to remove.

## Checked
Checked 2026-10-24 against the kubernetes/website "Versions in CustomResourceDefinitions" page (served
and storage, `strategy: None` semantics, conversion webhook requirements, permissible mutations, port
443, `conversionReviewVersions`, Storage Version Migration, `storedVersions`), the Kubebuilder book
(hub and spoke), controller-runtime `pkg/conversion` (`Hub`, `Convertible`) and the cert-manager CA
injector page (`CustomResourceDefinition` injectable, `cert-manager.io/inject-ca-from`).
Method: documentation only; no commands were run.
