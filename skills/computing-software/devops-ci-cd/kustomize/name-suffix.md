---
id: computing-software.devops-ci-cd.kustomize.name-suffix
name: name-suffix
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [namesuffix, names, hash, configmap]
level: intro
status: docs-checked
description: "nameSuffix appends text to every resource name; for ConfigMaps and Secrets it is added before the content hash."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/namesuffix/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`nameSuffix` appends the value to the names of all resources and references.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
nameSuffix: -custom-suffix
resources:
- deployment.yaml
```

Result: `the-deployment` becomes `the-deployment-custom-suffix`.

The built-ins page adds a detail about the PrefixSuffixTransformer, which handles both `namePrefix` and `nameSuffix`: the suffix is appended before the content hash if the resource type is ConfigMap or Secret. So a generated ConfigMap ends up like `name-suffix-<hash>`, not `name-<hash>-suffix`.

Examples from the built-ins page: a Deployment named `wordpress` could become `alices-wordpress`, `wordpress-v2` or `alices-wordpress-v2` using `namePrefix: alices-` and `nameSuffix: -v2`.

If a value starts with a hyphen, quote it in YAML so it parses as a string, as the task page does with `nameSuffix: "-001"`.

Use cases: version a release (`-v2`) so two copies run side by side, or mark a numbered instance. Like `namePrefix`, references between resources inside the project follow the rename.

Check the result with kustomize build and look at metadata.name and the references to the renamed object.

## Checked

2026-11-03. Confirmed against: the nameSuffix reference page, the built-ins page and the task page.
Removed or reworded: the Service/ConfigMap/Secret list for suffix references.

Method: documentation only; no commands were run.
