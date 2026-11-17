---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-faq-kernel-requirements
name: tetragon-faq-kernel-requirements
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [faq-kernel, tetragon, kernel-version, kernel-config, tetra-probe]
level: practitioner
status: docs-checked
description: "Check a host meets Tetragon's minimum kernel version and required kernel config options using tetra probe config and tetra probe."
sources:
  - "https://tetragon.io/docs/installation/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon kernel version and config requirements

Goal: confirm a node can run Tetragon before deploying.

## Minimum kernel
Linux 4.19 or greater. Tests run on LTS kernels 4.19, 5.4, 5.10, 5.15 and bpf-next; not all features work on older kernels, so use the most recent stable kernel possible. On arm64 kernels 4.19 and 5.4, features like reading exec arguments might not work because of a kernel bug; use 5.10 or later on arm64. BTF support is also needed (see the missing BTF FAQ).

## Check config
```shell
tetra probe config
```
Lists detected kernel features (for example `CONFIG_BPF:y`, `CONFIG_DEBUG_INFO_BTF:y`); missing features suggest the kernel is misconfigured.

## Probe runtime features
Needs root to load probe BPF programs:
```shell
sudo tetra probe
```
On a cluster node, run from the image:
```shell
kubectl run bpf-probe --image=quay.io/cilium/tetragon-ci:latest --privileged --restart=Never -it --rm --command -- tetra probe
```
Output is boolean per feature, such as `override_return`, `kprobe_multi`, `lsm`, `fmodret`, `signal`, `link_pin`, `batch_update`.

## Required options (may evolve with features)
- Core BPF: `CONFIG_BPF`, `CONFIG_BPF_JIT`, `CONFIG_BPF_JIT_DEFAULT_ON`, `CONFIG_BPF_EVENTS`, `CONFIG_BPF_SYSCALL`, `CONFIG_HAVE_BPF_JIT`, `CONFIG_HAVE_EBPF_JIT`, `CONFIG_FTRACE_SYSCALLS`
- BTF: `CONFIG_DEBUG_INFO_BTF`, `CONFIG_DEBUG_INFO_BTF_MODULES`
- Enforcement: `CONFIG_BPF_KPROBE_OVERRIDE`
- Cgroup and process tracking: `CONFIG_CGROUPS`, `CONFIG_MEMCG`, `CONFIG_BLK_CGROUP`, `CONFIG_CGROUP_SCHED`, `CONFIG_CGROUP_PIDS`, `CONFIG_CGROUP_FREEZER`, `CONFIG_CPUSETS`, `CONFIG_PROC_PID_CPUSET`, `CONFIG_CGROUP_DEVICE`, `CONFIG_CGROUP_CPUACCT`, `CONFIG_CGROUP_PERF`, `CONFIG_CGROUP_BPF`
- Optional on kernels >= 6.0: `CGROUP_FAVOR_DYNMODS=y`, which can ease pod and container association issues on platforms with frequent cgroup migrations
- Cgroupv1 on kernels >= 6.11: `CONFIG_MEMCG_V1=y`, `CONFIG_CPUSETS_V1=y`

## Checked

Date: 2026-11-07

Cited page read in full; every claim matched to page text.

Method: documentation only; no commands were run.
