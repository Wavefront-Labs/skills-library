---
id: computing-software.cloud-infrastructure-engineering.kubernetes.csi-driver-architecture
name: csi-driver-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, csi, container-storage-interface, csi-controller, csi-node, sidecar, external-provisioner, external-attacher, external-resizer, external-snapshotter, node-driver-registrar, livenessprobe, grpc, csidriver, csinode, volumeattachment, storage-architecture]
level: advanced
status: docs-checked
description: "How a CSI driver is actually wired into Kubernetes: controller vs node plugin, the sidecar containers, and the gRPC calls behind every PVC."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#csi", "https://kubernetes-csi.github.io/docs/introduction.html", "https://kubernetes-csi.github.io/docs/sidecar-containers.html", "https://kubernetes-csi.github.io/docs/node-driver-registrar.html", "https://kubernetes-csi.github.io/docs/csi-node-object.html", "https://kubernetes-csi.github.io/docs/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSI driver architecture — what actually runs when a PVC gets a disk

**Goal:** know which process does what when a PVC goes Pending → Bound → mounted, so
you can read logs from the right container instead of guessing.

## 1. Two plugins, not one
A CSI driver ships as (at least) two Deployments/DaemonSets, both wrapping the same
driver binary over a Unix domain socket, speaking CSI's gRPC spec:
- **Controller plugin** — usually a `Deployment` (the CSI deployment guide recommends leader election so only one replica is active). Talks
  to the cloud/storage API: `CreateVolume`, `DeleteVolume`, `ControllerPublishVolume`
  (attach), `ControllerExpandVolume`, `CreateSnapshot`.
- **Node plugin** — a `DaemonSet`, one pod per node, privileged, host-mounted. Talks to
  the local kernel: `NodeStageVolume` (format + mount to a staging path),
  `NodePublishVolume` (bind-mount staging path into the pod's volume dir),
  `NodeUnpublishVolume`, `NodeUnstageVolume`.

Each plugin pod is the driver container plus **sidecars** — this is where 90% of
"why is my PVC stuck" logs actually live, not in the driver container itself:
- `external-provisioner` (controller) — watches PVCs, calls `CreateVolume`.
- `external-attacher` (controller) — watches `VolumeAttachment` objects, calls
  `ControllerPublishVolume`/`Unpublish`.
- `external-resizer` (controller) — watches PVC size edits, calls `ControllerExpandVolume`.
- `external-snapshotter` + `snapshot-controller` (controller, cluster-wide) — implement
  `VolumeSnapshot`/`VolumeSnapshotContent`, call `CreateSnapshot`.
- `node-driver-registrar` (node) — fetches the driver's `NodeGetInfo` and registers the driver's
  socket with kubelet via the kubelet plugin registration mechanism; kubelet then maintains the
  `CSINode` object. The `CSIDriver` object is created separately by whoever installs the driver.
- `livenessprobe` (both) — monitors the driver's health and reports it to Kubernetes through the
  liveness probe mechanism, so a wedged driver can be restarted.

## 2. The lifecycle, call by call
1. PVC created → `external-provisioner` sees it, calls `CreateVolume` (controller) →
   disk exists in the cloud, PV object created.
2. Scheduler places the pod → a `VolumeAttachment` object is created for the volume and node;
   `external-attacher` watches `VolumeAttachment` objects and calls `ControllerPublishVolume`
   → disk attached to the node (only for drivers that advertise the `PUBLISH_UNPUBLISH_VOLUME`
   controller capability).
3. kubelet on that node calls the **node plugin directly** (no sidecar in between):
   `NodeStageVolume` (stage the volume on the node), then `NodePublishVolume` (make it
   available at the pod's volume path).
4. Pod deleted → reverse order: `NodeUnpublish` → `NodeUnstage` → (if no other pod on
   that node needs it) `ControllerUnpublish` (detach) → eventually `DeleteVolume` if the
   PVC itself is deleted and `reclaimPolicy: Delete`.

## 3. Where to actually look when something's stuck
- PVC stuck Pending: `kubectl describe pvc` events first (often enough), then
  `external-provisioner` container logs in the controller pod.
- Pod stuck `ContainerCreating` with a volume mount error: `kubectl describe pod` for
  the volume events, then the **node plugin** pod on that specific node
  (`kubectl get pods -n <csi-namespace> -o wide` shows which node each pod runs on), not the
  controller — stage/publish is node-local, because kubelet calls the node plugin directly.
- Attach problems (for example a Multi-Attach error on a volume still attached to another
  node): inspect the `VolumeAttachment` objects (`kubectl get volumeattachment`), which
  `external-attacher` acts on, and check that node's state before changing anything;
  force-detaching a volume that is still in use risks data loss.
- `CSINode` object (`kubectl get csinode <node> -o yaml`) lists the drivers registered on the node,
  the node ID the driver reported, and its topology keys.

## Gotchas
- The node plugin needs privileged host access (the CSI docs note containerized node plugins are
  typically deployed as privileged containers on Linux); follow the driver's own install manifest.
- Sidecars are released and versioned separately from the driver, each with its own compatibility
  table (supported Kubernetes versions and CSI spec versions) in the kubernetes-csi docs; use the
  sidecar versions your driver's install manifest specifies.
- With leader election, only one controller replica is active; check which replica holds the lease before reading logs.

## Verify
- [ ] `kubectl get pods -n <csi-namespace> -o wide` and name each sidecar container in
      the controller and node pods for your installed driver.
- [ ] `kubectl get csidriver,csinode` and read the capabilities reported.
- [ ] Traced one PVC's full create→attach→mount path through the right container's logs.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: kubelet calls NodeGetInfo/NodeStageVolume/NodePublishVolume directly; node-driver-registrar registers via the plugin registration mechanism and kubelet manages CSINode; external-attacher watches VolumeAttachment and needs the PUBLISH_UNPUBLISH_VOLUME capability; livenessprobe reports via the liveness probe mechanism; leader election recommended for controller replicas. Removed unconfirmed details (replica counts, /healthz, staging paths, deletion advice, sidecar-version claims kept only as general advice).

Method: documentation only; no commands were run.
