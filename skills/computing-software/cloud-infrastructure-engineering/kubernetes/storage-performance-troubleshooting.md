---
id: computing-software.cloud-infrastructure-engineering.kubernetes.storage-performance-troubleshooting
name: storage-performance-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, storage-performance, fio, iostat, cgroup, io-throttling, noisy-neighbor, iops, latency, ebs-burst-balance, blkio, cadvisor, container-storage-interface]
level: advanced
status: docs-checked
description: "Diagnosing slow PVC I/O on Kubernetes: isolating app vs. node vs. cgroup vs. cloud-disk-tier causes, with fio and iostat commands to run from inside the pod."
sources: ["https://github.com/axboe/fio/blob/master/HOWTO.rst", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/parameters.md", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/cgroup-v2.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage performance troubleshooting

**Goal:** when a database on a PVC is slow, work out whether the disk tier, a throttle, cgroup limits, or a noisy neighbour is the cause.

## 1. Rule out the application first
Confirm the application itself reports I/O wait or latency (database wait events and I/O metrics) rather than CPU starvation or lock contention.

## 2. Benchmark from inside the Pod
fio options used here are documented in the fio HOWTO: `--name`, `--rw` (`randrw`), `--bs`, `--size`, `--numjobs`, `--runtime` with `--time_based`, `--filename`, `--iodepth`, `--direct` and `--group_reporting`.
```bash
kubectl exec -it <pod> -- fio --name=randrw --rw=randrw --bs=4k --size=1G \
  --numjobs=4 --runtime=60 --time_based --filename=/data/fio-test \
  --iodepth=16 --direct=1 --group_reporting
```
- `--direct=1` uses non-buffered I/O instead of the page cache.
- Compare small random I/O (`--bs=4k`) with large sequential writes (`--rw=write --bs=1m`) and match the test to the workload.
- Run the same fio against the node's device or a scratch volume of the same type and zone to separate disk speed from container-path overhead. Delete the test file afterwards.

## 3. Provider disk limits
Cloud disk types have their own IOPS and throughput limits, and some allow limited bursts. Read your provider's current volume-type documentation for the limits and for the per-volume metrics, which are not visible from inside Kubernetes. With the EBS CSI driver, `iops`, `iopsPerGB` and `throughput` StorageClass parameters can be set for io1, io2 and gp3 volumes (`throughput` is gp3 only, default 125 MiB/s); the driver defaults to gp3 when no type is given.

## 4. cgroup I/O limits
If the Pod's cgroup has I/O limits, the container can be throttled regardless of disk speed. On cgroup v2 look at the `io.max` file of the container's cgroup (and `io.weight`); on cgroup v1 look at `blkio.throttle.read_iops_device` and related files. A fio run inside the Pod far below the node-level run is the typical signature.

## 5. Noisy neighbours
- Shared local disks: use `iostat -x 1` on the node during the incident and look at `%util` and `await`.
- Network storage: contention is invisible to node-local tools; use the storage system's own metrics.

## 6. Order of investigation
1. Application wait metrics. 2. fio inside the Pod matched to the workload. 3. Same fio on the node. 4. Provider per-volume metrics. 5. cgroup limits. 6. `iostat -x` on the node.

## Gotchas
- `kubectl top` shows CPU and memory, not disk I/O.
- After a CSI driver or kubelet upgrade compare mount options (`findmnt`) before and after an unexplained regression.
- Several containers writing to one volume mask which one generates the I/O; benchmark per container.

## Verify
- [ ] The application cause was ruled out first.
- [ ] fio with `--direct=1` was run inside the Pod and on the node and compared.
- [ ] Provider volume limits and metrics were checked for the volume type in use.
- [ ] cgroup I/O limits were checked.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: fio options in the fio HOWTO, cgroup v1/v2 file names in kernel docs, EBS CSI performance parameters.

Method: documentation only; no commands were run.
