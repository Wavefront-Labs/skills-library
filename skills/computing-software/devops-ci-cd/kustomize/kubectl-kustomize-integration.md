---
id: computing-software.devops-ci-cd.kustomize.kubectl-kustomize-integration
name: kubectl-kustomize-integration
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [kubectl, apply, diff, delete, kustomize-flag]
level: intro
status: docs-checked
description: "Use kubectl kustomize and the -k flag to view, apply, diff, get, describe and delete objects managed by a kustomization directory."
sources:
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Since Kubernetes 1.14, kubectl also supports managing objects with a kustomization file. Use `--kustomize` or `-k` in kubectl commands; `-k` should point to a kustomization directory.

```bash
kubectl kustomize <kustomization_directory>   # view the resources
kubectl apply -k <kustomization_directory>/   # apply
kubectl get -k ./                              # view objects
kubectl describe -k ./                         # describe objects
kubectl diff -k ./                             # compare to the state if the manifest was applied
kubectl delete -k ./                           # delete objects
```

The task page's example: with `namePrefix: dev-`, labels `app: my-nginx` (`includeSelectors: true`) and `deployment.yaml` as a resource, `kubectl apply -k ./` outputs `deployment.apps/dev-my-nginx created`, and `kubectl delete -k ./` outputs `deployment.apps "dev-my-nginx" deleted`.

`kubectl diff -k` compares the Deployment object against the state the cluster would be in if the manifest was applied.

Kustomize is also a standalone tool. The page overview lists three kustomize features: generating resources from other sources, setting cross-cutting fields for resources, and composing and customizing collections of resources.

## Checked

2026-11-08: read the Kubernetes kustomize task page in full; confirmed the version, `-k`/`--kustomize` flag, the view, apply, get, describe, diff and delete commands, the example output and the three features. Removed the claims that teams can pin a newer standalone version than kubectl bundles and the `--dry-run=client` pipe suggestion, which the page does not state.

Method: documentation only; no commands were run.
