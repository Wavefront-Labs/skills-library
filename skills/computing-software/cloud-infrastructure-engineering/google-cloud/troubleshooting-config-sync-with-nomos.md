---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-config-sync-with-nomos
name: troubleshooting-config-sync-with-nomos
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, config-sync, config-sync-troubleshooting, nomos-status, rootsync, reposync, gitops]
level: practitioner
status: docs-checked
description: "Debug Config Sync on GKE fleets: nomos status and vet, RootSync/RepoSync, KNV error codes, management conflicts and rendering errors."
sources: ["https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/how-to/nomos-command", "https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/reference/errors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Config Sync with nomos

## First look
```bash
gcloud beta container fleet config-management status --project=<P>   # per-membership sync state
nomos status --contexts=$(kubectl config current-context)           # last applied commit, status, errors
kubectl get rootsync <ROOTSYNC_NAME> -n <NAMESPACE> -o yaml
kubectl get reposync -A
```
`nomos status` reports, per cluster, the hash of the last applied commit and the status of the
resources Config Sync manages.

## Common errors
| Code | Meaning (from the errors reference) | Next step |
|---|---|---|
| `KNV2004` Source Error | Config Sync cannot read from the source of truth | follow "Troubleshoot connecting to the source of truth" and Known issues |
| `KNV1021` Unknown Object | no CustomResourceDefinition for the resource in the cluster | add or install the CRD for non-built-in kinds |
| `KNV2009` Apply Error | generic: some configs failed to sync | follow "Troubleshoot syncing" |
| `KNV1060` Management Conflict | same object (group, kind, name, namespace) declared in more than one source | RootSync wins over RepoSync; update one source or delete the object from it. `nomos vet` checks one repo at a time and cannot detect this |
| `KNV1068` Actionable Rendering Error | kustomize rendering problem | preview with `nomos hydrate` and `nomos vet`; remote bases from public repos may need `spec.override.enableShellInRendering: true` |
| `KNV2005` Resource Fight | another controller fights Config Sync over a resource | see "Troubleshoot controller fights" |

## Validate before push
```bash
nomos vet --path=./config-root --source-format=unstructured
nomos hydrate --path=./config-root --source-format=unstructured --output=<OUT_DIR>
```
`--source-format unstructured` is required for an unstructured source of truth. `nomos vet` exits
non-zero and logs errors to STDERR, so it works as a CI gate.

## Gotchas
- The annotation `configmanagement.gke.io/managed: disabled` marks objects or namespaces as unmanaged (see `KNV1056`).
- `KNV1034`: the `config-management-system`, `resource-group-system` and `config-management-monitoring` namespaces must not be declared in the source.

## Verify
- [ ] `nomos status` shows the latest commit applied for every cluster, with no errors.

## Checked
Date: 2026-10-31. Confirmed in the Config Sync pages nomos-command and errors reference: nomos
`status`, `vet`, `hydrate`, flags `--contexts`, `--path`, `--source-format`, `--output`, the error rows above,
and the managed-disabled annotation. `gcloud container fleet config-management status` exists only under
`gcloud beta` per the review tooling, so the command is written with `beta`. Removed unconfirmed claims:
status-field commit names, credential type names, reconciler log commands, the resource-id annotation,
deletion detach annotation, drift-revert behaviour and reconciler resource overrides.
Method: documentation only; no commands were run.
