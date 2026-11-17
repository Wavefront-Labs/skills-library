---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-autoscaler-safe-to-evict-annotations
name: opa-gatekeeper-autoscaler-safe-to-evict-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, cluster-autoscaler, helm, audit, annotations, emptydir, export]
level: advanced
status: docs-checked
description: "Let the Cluster Autoscaler scale down nodes that run the Gatekeeper audit pod by setting safe-to-evict-local-volumes, and avoid evicting violation-export volumes."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/install.md", "https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/audit.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper autoscaler safe to evict annotations

The audit pod mounts an `emptyDir` volume named `tmp-volume` for `/tmp/audit`. By default the Kubernetes Cluster Autoscaler refuses to downscale a node that hosts a pod with local storage. To allow it, pass the `safe-to-evict-local-volumes` annotation through Helm:

```sh
helm upgrade --install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system --create-namespace \
  --set-string 'auditPodAnnotations.cluster-autoscaler\.kubernetes\.io/safe-to-evict-local-volumes=tmp-volume'
```

Caveat: when violation export is enabled with `exportBackend=disk`, the audit pod has a second local volume, `tmp-violations` by default, holding results being handed to the export sidecar. Do not list it in the annotation unless you accept losing incomplete or unconsumed export files on eviction. To allow both explicitly, set `enableViolationExport=true`, `exportBackend=disk` and the annotation value `tmp-volume\,tmp-violations` (escaped comma). If you customised `audit.exportVolume.name`, use that name instead of `tmp-violations`.

Related tuning: the audit pod writes its API server cache to disk by default (v3.7.0+), which keeps memory low. Setting `audit.writeToRAMDisk=true` in Helm switches that cache to a tmpfs ramdisk (`emptyDir` with `medium: Memory`), which reduces IOPS but raises the audit pod memory footprint.

## Checked

2026-11-04. Confirmed against install.md (Configuring Pod Annotations for Cluster Autoscaler) and audit.md (audit cache RAM disk). Removed or corrected: a generic closing tip.

Method: documentation only; no commands were run.
