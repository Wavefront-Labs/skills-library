---
id: computing-software.cybersecurity-defensive.system-hardening.containerd-hardening
name: containerd-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [containerd-hardening, containerd, cri, kubernetes-node-hardening, runc, gvisor, container-runtime]
level: advanced
status: docs-checked
description: "Harden containerd on Kubernetes nodes: socket permissions, CRI plugin config, registry TLS and mirrors, default seccomp/AppArmor, sandboxed runtimes, and patching runc."
sources: ["https://github.com/containerd/containerd/blob/main/docs/cri/config.md", "https://github.com/containerd/containerd/blob/main/docs/hosts.md", "https://github.com/containerd/containerd/blob/main/docs/man/containerd-config.toml.5.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/tutorials/security/seccomp.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/tasks/configure-pod-container/user-namespaces.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# containerd hardening

containerd is a widely used Kubernetes container runtime. Access to its socket equals root
on the node and control of every container on it.

## Socket and files
- The containerd socket (`/run/containerd/containerd.sock` by default) should stay root-owned: the `[grpc]` `uid` and `gid` options default to 0. Never mount it into
  pods (same as the Docker socket). Kubernetes policies should block `hostPath` mounts of `/run/containerd`.
- Keep `/etc/containerd/config.toml` and `/var/lib/containerd` writable by root only.
- Do not expose the containerd API over TCP (the `grpc-tcp` listener is a separate, opt-in section).

## CRI plugin settings (config.toml, version 2 format shown)
```toml
version = 2
[plugins."io.containerd.grpc.v1.cri"]
  enable_unprivileged_ports = false     # default true
  enable_unprivileged_icmp = false      # default true
  restrict_oom_score_adj = false        # default false
  max_container_log_line_size = 16384   # default 16384; -1 means no limit
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
  [plugins."io.containerd.grpc.v1.cri".registry]
    config_path = "/etc/containerd/certs.d"
```
In config version 3 the same runtime keys live under `plugins.'io.containerd.cri.v1.runtime'` and the registry setting under `plugins.'io.containerd.cri.v1.images'.registry`.
Per-registry `hosts.toml` under `certs.d/<registry>/` with `ca` and `skip_verify = false` (never true), plus
mirrors for pull-through caches.

## Default security profiles
- Kubernetes defaults: enable kubelet `seccompDefault: true` (GA 1.27) so pods without a profile get
  `RuntimeDefault` seccomp from containerd.
- AppArmor (the CRI option `disable_apparmor` defaults to false) or SELinux (`enable_selinux`, default false, in the CRI config) enforced on nodes.
- Pod Security Admission "restricted" for workload namespaces.

## Sandboxed runtimes for untrusted workloads
Add gVisor (`runsc`) or Kata Containers as additional runtime handlers and select them via `RuntimeClass` for
multi-tenant or untrusted code:
```toml
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
  runtime_type = "io.containerd.runsc.v1"
```

## Patch the runtime stack
containerd and runc are the container isolation boundary. Track their security advisories and releases, patch nodes promptly, and prefer node image rollouts
(immutable nodes) over in-place upgrades.

## User namespaces
Kubernetes user namespaces (`hostUsers: false` in the pod spec; the `UserNamespacesSupport` feature gate is GA from Kubernetes 1.36) map container root to an unprivileged host UID, limiting
escape impact; see the Kubernetes user-namespaces task and containerd's user-namespaces documentation for runtime and kernel requirements.

## Verify
`stat -c '%a %U:%G' /run/containerd/containerd.sock` shows root ownership and a mode no wider than you intend; the active `config.toml` (compare with `containerd config default`, which prints the defaults for your containerd version) shows the expected runtime handlers and registry `config_path`; a pod without a seccomp profile on a node with `seccompDefault: true` runs
with `RuntimeDefault`; containerd and runc are on supported, patched releases.

## Checked
Checked 2026-10-25 against containerd's documentation (containerd/containerd: docs/cri/config.md, docs/hosts.md, docs/man/containerd-config.toml.5.md, main branch) and the Kubernetes seccomp tutorial and user-namespaces task (kubernetes/website, 2026-10-24). Confirmed: CRI keys `enable_unprivileged_ports`, `enable_unprivileged_icmp`, `restrict_oom_score_adj`, `max_container_log_line_size`, `enable_selinux`, `disable_apparmor`, `SystemdCgroup` under the runc options, registry `config_path`, `hosts.toml` with `ca` and `skip_verify`, `runtime_type = "io.containerd.runsc.v1"`, config versions 2 and 3 key paths, grpc `uid`/`gid` defaults, kubelet `seccompDefault` (GA 1.27). Removed unconfirmed: numeric socket and file modes, the `cri-containerd.apparmor.d` profile name, specific runc CVE identifiers, and the `crictl`/kube-bench verification steps; the CIS Kubernetes benchmark was not read.

Method: documentation only; no commands were run.
