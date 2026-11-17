---
id: computing-software.devops-ci-cd.kustomize.configmap-secret-task-flow
name: configmap-secret-task-flow
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [configmap, secret, generator, kubectl, tutorial]
level: intro
status: docs-checked
description: "Walk through generating ConfigMaps and Secrets with kubectl kustomize and consuming them from a Deployment by generator name."
sources:
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Kubernetes task page shows the generator workflow end to end. Create the kustomization and inspect the result with `kubectl kustomize ./`.

ConfigMap from a file (the page writes the files with shell here-documents; the content is):

```yaml
# application.properties contains: FOO=Bar
# kustomization.yaml
configMapGenerator:
- name: example-configmap-1
  files:
  - application.properties
```

`kubectl kustomize ./` outputs a ConfigMap named like `example-configmap-1-8mbdf7882g` with the file as one data item. Using `envs` with a `.env` file makes each variable its own key, which differs from the file example where the whole file is one key. Using `literals: [FOO=Bar]` creates keys directly.

To consume it, reference the generator name in the Deployment:

```yaml
volumes:
- name: config
  configMap:
    name: example-configmap-1
```

Kustomize replaces the name with the generated one, such as `example-configmap-1-g4hk9g2ff8`. The same works for Secrets: `secretGenerator` with `files: [password.txt]` yields `password.txt` base64 encoded with `type: Opaque`, and a Deployment volume references it with `secret: secretName: example-secret-1`.

Generated ConfigMaps and Secrets have a content hash suffix, which ensures a new ConfigMap or Secret is generated when contents change. To disable the suffix use `generatorOptions: {disableNameSuffixHash: true}`; the page also shows `labels: {type: generated}` and `annotations: {note: generated}` under `generatorOptions`.

## Checked

2026-11-08: read the Kubernetes kustomize task page in full; confirmed the file, env and literal ConfigMap examples, name replacement in the Deployment, the Secret examples and generatorOptions. Removed the verification tip about grepping `name:`, which the page does not give.

Method: documentation only; no commands were run.
