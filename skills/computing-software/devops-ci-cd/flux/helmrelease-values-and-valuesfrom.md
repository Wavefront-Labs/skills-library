---
id: computing-software.devops-ci-cd.flux.helmrelease-values-and-valuesfrom
name: helmrelease-values-and-valuesfrom
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, values, valuesfrom, targetpath, configmap-secret]
level: sme
status: docs-checked
description: "Merge inline values with ConfigMap and Secret values in a HelmRelease, including targetPath, optional and literal."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Helm values come from `.spec.valuesFrom` and `.spec.values`. Changes to the combined values trigger a new release.

Merge order: `valuesFrom` entries in order (later wins), then inline `.spec.values` overrides them. An entry with `targetPath` overwrites everything before it, including inline values.

Fields of a `valuesFrom` item:
- `kind`: `ConfigMap` or `Secret`, in the HelmRelease namespace.
- `name`.
- `valuesKey`: data key; defaults to `values.yaml`.
- `targetPath`: YAML dot path where a single flat value is merged, for example `tls.crt`.
- `optional`: a missing referent is ignored; bad keys or paths and transient errors still fail.
- `literal`: with `targetPath`, merge verbatim without Helm `--set` parsing (commas, brackets, dots), like `helm --set-literal`. Good for config files or JSON blobs.

```yaml
spec:
  values:
    replicaCount: 2
  valuesFrom:
    - kind: ConfigMap
      name: prod-env-values
      valuesKey: values-prod.yaml
    - kind: Secret
      name: prod-tls-values
      valuesKey: crt
      targetPath: tls.crt
      optional: true
```

To react at once to changes in a referenced ConfigMap or Secret, label it `reconcile.fluxcd.io/watch: Enabled`.

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/): valuesFrom fields and merge order, `optional`, `literal` (helm --set-literal), `targetPath` and the `reconcile.fluxcd.io/watch: Enabled` label. Removed an unsupported advice sentence about SOPS.

Method: documentation only; no commands were run.
