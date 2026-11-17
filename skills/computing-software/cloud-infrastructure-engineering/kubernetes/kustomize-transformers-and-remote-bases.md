---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kustomize-transformers-and-remote-bases
name: kustomize-transformers-and-remote-bases
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kustomize, images-transformer, nameprefix, commonlabels, labels-transformer, remote-base, kustomize-remote, replacements, kustomize-edit, namespace-transformer]
level: practitioner
status: verified
description: "Use Kustomize built-in transformers (images, namePrefix/Suffix, labels vs commonLabels, namespace, replacements) and pin remote bases to immutable refs safely."
sources: ["https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/", "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/resource/", "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Kustomize transformers and remote bases

## Built-in transformers
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: payments-prod
namePrefix: prod-
nameSuffix: -v2
labels:
- pairs: {app.kubernetes.io/part-of: payments, env: prod}
  includeSelectors: false        # metadata only; safe to add later
  includeTemplates: true         # also pod template labels
images:
- name: ghcr.io/acme/payments    # matches image name in manifests
  newName: registry.internal/acme/payments
  newTag: "1.8.3"
  # digest: sha256:...           # pins; overrides tag
replicas:
- {name: payments, count: 4}
resources:
- ../../base
```
- **`commonLabels` is deprecated** (5.8.3 warns; `kustomize edit fix` converts it to `labels:` with
  `includeSelectors: true`, so the selector hazard survives the conversion) and also rewrites **selectors** — adding/changing one on an
  existing Deployment changes its immutable `spec.selector` → apply fails. Use `labels:` with
  `includeSelectors: false` for anything added after first deploy.
- `namePrefix/Suffix` also updates references Kustomize knows (configMapRef, secretRef,
  serviceName in Ingress, etc.); references inside CRDs need a `configurations:` nameReference
  entry or they break (run: a `Widget.spec.configName` stayed `cm` while the ConfigMap became `p-cm`; with a
  `nameReference` entry for path `spec/configName` it became `p-cm`).
- `namespace:` overrides all namespaced resources, including ones that deliberately live
  elsewhere — split those into another kustomization.
- `images:` with `kustomize edit set image ghcr.io/acme/payments=:1.8.4` from CI.

## replacements (successor of vars)
```yaml
replacements:
- source: {kind: Service, name: db, fieldPath: metadata.name}
  targets:
  - select: {kind: Deployment, name: payments}
    fieldPaths: ["spec.template.spec.containers.[name=app].env.[name=DB_HOST].value"]
```

## Remote bases
```yaml
resources:
- https://github.com/acme/platform-bases//apps/web?ref=v2.4.1        # tag
- github.com/acme/platform-bases//monitoring?ref=3f2c9e1a7b...      # commit SHA (best)
- https://raw.githubusercontent.com/org/repo/v1.0.0/deploy/crds.yaml  # single file URL
```
- Always pin `?ref=` to a tag or **commit SHA**; branch refs make builds non-reproducible.
- Remote fetch uses `git` on the build host — CI/Argo CD repo-server need network and creds;
  air-gapped setups must vendor (`git subtree`/copy) instead.
- Builds are slower (clone per build); Argo CD caches per revision.
- Security: a remote base can introduce any resource (ClusterRoleBinding...) — review diffs on
  ref bumps (Renovate PRs + `kustomize build | kubectl diff`).

## Verify
```bash
kustomize build overlays/prod | kubeconform -strict -summary -kubernetes-version 1.33.0
kustomize build overlays/prod | grep 'image:'
# with a cluster: kustomize build overlays/prod | kubectl apply --dry-run=server -f -   (not run here)
```
- [ ] No `commonLabels` in overlays of existing apps; all remote refs pinned.
