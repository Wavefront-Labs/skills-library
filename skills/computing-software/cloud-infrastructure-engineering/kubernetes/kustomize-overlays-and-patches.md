---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kustomize-overlays-and-patches
name: kustomize-overlays-and-patches
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kustomize, kustomization-yaml, bases-and-overlays, strategic-merge-patch, json6902, patchesstrategicmerge, patchesjson6902, components, configmapgenerator, secretgenerator, namereference, replacements, vars-deprecated, kubectl-kustomize, gitops, environment-overlays]
level: practitioner
status: verified
description: "Structure Kustomize bases and overlays: strategic-merge vs JSON6902 patches, components, generators, and the pitfalls that break builds."
sources: ["Kustomize docs (kubectl-sigs/kustomize)", "Kubernetes docs - Declarative Management with Kustomize"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kustomize overlays and patches — environment-specific manifests without templating

**Goal:** one base of plain YAML, N environment overlays that each produce a correct,
diffable manifest set via `kustomize build`, with no Go templating and no values file.

## 1. Layout
```
base/
  kustomization.yaml     # resources: [deployment.yaml, service.yaml]
  deployment.yaml service.yaml
overlays/
  dev/kustomization.yaml       # resources: [../../base]
  staging/kustomization.yaml
  prod/kustomization.yaml
    patches: [...]
    namePrefix: prod-
    namespace: prod
```
`kustomize build overlays/prod` (or `kubectl kustomize overlays/prod`, or
`kubectl apply -k overlays/prod`) renders. Never apply `base/` directly in a real
environment — overlays are where namespace, replicas and resource limits differ.

## 2. Patch types — pick the right one
- **Strategic merge patch** (`patches:` with a partial YAML object matching
  `kind`/`metadata.name`): good for adding/overriding fields, merges by K8s merge-key
  semantics (e.g. appends to `containers` by `name`). Cannot delete a list item cleanly
  without `$patch: delete` on that element, and cannot target by array index.
- **JSON6902 patch** (`patches:` with `target:` + `path:` to an RFC 6902 ops file, or
  inline `patch: |-`): required when you need to **remove** a field/array element, or
  patch something strategic-merge can't address. Ops are positional (`/spec/replicas`,
  `/spec/template/spec/containers/0/image`) — fragile if the base reorders containers.
- Legacy `patchesStrategicMerge:`/`patchesJson6902:` keys still build but print a deprecation warning
  (5.8.3); `kustomize edit fix` rewrites them into the unified `patches:` list. Prefer that form.

## 3. Generators and name/hash behaviour
- `configMapGenerator` / `secretGenerator` append a content hash to the generated
  name (`app-config-7d8f9c6b2`) and Kustomize rewrites every reference to that name
  automatically (`nameReference` transformer) — this is **why** you use the generator
  instead of a static ConfigMap: it forces a rollout on content change without a
  manual checksum annotation.
- `disableNameSuffixHash: true` (under `generatorOptions`, in the kustomization that defines the generator; set in
  an overlay it did not affect the base's generator on 5.8.3) turns that off — then you own rollout-on-change
  yourself (e.g. an explicit pod annotation), usually not worth doing.
- `secretGenerator` with `literals:`/`envs:` puts plaintext into the rendered
  manifest and into git if committed — fine for non-secret config, never for real
  secrets; see `computing-software.cloud-infrastructure-engineering.kubernetes.sops-encrypted-secrets-in-git`
  or the external-secrets/sealed-secrets skills for the real answer.

## 4. Components vs overlays
- A **component** (`kind: Component`) is an optional, composable chunk of
  patches/resources an overlay can opt into (`components: [../../components/debug-sidecar]`).
  Use when a feature (e.g. a sidecar, a feature-flag patch) applies to *some but not
  all* overlays — overlays alone force either duplicating the patch or inventing a
  deeper overlay-of-overlay hierarchy.
- `replacements:` (the modern form; `vars:` is deprecated) propagates a value from one
  resource field into another by JSONPath, e.g. the generated ConfigMap name into an
  env var — safer than string templating because it fails the build if the source
  path doesn't exist (`fieldPath ... is missing for replacement source`, run on 5.8.3). Run on 5.8.3, a
  replacement sourced from `metadata.name` of a generated ConfigMap injects the unhashed name (`app-config`),
  not the suffixed one, so do not use it to wire a hashed ConfigMap reference; let `nameReference` do that.

## Gotchas
- `kustomize build` output order is **not** the order resources are listed; don't
  assume apply ordering — that's what Argo CD sync waves or `depends-on` are for.
- Patches apply in list order; two patches touching the same path silently let the
  later one win — no warning (run: `replicas: 2` then `replicas: 5` built as 5).
- `namePrefix`/`nameSuffix` apply to *all* resources in the tree. Kustomize also rewrites references to them:
  a ClusterRoleBinding's ServiceAccount `subjects[].name` follows the renamed account and `subjects[].namespace`
  becomes the overlay namespace (kubectl 1.30 / Kustomize 5.0.4). Check RBAC subjects that point at accounts
  outside the tree.
- Remote bases (`resources: [github.com/org/repo/base?ref=v1.2.0]`) pin by git ref (tag, branch or commit SHA per
  the Kustomize `remoteBuild.md` example); a branch name or no `ref` is a moving target, so pin a tag or SHA. Large repos
  can hit the default clone timeout (about 27 s seen on 5.8.3); add `&timeout=120`.
- Helm users layering Kustomize on top: `helmCharts:` (built-in Helm inflator) renders
  then patches, but has weaker control over Helm hook ordering than templating with
  Helm directly — see `kustomize-helm-postrender-and-chart-inflator` for the tradeoffs
  and the alternative (Argo CD `--enable-helm` postRenderer).

## Verify
- [ ] `kustomize build overlays/<env>` for every overlay produces valid YAML
      (`kubeconform -strict`) with no unresolved `$patch` markers.
- [ ] Diff `overlays/staging` vs `overlays/prod` output — the only differences are
      the ones you intend (replica count, resource limits, image tag), nothing
      accidentally diverged.
- [ ] A changed `configMapGenerator` literal produces a new hash suffix and the
      Deployment's volume/env reference updates to match.
- [ ] JSON6902 patches still apply after a base container reorder (or you've pinned
      by name-based strategic merge instead of index).
