---
id: computing-software.cloud-infrastructure-engineering.crossplane.image-config-rewrite-pull
name: image-config-rewrite-pull
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [imageconfig, registry, mirror, pull-secret, rewriteimage]
level: advanced
status: docs-checked
description: "Centralize registry pull secrets and mirror rewrites for package images with ImageConfig."
sources:
  - https://docs.crossplane.io/latest/packages/image-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An `ImageConfig` applies to packages without being referenced. `spec.matchImages` lists `Prefix` matches (no wildcards; `type` defaults to `Prefix`). With overlapping configs, the longest prefix wins.

Pull secret:

```yaml
apiVersion: pkg.crossplane.io/v1beta1
kind: ImageConfig
metadata:
  name: acme-packages
spec:
  matchImages:
  - prefix: registry1.com/acme-co/
  registry:
    authentication:
      pullSecretRef:
        name: acme-registry-credentials
```

The secret must be type `kubernetes.io/dockerconfigjson` in the Crossplane namespace, created with `kubectl -n crossplane-system create secret docker-registry ...`.

Mirror rewrite swaps the matched prefix:

```yaml
spec:
  matchImages:
  - prefix: xpkg.crossplane.io
  rewriteImage:
    prefix: registry1.com
```

This also redirects dependencies, which would otherwise still pull from `xpkg.crossplane.io`. `spec.package` is unchanged; the result appears in `status.resolvedPackage`. Rewriting runs first, so other ImageConfigs must match the rewritten path.

`spec.runtime.configRef` can assign a DeploymentRuntimeConfig to matching packages, including dependencies. It takes precedence over the package's `runtimeConfigRef`, and `status.appliedImageConfigRefs` records `ConfigureRuntime`.

Use one ImageConfig per registry host.

## Checked

Matching, longest-prefix rule, pull secret, rewriteImage, dependency redirect, status fields and runtime configRef confirmed on the Image Configs page. An unsourced air-gapped usage claim was removed.

Method: docs-checked 2026-11-09 against the raw Image Configs page (docs repo, current content folder), read in full.
