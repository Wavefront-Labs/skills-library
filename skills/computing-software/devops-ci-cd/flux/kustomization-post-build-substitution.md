---
id: computing-software.devops-ci-cd.flux.kustomization-post-build-substitution
name: kustomization-post-build-substitution
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, postbuild, substitute, substitutefrom, envsubst]
level: sme
status: docs-checked
description: "Inject per-cluster variables into manifests after kustomize build with postBuild.substitute and substituteFrom."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.postBuild.substitute` is a map of variables replaced in the final YAML after `kustomize build`. `.spec.postBuild.substituteFrom` loads variables from ConfigMaps and Secrets, using their data keys as variable names. Variable names must match `^[_[:alpha:]][_[:alpha:][:digit:]]*$`.

Supported bash-style forms: `${var:=default}`, `${var:position}`, `${var:position:length}`, `${var/substring/replacement}`.

Manifest:

```yaml
metadata:
  labels:
    environment: ${cluster_env:=dev}
    region: "${cluster_region}"
```

Kustomization:

```yaml
spec:
  postBuild:
    substitute:
      cluster_env: "prod"
    substituteFrom:
      - kind: ConfigMap
        name: cluster-vars
        optional: true
      - kind: Secret
        name: cluster-secret-vars
```

By default a missing referenced ConfigMap or Secret fails reconciliation. `optional: true` treats it as present but empty.

To react at once to changes in a referenced ConfigMap or Secret, label it `reconcile.fluxcd.io/watch: Enabled`, or start kustomize-controller with `--watch-configs-label-selector=owner!=helm`.

Numbers and booleans used as variable values must be enclosed in double quotes to be treated as strings. Inline `substitute` values take precedence over `substituteFrom`; among `substituteFrom` entries later values win. To avoid substitution in embedded scripts use `$var` instead of `${var}`, or `$${var}` to print `${var}`. Disable substitution on one object by labelling or annotating it `kustomize.toolkit.fluxcd.io/substitute: disabled`.

Undefined `${var}` values become an empty string unless a default is given. `.spec.postBuild.substituteStrategy` is `WithVariables` (default; substitution only runs if at least one variable is available) or `Always`.

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): `postBuild.substitute`/`substituteFrom`, variable-name regexp, supported `${var...}` forms, `optional`, precedence, `$${var}`, `substitute: disabled`, `substituteStrategy`, quoting of numbers and booleans, and the watch label and `--watch-configs-label-selector`. Replaced an unsupported 'define every variable' line with the documented empty-string behaviour.

Method: documentation only; no commands were run.
