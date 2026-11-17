---
id: computing-software.cloud-infrastructure-engineering.openebs.troubleshoot-replicated-storage-logs-known-issues
name: troubleshoot-replicated-storage-logs-known-issues
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [troubleshooting, replicated-pv-mayastor, logs, coredump, gdb, sigill, diskpool-schema, multipath, high-availability]
level: advanced
status: docs-checked
description: "Diagnose Replicated PV Mayastor: pod logs to collect, coredumps with systemd-coredump and gdb, DiskPool v1beta2 schema errors, SIGILL exit 132, and known issues."
sources:
  - https://openebs.io/docs/troubleshootingre
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Logs.** If unsure, collect logs from every Replicated Storage container; nearly always you need the control plane pods: `csi-controller`, `core-agent`, `rest` and `msp-operator`. The data plane (the io-engine pods) log is the most useful for I/O errors, though also provisioning and management faults can show there. For mount or unmount problems on an application node, read the CSI node agent pod on that node. The CSI sidecars run in the same pods as the controller and node plugin and can hold useful detail when those fail.

**Coredumps.** The steps apply specifically to Ubuntu per the page. It relies on `systemd-coredump`, the `coredumpctl` utility and `gdb`. After installing, verify the global core pattern pipes dumps to systemd-coredump and list dumps. A coredump alone is of little use: copy the relevant parts of the crashed container's filesystem so gdb can find the binary, extract the compressed dump, open it in gdb, set the sysroot and print backtraces for all threads. **Do not start gdb with `coredumpctl`**; it passes an invalid binary path and Rust stack unwinding fails.

**DiskPool schema errors after upgrading to 2.4 or later.** `kubectl get dsp -n openebs` may fail because of old `v1alpha1` or `v1beta1` entries in the discovery cache; run `kubectl get diskpools.openebs.io -n openebs` once to refresh it to `v1beta2`. When creating a pool, use `apiVersion: openebs.io/v1beta2` in the YAML, and check with `kubectl get crd diskpools.openebs.io`.

**IO engine pod restarts with exit code 132 while mounting a PVC.** The process received SIGILL: the node CPU lacks the required instruction set (SSE4.2 on x86-64).

**Known limitation.** The page's heading says volumes are highly durable but, without multipathing, not highly available. Replicas keep synchronously mirrored copies on more than one node and pool, but a volume is reachable through a single NVMe-oF target in a single Replicated Storage pod. If that pod stops running, the HA switch-over module detects it and moves the target to a healthy worker node.

**Other known issues the page lists:**

- *IOVA error at io-engine start* (`couldn't allocate memory due to IOVA exceeding limits of current DMA mask`): likely IOMMU is enabled; set `--set mayastor.io_engine.envcontext=iova-mode=pa` at install.
- *Long node reboot times* with Replicated Storage volumes mounted, because of the long default NVMe `ctrl_loss_tmo`: cordon the node and clear application pods first; the `ioTimeout` StorageClass parameter can tune it.
- *Node restart when an app is scheduled* on a node running Replicated Storage with the Prometheus exporter, a kernel bug: use kernel 5.13 or later.
- *xfs mount failure* on kernels older than 5.10 from newer xfsprogs options: upgrade the kernel to 5.10 or higher.
- *Pod may restart if a pool disk becomes inaccessible*; a fix was under investigation.
- *RKE on Fedora CoreOS* needs the `/opt/rke/var/lib/kubelet/plugins:/var/lib/kubelet/plugins` bind in `services_kublet->extra_binds`, or CSI driver registration fails.
- *Loki MinIO pods in ImagePullBackOff* on OpenEBS v4.3.0 through v4.6.1 (images from quay.io/minio): upgrade to v4.6.2 or later, which uses the docker.io/openebs mirrors.

## Checked

Method: 2026-11-08 read the raw markdown of the cited Replicated Storage troubleshooting page in full; logs, coredump, DiskPool schema and SIGILL entries match. Noted that the coredump steps are Ubuntu-specific, corrected the known-limitation entry (the page says HA switch-over moves the target) and added the other known issues the page lists.
