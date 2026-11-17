---
id: computing-software.devops-ci-cd.kustomize.namespace-field
name: namespace-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [namespace, kustomization, transformer]
level: intro
status: docs-checked
description: "The namespace field sets or overrides metadata.namespace on all resources in a kustomization."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/namespace/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`namespace:` adds a namespace to all resources. It overrides the existing namespace when a resource already sets one, and adds it when the resource has none.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: kustomize-namespace
resources:
- deployment.yaml
```

With a Deployment that has `namespace: the-namespace`, the build output shows `namespace: kustomize-namespace`.

Points to remember:

- The field is a convenience for NamespaceTransformer, so more options exist if you configure it through `transformers` (see the namespace-transformer-options skill).
- Generators run before the namespace transformer. For `behavior: merge` or `replace` on a base ConfigMap, the overlay generator namespace must match the base ConfigMap's namespace as written, not the new one.
- The Kubernetes task page lists "setting the same namespace for all resources" as a standard cross-cutting field alongside prefix, suffix, labels and annotations.
- Combined example from the task page: `namespace: my-namespace`, `namePrefix: dev-`, `nameSuffix: "-001"` yields a Deployment named `dev-nginx-deployment-001` in `my-namespace`.

Create the Namespace object itself as a resource; the field sets references but does not generate the object.

## Checked

2026-11-03. Confirmed against: the namespace and configMapGenerator reference pages and the Kubernetes kustomization task page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
