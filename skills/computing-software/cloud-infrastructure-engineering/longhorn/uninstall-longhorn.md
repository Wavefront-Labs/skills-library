---
id: computing-software.cloud-infrastructure-engineering.longhorn.uninstall-longhorn
name: uninstall-longhorn
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [uninstall, deleting-confirmation-flag, helm-uninstall, webhooks, cleanup]
level: practitioner
status: docs-checked
description: "Uninstall Longhorn with Helm or kubectl: the deleting-confirmation-flag setting, workload deletion, Argo CD warning and webhook cleanup."
sources:
  - https://longhorn.io/docs/1.13.0/deploy/uninstall/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove Longhorn cleanly.

Prerequisites:
- Set `deleting-confirmation-flag` to `true` or the uninstall job fails:

```bash
kubectl -n longhorn-system patch -p '{"value": "true"}' --type=merge lhs deleting-confirmation-flag
```

- Delete workloads that use Longhorn volumes first (PV, PVC, StorageClass, Deployment, StatefulSet, DaemonSet and so on).

Helm: `helm uninstall longhorn -n longhorn-system`

kubectl:

```bash
kubectl create -f https://raw.githubusercontent.com/longhorn/longhorn/v1.13.0/uninstall/uninstall.yaml
kubectl get job/longhorn-uninstall -n longhorn-system -w
kubectl delete -f https://raw.githubusercontent.com/longhorn/longhorn/v1.13.0/deploy/longhorn.yaml
kubectl delete -f https://raw.githubusercontent.com/longhorn/longhorn/v1.13.0/uninstall/uninstall.yaml
```

Other tools: Rancher (delete the app in Catalog Apps), Helm Controller (`kubectl delete helmchart`), Fleet (delete the GitRepo, wait for the `longhorn-uninstall` job, then delete the manifest), Flux (`flux delete helmrelease longhorn-release -n longhorn-system`). Do not use `argocd app delete longhorn`: Argo CD lacks PreDelete hook support, leaving dangling resources.

Troubleshooting:
- A failed Helm or Rancher uninstall: check logs of the `longhorn-uninstall-xxx` pod; a `false` deletion flag is common.
- Cancel an accidental uninstall with `helm rollback longhorn <revision> -n longhorn-system`.
- Webhook errors (`service "longhorn-admission-webhook" not found`): delete leftover `longhorn-webhook-validator` and `longhorn-webhook-mutator` webhook configurations.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/deploy/uninstall/ : deleting-confirmation-flag, Helm, kubectl, Fleet, Flux, Argo CD guidance, rollback and webhook cleanup. Nothing else was removed.

Method: documentation only; no commands were run.
