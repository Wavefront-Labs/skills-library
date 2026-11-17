---
id: computing-software.cloud-infrastructure-engineering.crossplane.composition-function-install
name: composition-function-install
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function, package, install, healthy]
level: intro
status: docs-checked
description: "Install a composition function with a Function package object and read its INSTALLED and HEALTHY status."
sources:
  - https://docs.crossplane.io/latest/composition/compositions/
  - https://docs.crossplane.io/latest/packages/functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Installing a Function creates a function pod that Crossplane sends requests to. Create a `Function` object and set `spec.package` to the package location.

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.crossplane.io/crossplane-contrib/function-patch-and-transform:v0.8.2
```

The pod runs in the Crossplane namespace, `crossplane-system` by default. Functions are packages, so you install and configure them the same way as a provider.

Check status with:

```shell
kubectl get functions
```

During install the Function reports `INSTALLED` True and `HEALTHY` Unknown. When it is ready for use, `HEALTHY` becomes True.

`Function` objects are in the `pkg.crossplane.io` group; the `meta.pkg.crossplane.io` group is for creating Function packages.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Compositions page and Functions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: package-capabilities claim, install-order and health-gating claims, and the function-revision events advice.

Method: documentation only; no commands were run.
