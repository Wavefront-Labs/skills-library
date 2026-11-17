---
id: computing-software.devops-ci-cd.kustomize.generated-name-hash-suffix
name: generated-name-hash-suffix
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [hash, rollout, configmap, secret, name-suffix]
level: practitioner
status: docs-checked
description: "Generated ConfigMaps and Secrets carry a content-hash name suffix that kustomize propagates to workloads, so a config change creates a new resource."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/namesuffix/
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Generated ConfigMaps and Secrets get a suffix derived from their contents, for example `my-java-server-env-vars-44k658k8gk`.

Why it matters: workloads reference the generated resource by the name in the generator (without the suffix). Kustomize identifies those references and updates them to the suffixed name. Changing the contents changes the suffix, which creates a new ConfigMap or Secret, and kustomize transforms the workloads to point to it.

Example on the Kubernetes task page: a Deployment volume says `configMap: name: example-configmap-1`; the build output rewrites it to `example-configmap-1-g4hk9g2ff8`.

Controls:

```yaml
generatorOptions:
  disableNameSuffixHash: true
```

This disables the default behaviour of adding a hash suffix to generated names. Per-entry control is `options.disableNameSuffixHash` inside a generator entry; if the global `generatorOptions` sets `disableNameSuffixHash: true`, that trumps any attempt to override it locally.

`nameSuffix` interplay: for ConfigMap and Secret, the configured suffix is appended before the content hash.

Gotcha: when an overlay `configMapGenerator` overrides an existing ConfigMap with `behavior: replace` or `merge`, it does not cause suffixing of the existing ConfigMap's name. To get suffixing, use the generator in the base; the overlay generator then updates the suffix from the new content. With merge or replace, name and namespace must match the target ConfigMap in the base.

## Checked

2026-11-08: confirmed against the configMapGenerator page (suffix example, name propagation, options.disableNameSuffixHash precedence, overlay suffix gotcha), the nameSuffix page (suffix goes before the hash) and the Kubernetes kustomize task page (example-configmap-1-g4hk9g2ff8 and the generatorOptions section). Removed the unsupported claims that pods roll as a result, that disabling the hash overwrites the old resource in place, and the replacements advice.

Method: documentation only; no commands were run.
