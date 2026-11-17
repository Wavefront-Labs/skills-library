---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-sysctls-safe-and-unsafe
name: pod-sysctls-safe-and-unsafe
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, securitycontext, sysctls, unsafe-sysctls, pod-security-standards, kubelet-config]
level: practitioner
status: docs-checked
description: "Set namespaced kernel parameters per pod via securityContext.sysctls, the safe set, enabling unsafe ones with allowedUnsafeSysctls, and PSS interaction."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/sysctl-cluster/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod sysctls

```yaml
spec:
  securityContext:
    sysctls:
    - name: net.ipv4.ip_local_port_range
      value: "1024 65000"
    - name: net.ipv4.tcp_keepalive_time
      value: "300"
```
Only **namespaced** sysctls can be set per pod, and the pod `securityContext` applies to all
containers in the pod. Namespaced ones listed in the docs: `kernel.shm*`, `kernel.msg*`,
`kernel.sem`, `fs.mqueue.*`, and the `net.*` sysctls that can be set in the container network
namespace (with exceptions, such as `net.netfilter.nf_conntrack_max` which is not namespaced
before Linux 5.12.2). Sysctls with no namespace are node-level: configure them on each node's OS
or with a privileged DaemonSet. Names may use `.` or `/` as separator (the kubelet since 1.23,
pod securityContext since 1.25).

## Safe set (enabled by default)
`kernel.shm_rmid_forced`, `net.ipv4.ip_local_port_range`, `net.ipv4.tcp_syncookies`,
`net.ipv4.ping_group_range` (1.18), `net.ipv4.ip_unprivileged_port_start` (1.22),
`net.ipv4.ip_local_reserved_ports` (1.27), `net.ipv4.tcp_keepalive_time`,
`net.ipv4.tcp_fin_timeout`, `net.ipv4.tcp_keepalive_intvl`, `net.ipv4.tcp_keepalive_probes`
(all 1.29), `net.ipv4.tcp_rmem` and `net.ipv4.tcp_wmem` (1.32),
`net.ipv4.tcp_slow_start_after_idle` and `net.ipv4.tcp_notsent_lowat` (1.37). Several need a
minimum kernel version (see the docs page). A safe sysctl must not affect other pods, harm the
node, or gain CPU or memory beyond the pod's limits. Exceptions: `net.*` sysctls are not
allowed with host networking, and `net.ipv4.tcp_syncookies` is not namespaced on kernel 4.5
or lower.

## Unsafe sysctls
Any other namespaced sysctl (for example `net.core.somaxconn`, `kernel.msgmax`) is disabled by
default and must be allowed per node, only namespaced ones can be enabled:
```yaml
# KubeletConfiguration
allowedUnsafeSysctls: ["net.core.somaxconn", "kernel.msg*"]
```
(the equivalent flag is `--allowed-unsafe-sysctls`). A pod asking for a disabled unsafe sysctl
is scheduled but fails to launch. The docs suggest treating such nodes as tainted and using
taints and tolerations so only pods that need them land there.

## Defaults for all pods
`defaultPodSysctls` in the KubeletConfiguration (feature gate `DefaultPodSysctls`) sets sysctls
for every pod on the node, including static pods, for both safe and unsafe namespaced sysctls,
without needing `allowedUnsafeSysctls`. Check the docs page for the gate's stage in your release.

## Pod Security
The Pod Security Standards allow only the "safe" subset of sysctls (namespaced and isolated from
other pods) in the baseline profile; restricted builds on baseline. Unsafe sysctls need a
namespace using the privileged level or a policy exemption.

## Verify
```bash
kubectl exec <pod> -- sysctl net.ipv4.ip_local_port_range
kubectl describe pod <pod>      # a pod with a disallowed sysctl fails to start; read its events
```

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Using sysctls in a Kubernetes Cluster"
(current docs, which lists the 1.37 additions; latest release v1.37.1), "Pod Security Standards",
and the kubelet config v1beta1 type (`allowedUnsafeSysctls`). Confirmed: safe set with versions,
exceptions, unsafe enabling, namespaced list, `defaultPodSysctls`, PSS rule. Removed the
unconfirmed `SysctlForbidden` reason, "stay failed" wording and event query.
Method: documentation only; no commands were run.
