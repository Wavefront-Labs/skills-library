---
id: computing-software.devops-ci-cd.kustomize.name-prefix
name: name-prefix
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [nameprefix, names, references, transformer]
level: intro
status: docs-checked
description: "namePrefix prepends a string to every resource name and propagates the new name to references such as Services, ConfigMaps and Secrets."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/nameprefix/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`namePrefix` prepends the value to the names of all resources and references.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namePrefix: custom-prefix-
resources:
- deployment.yaml
```

A Deployment named `the-deployment` builds as `custom-prefix-the-deployment`.

References are updated too. The page lists: Service references from StatefulSets, ConfigMap references from PodSpecs, and Secret references from PodSpecs. That is why you should never hard-code a prefixed name in another object when kustomize can follow the reference.

For names embedded in places kustomize does not know (a command-line argument, for instance), use `replacements` to copy the final `metadata.name` rather than typing it. The task page demonstrates this with `namePrefix: dev-` and `nameSuffix: "-001"` and a `replacements` source of the Service name, producing `dev-my-nginx-001` in a container command.

Overlay use: put `namePrefix: dev-` in `dev/kustomization.yaml` and `namePrefix: prod-` in `prod/kustomization.yaml` over the same base, as the task page does.

The page example writes the trailing hyphen into the value (`custom-prefix-`).

## Checked

2026-11-03. Confirmed against: the namePrefix reference page, the built-ins page and the Kubernetes kustomization task page.
Removed or reworded: the claim that kustomize concatenates exactly what you write.

Method: documentation only; no commands were run.
