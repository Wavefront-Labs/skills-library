---
id: computing-software.cloud-infrastructure-engineering.kubernetes.configmap-update-propagation
name: configmap-update-propagation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, configmap, configmap-propagation-delay, subpath, volume-mount, secrets]
level: practitioner
status: docs-checked
description: "How and when ConfigMap and Secret changes reach running pods: volume sync delay, subPath and env never updating, symlink swaps, and reload strategies."
sources: ["https://kubernetes.io/docs/concepts/configuration/configmap/#mounted-configmaps-are-updated-automatically", "https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod", "https://github.com/kubernetes/kubernetes/blob/master/pkg/volume/util/atomic_writer.go", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ConfigMap and Secret update propagation

## Who sees an update
| Consumption | Updated in running pod? |
|---|---|
| Volume mount (whole ConfigMap/Secret) | yes, eventually |
| Volume with `subPath` | **never** |
| `env` / `envFrom` | **never** (process env is fixed at start) |
| Projected volume | yes, like volumes |
| Immutable ConfigMap/Secret | cannot change; create a new one |

## Delay
The kubelet checks mounted ConfigMaps on every periodic sync, using its local cache whose type is set by
`configMapAndSecretChangeDetectionStrategy` (watch by default, or ttl-based, or direct API calls). The total delay can be as long as the kubelet
sync period plus the cache propagation delay of the chosen cache type.

## Mechanism (why apps miss updates)
The visible files are symlinks to files in a hidden timestamped directory, and a `..data` symlink points at the current one. The kubelet
writes new content and swaps the `..data` symlink (kubelet atomic writer). Consumers can monitor the `..data` symlink using inotify rather than the individual files.

## Reload strategies
1. App watches the mounted dir and reloads (best, no restart).
2. Restart on change: a hash of the config in a pod-template annotation changes `.spec.template`, which triggers a rollout; `kubectl rollout restart` does it manually.
3. Immutable, versioned ConfigMaps (`app-config-v7`) referenced from the template: a name change is a template change, so it triggers a rollout.

## Verify
```bash
kubectl exec <pod> -- ls -la /etc/config/          # ..data symlink timestamp
kubectl exec <pod> -- cat /etc/config/app.conf
```
Change the ConfigMap, then poll the file; if it never updates, check for subPath in the pod spec.

## Checked
Checked 2026-10-24 against the ConfigMap, Secret and Configure a Pod to Use a ConfigMap pages (website main, v1.37) and the kubelet atomic writer source: volume updates are eventual, delay = kubelet sync period plus cache propagation (watch default, ttl-based or API), subPath mounts never update, env vars never update, projected content is eventually updated, the `..data` symlink and inotify note, immutable objects, a rollout starts only when the pod template changes. Removed the 60-90 s estimate, the timestamp format, `IN_*` event names and the Helm, reloader and sidecar specifics.
Method: documentation only; no commands were run.
