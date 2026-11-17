---
id: computing-software.cybersecurity-defensive.cloud-security.tetragon-runtime-enforcement
name: tetragon-runtime-enforcement
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [tetragon, ebpf, runtime-security, tracing-policy, kubernetes-runtime, process-enforcement, cloud-workload-protection]
level: advanced
status: draft
description: "Use Cilium Tetragon for eBPF runtime security: TracingPolicies for process, file and network events, in-kernel enforcement, Kubernetes-aware filtering and export."
sources: ["https://tetragon.io/docs/", "https://tetragon.io/docs/concepts/tracing-policy/", "https://github.com/cilium/tetragon"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tetragon

Kubernetes-aware eBPF observability and **enforcement**: filters and acts in kernel (low overhead,
no TOCTOU gap from user-space decisions).

## Install
`helm install tetragon cilium/tetragon -n kube-system`; events via `kubectl logs -n kube-system ds/tetragon -c export-stdout` or the `tetra` CLI (`tetra getevents -o compact`). Default: process exec/exit events with pod metadata.

## TracingPolicy example (detect and kill writes to sensitive files)
```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata: {name: protect-etc-shadow}
spec:
  kprobes:
  - call: "security_file_permission"
    syscall: false
    args: [{index: 0, type: "file"}, {index: 1, type: "int"}]
    selectors:
    - matchArgs:
      - {index: 0, operator: "Equal", values: ["/etc/shadow", "/etc/sudoers"]}
      - {index: 1, operator: "Equal", values: ["2"]}     # MAY_WRITE
      matchActions:
      - action: Sigkill
```
Use `TracingPolicyNamespaced` and `podSelector` to scope to workloads.

## Useful policies
- Process exec of shells/package managers in production containers (detect, later kill).
- Outbound connections from pods that should not egress (`tcp_connect` kprobe, match by destination).
- Privilege escalation (`commit_creds`), kernel module loading, `ptrace`.
- Binary execution from writable paths (`/tmp`, `/dev/shm`).

## Export
JSON events to stdout/file -> Fluent Bit/Vector -> SIEM; Prometheus metrics for policy hits.

## Gotchas
- Enforcement actions (Sigkill, Override return value) can break workloads - run detect-only first and scope with selectors.
- Kernel version and BTF requirements; hook names are kernel-internal and may vary across versions.
- Policies are cluster objects: protect them with RBAC (an attacker with cluster-admin can delete them).

## Verify
- [ ] Test pod writing to /etc/shadow is killed and the event appears in the SIEM.
- [ ] No enforcement hits on production workloads during the detect-only phase.
