---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-image-garbage-collection
name: kubelet-image-garbage-collection
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, image-gc, imagegchighthreshold, serialize-image-pulls, container-gc, image-pull, disk-usage]
level: practitioner
status: docs-checked
description: "Tune kubelet image and container garbage collection (GC thresholds, max image age, dead container limits) and image pull concurrency so nodes neither fill disks nor thrash pulls."
sources: ["https://kubernetes.io/docs/concepts/architecture/garbage-collection/#containers-images", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://kubernetes.io/docs/concepts/containers/images/#serial-and-parallel-image-pulls", "https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubelet image and container garbage collection

## Image GC
The kubelet collects unused images every five minutes (unused containers every minute). Fields in
`KubeletConfiguration` with their documented defaults:
```yaml
imageGCHighThresholdPercent: 85    # disk usage above this triggers image GC (default 85)
imageGCLowThresholdPercent: 80     # GC deletes images until usage reaches this (default 80)
imageMinimumGCAge: 2m              # minimum age of an unused image before GC (default 2m)
imageMaximumGCAge: 168h            # delete images unused this long regardless of disk usage; default 0s (disabled)
```
Images are deleted starting with the least recently used. The kubelet's image GC ignores images pinned
by the container runtime. `imageMaximumGCAge` does not track usage across kubelet restarts: after a
restart the kubelet waits the full duration again. The kubelet's default hard eviction threshold
`imagefs.available` is 15%, i.e. 85% used, the same as the default high GC threshold; set the GC
high threshold below your eviction line if you want image GC to run before eviction.
Avoid external image-GC tools, which can break kubelet behaviour.

## Container GC
The Kubernetes garbage-collection page describes these variables: `MinAge` (minimum age before a
container can be collected; disable with 0), `MaxPerPodContainer` (maximum dead containers per pod;
disable with a negative value) and `MaxContainers` (maximum dead containers in total; disable with
a negative value). If the two maximums conflict, the kubelet lowers `MaxPerPodContainer`, in the worst
case to 1. Only containers managed by the kubelet are collected.

## Image pulls
```yaml
serializeImagePulls: true          # default: pull images one at a time
maxParallelImagePulls: 5           # only valid when serializeImagePulls is false; unset means no limit (stable in v1.35)
registryPullQPS: 5                 # default 5; 0 means no limit
registryBurst: 10                  # default 10
```
With `serializeImagePulls: false` the kubelet sends pull requests to the image service immediately; make
sure the container runtime's image service can handle parallel pulls. The kubelet never pulls multiple
images in parallel on behalf of one Pod (for example an init container and an app container).

## Observe and act
```bash
crictl images                            # list images on the node
crictl rmi --prune                       # remove unused images now (the crictl flag is "Remove all unused images"; pinned images are excluded)
kubectl get events -A --field-selector reason=FreeDiskSpaceFailed
kubectl get events -A --field-selector reason=ImageGCFailed
```
`FreeDiskSpaceFailed` (the kubelet source's message: "Insufficient free disk space on the node's image
filesystem ... Failed to free sufficient space by deleting unused images") usually means the disk is
full for reasons other than unused images (logs, volumes, other files) or an unusually large set of
in-use images; `ImageGCFailed` is emitted when the GC pass returns an error. Fix by investigating disk
usage, a larger disk, or fewer image variants.

## Gotchas
- A separate image filesystem (dedicated disk) means the thresholds apply to that disk.
- Images removed by GC must be pulled again the next time a pod needs them, so aggressive GC
  increases pull traffic and start times.

## Verify
- [ ] Image GC fires before DiskPressure on a fill test.
- [ ] No recurring `ImageGCFailed` or `FreeDiskSpaceFailed` events.

## Checked
Checked 2026-10-24 against the kubernetes/website Garbage Collection page (five-minute image GC and
one-minute container GC, thresholds, `imageMaximumGCAge`, container GC variables), the
`KubeletConfiguration` v1beta1 reference (defaults for the image GC, pull and eviction fields), the
Images page (parallel pulls, `maxParallelImagePulls` stable in v1.35), the kubelet image GC manager and
event source in kubernetes/kubernetes (pinned images, event reasons) and the cri-tools `crictl` source
(`rmi --prune`). Removed: the unverified claim that GC thresholds above eviction cause pod eviction
before GC finishes, and image-baking suggestions.
Method: documentation only; no commands were run.
