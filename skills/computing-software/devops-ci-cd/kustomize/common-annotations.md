---
id: computing-software.devops-ci-cd.kustomize.common-annotations
name: common-annotations
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [commonannotations, annotations, metadata]
level: intro
status: docs-checked
description: "commonAnnotations adds the same annotations to all resources, overriding values for keys that already exist."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/commonannotations/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`commonAnnotations` adds annotations to all resources. If the annotation key already exists on a resource, its value is overridden.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
commonAnnotations:
  oncallPager: 800-555-1212
resources:
- deploy.yaml
```

Build output: the Deployment gets `metadata.annotations.oncallPager: 800-555-1212`. The Kubernetes task page's cross-cutting example shows the annotation appearing on the Pod template too (`spec.template.metadata.annotations`) for a Deployment.

Under the hood the field is the AnnotationsTransformer. Through the `transformers` field you can set `fieldSpecs`:

```yaml
apiVersion: builtin
kind: AnnotationsTransformer
metadata:
  name: not-important-to-example
annotations:
  app: myApp
  greeting/morning: a string with blanks
fieldSpecs:
- path: metadata/annotations
  create: true
```

Arguments: `Annotations map[string]string` and `FieldSpecs`.

The built-ins page describes annotations as non-identifying metadata that, like labels, are key value pairs.

An existing key with the same name is overridden, so review the build output after adding the field.

## Checked

2026-11-03. Confirmed against: the commonAnnotations reference page, the Kustomize built-ins page and the Kubernetes kustomization task page.
Removed or reworded: the claim that annotations are safe on live objects, and the 'silently' wording.

Method: documentation only; no commands were run.
