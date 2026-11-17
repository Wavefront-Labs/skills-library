---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cgroup-driver-and-cgroup-v2
name: cgroup-driver-and-cgroup-v2
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cgroup-driver, systemd-cgroup, cgroup-v2, containerd, kubelet, node-setup]
level: practitioner
status: docs-checked
description: "Align kubelet and containerd on the systemd cgroup driver, verify cgroup v2, and fix the instability and 'misconfiguration: kubelet cgroup driver' errors from mismatches."
sources: ["https://kubernetes.io/docs/setup/production-environment/container-runtimes/", "https://kubernetes.io/docs/concepts/architecture/cgroups/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cgroup driver and cgroup v2

## Rule
On systemd hosts, kubelet **and** container runtime must both use the `systemd` cgroup
driver. Two managers (systemd + cgroupfs) of one hierarchy cause resource accounting drift and
instability under pressure. The kubelet's own default driver is `cgroupfs`; kubeadm sets `systemd` when
`cgroupDriver` is not set (since 1.22). Check your container runtime's default and set it explicitly
(`containerd config default` produces a starting config; CRI-O uses systemd by default).

## Check
```bash
stat -fc %T /sys/fs/cgroup/            # cgroup2fs = v2, tmpfs = v1
grep cgroupDriver /var/lib/kubelet/config.yaml
grep SystemdCgroup /etc/containerd/config.toml
```

## Fix containerd
Start from `containerd config default > /etc/containerd/config.toml` if you have no config, then set `SystemdCgroup = true`:
```toml
# containerd 1.x
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
# containerd 2.x
[plugins.'io.containerd.cri.v1.runtime'.containerd.runtimes.runc]
  [plugins.'io.containerd.cri.v1.runtime'.containerd.runtimes.runc.options]
    SystemdCgroup = true
```
then `systemctl restart containerd`. CRI-O uses the systemd cgroup driver by default (`cgroup_manager = "cgroupfs"` changes it).

Kubelet: `cgroupDriver: systemd` in KubeletConfiguration. With feature gate `KubeletCgroupDriverFromCRI` (beta from 1.31, stable
from 1.34) and a runtime that supports the `RuntimeConfig` CRI RPC, the kubelet detects the driver from the runtime and
ignores its own `cgroupDriver`. containerd 1.x lacks that RPC, so the kubelet falls back to its own setting; the docs say
the fallback is dropped in 1.38 and old containerd will then fail with newer kubelets.

## cgroup v2
- Some features use only cgroup v2: MemoryQoS (beta from 1.37) and Pressure Stall Information. cgroup v1 is deprecated since
  1.35 and the kubelet does not start on a v1 node by default; set `failCgroupV1: false` in the kubelet config to override.
- Requirements: a distribution that enables v2, Linux kernel 5.8 or later, a runtime with v2 support (containerd 1.4+, CRI-O 1.20+),
  and the systemd cgroup driver in both kubelet and runtime. On GRUB systems you can add `systemd.unified_cgroup_hierarchy=1`.
- Check agents and runtimes first: cAdvisor stand-alone 0.43.0+, OpenJDK jdk8u372, 11.0.16 or 15+, uber-go/automaxprocs 1.5.1+,
  and Node.js 20.3.0+ (v18 does not reliably read v2 memory limits; set the heap size explicitly otherwise).

## Switching an existing node
Changing the cgroup driver of a node that has joined the cluster is sensitive: pods created under one driver can fail to
recreate their sandbox under another, and restarting the kubelet may not fix it. The docs recommend replacing the node (or
reinstalling it by automation) with the updated configuration.

## Symptoms of mismatch
Two cgroup managers give two views of available and in-use resources; the docs say nodes can become unstable under resource
pressure. Look for sandbox creation errors that mention cgroups in the kubelet and runtime logs.

## Verify
- [ ] Kubelet and runtime both report the systemd driver.
- [ ] `stat -fc %T /sys/fs/cgroup` = `cgroup2fs` on every node.

## Checked

2026-10-26: kubernetes.io container-runtimes, about-cgroup-v2 and kubeadm upgrade pages (v1.37 docs, kubernetes/website main 2026-10-25), the kubelet config API source and the KubeletCgroupDriverFromCRI feature-gate page. Confirmed: kubelet default driver cgroupfs and kubeadm systemd default since 1.22, containerd 1.x and 2.x SystemdCgroup sections, CRI-O defaults, KubeletCgroupDriverFromCRI stages and fallback removal in 1.38, stat command output, cgroup v2 requirements and app versions, v1 deprecation in 1.35 with failCgroupV1, node-replacement advice. Removed unconfirmed systemd and runc version floors, the Go version claim, v1 maintenance-mode date, specific error strings and the cpu/memory manager state removal.

Method: documentation only; no commands were run.
