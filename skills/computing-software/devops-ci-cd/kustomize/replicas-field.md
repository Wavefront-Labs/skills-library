---
id: computing-software.devops-ci-cd.kustomize.replicas-field
name: replicas-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [replicas, scaling, deployment, statefulset]
level: intro
status: docs-checked
description: "Set replica counts per overlay with the replicas field, which matches by name across Deployment, ReplicaSet, ReplicationController and StatefulSet."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replicas/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`replicas` changes the replica count without a patch:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
replicas:
- name: deployment-name
  count: 5
resources:
- deployment.yaml
```

A Deployment with `replicas: 3` becomes 5. The field accepts a list so several resources can change at once.

The declaration takes no `kind` or `group`, so it matches any group and kind that has the matching name and is one of Deployment, ReplicationController, ReplicaSet or StatefulSet. If two kinds share a name, both change.

For more complex needs, revert to a patch; the reference page says so directly. The built-in behind this is ReplicaCountTransformer, whose `transformers` form accepts `replica` plus `fieldSpecs`:

```yaml
apiVersion: builtin
kind: ReplicaCountTransformer
metadata:
  name: not-important-to-example
replica:
  name: myapp
  count: 23
fieldSpecs:
- path: spec/replicas
  create: true
  kind: Deployment
- path: spec/replicas
  create: true
  kind: ReplicationController
```

Typical use: base has a small count, the prod overlay sets a larger `count` for the same `name`.

## Checked

2026-11-03. Confirmed against: the replicas reference page and the built-ins page (ReplicaCountTransformer).
Removed or reworded: the advice to use the original name.

Method: documentation only; no commands were run.
