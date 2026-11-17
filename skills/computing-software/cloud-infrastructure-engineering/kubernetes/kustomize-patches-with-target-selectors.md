---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kustomize-patches-with-target-selectors
name: kustomize-patches-with-target-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kustomize, patch-target, json6902, strategic-merge-patch, overlays]
level: practitioner
status: verified
description: "Apply one Kustomize patch to many resources with target selectors (kind, name regex, labelSelector, annotationSelector), using strategic merge or JSON 6902 patches."
sources: ["https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/", "https://kubectl.docs.kubernetes.io/references/kustomize/glossary/#target"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kustomize patches with target selectors

## JSON 6902 patch on every matching Deployment
```yaml
# kustomization.yaml
resources: [../../base]
patches:
- target:
    group: apps
    version: v1
    kind: Deployment
    labelSelector: "tier=web"
  patch: |-
    - op: add
      path: /spec/template/spec/containers/0/env/-
      value: {name: OTEL_EXPORTER_OTLP_ENDPOINT, value: "http://otel-collector:4317"}
```

## Strategic merge patch applied to many objects
```yaml
patches:
- target:
    kind: Deployment
    name: "api-.*"                # regex on names
    annotationSelector: "team=payments"
  patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ignored-when-target-is-set
    spec:
      template:
        spec:
          nodeSelector: {pool: payments}
```
With a `target`, the name in the patch body is ignored and the patch applies to every match.

## Target fields
`group`, `version`, `kind`, `name` (regex), `namespace`, `labelSelector`, `annotationSelector`.
All given fields must match.

## Gotchas
- JSON 6902 `add` to `/env/-` fails if `env` does not exist; add it with a strategic merge patch,
  or use `op: add` on `/env` with a full list for bases without env.
- Container index paths (`/containers/0`) break when containers are reordered; use strategic
  merge with the container name when possible.
- A selector matching nothing is silent; check output.

## Verify
```bash
kustomize build overlays/prod | yq 'select(.kind=="Deployment") | [.metadata.name, .spec.template.spec.nodeSelector]'
```
Every intended Deployment shows the change and no others do.

## Checked
- `kubectl kustomize` (Kustomize 5.0.4, kubectl 1.30.3) on a scratch base with two Deployments: JSON 6902 `add` to `/env/-` fails with "doc is missing path" when `env` is absent and works when present, `labelSelector` and `annotationSelector` targets match as described, a regex `name` plus `annotationSelector` patched only the matching Deployment and ignored the patch body's own name, a selector that matches nothing builds silently (exit 0), and the yq verification command printed the expected name and nodeSelector (mikefarah yq 4.54.1).
