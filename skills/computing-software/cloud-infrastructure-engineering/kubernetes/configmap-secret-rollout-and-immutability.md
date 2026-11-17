---
id: computing-software.cloud-infrastructure-engineering.kubernetes.configmap-secret-rollout-and-immutability
name: configmap-secret-rollout-and-immutability
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, configmap, secret, volume-mount, subpath, env-from, kubelet-sync-period, immutable-configmap, checksum-config, rolling-restart, projected-volume, hot-reload]
level: practitioner
status: docs-checked
description: "Why workloads don't pick up ConfigMap/Secret changes the way people expect: volume sync delay, the subPath caveat, env vars never updating, and forcing a rollout."
sources: ["https://kubernetes.io/docs/concepts/configuration/configmap/", "https://kubernetes.io/docs/concepts/configuration/secret/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ConfigMap/Secret rollout and immutability: config doesn't push, it eventually syncs
**Goal:** stop assuming `kubectl apply` on a ConfigMap instantly changes running pod
behaviour, and know exactly which consumption method updates, when, and which never does.
## 1. Three consumption methods, three different update behaviours
- **Volume mount (whole ConfigMap/Secret as a directory)**: the kubelet checks the mounted
  data on every periodic sync, using a local cache whose type comes from
  `configMapAndSecretChangeDetectionStrategy` (watch by default, ttl-based, or direct API
  calls). The total delay can be as long as the kubelet sync period plus the cache
  propagation delay. The application has to notice the changed file itself.
- **Volume mount with `subPath`**: **does not receive updates**. If you need live updates,
  mount the whole ConfigMap into a directory and have the app read `<dir>/<file>`.
- **Environment variables** (`env.valueFrom.configMapKeyRef` or `envFrom`): ConfigMaps
  consumed as environment variables are not updated automatically and require a pod restart.
## 2. Forcing a pickup when nothing watches for you
A Deployment rolls out if and only if its pod template (`.spec.template`) changes. So:
- Put a hash of the ConfigMap/Secret content in a pod-template annotation; a content change
  changes the template and triggers a normal rolling update.
- Reference a new, versioned ConfigMap/Secret name from the template.
- `kubectl rollout restart deployment/<name>` restarts the pods manually after a config change.
## 3. Immutable ConfigMaps and Secrets
Setting `immutable: true` (stable since v1.21) means the data can no longer be changed:
you can only delete and recreate the object. Benefits: protection from accidental updates and,
for clusters with very many ConfigMap-to-Pod mounts, less kube-apiserver load because the
kubelet closes its watches on immutable objects. Each config change is then a new object
name, which means the Deployment's reference must change too; that name change is itself the
rollout trigger.
## Gotchas
- Secrets mounted as volumes follow the same kubelet sync period plus cache propagation
  delay as ConfigMaps, and `subPath` Secret mounts do not receive updates.
- The ConfigMap and Secret size limit is 1 MiB each.
## Verify
- [ ] Edit a plain-volume-mounted ConfigMap and confirm the file content inside a running
      pod changes after the sync window (`kubectl exec ... cat <path>`).
- [ ] Confirm a `subPath`-mounted file does **not** change under the same edit.
- [ ] Confirm an env-sourced value does not change without a pod restart.
- [ ] Any `immutable: true` object's consumers reference it by its versioned name.

## Checked
Checked 2026-10-24 against the ConfigMap, Secret, Configure a Pod to Use a ConfigMap and Deployment pages (website main, v1.37): update behaviour for volume, subPath and env consumption, `configMapAndSecretChangeDetectionStrategy`, delay = sync period plus cache propagation, immutable ConfigMaps and Secrets (stable v1.21, kubelet closes watches, delete and recreate only), a rollout starts if and only if the pod template changes, 1 MiB limit. Removed the unconfirmed tool names, `~1 minute` lag figure, Helm and Reloader details and the claim that the kubelet resync skips subPath files by design.
Method: documentation only; no commands were run.
