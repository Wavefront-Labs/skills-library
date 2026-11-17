---
id: computing-software.cloud-infrastructure-engineering.kubernetes.privileged-node-agent-daemonsets
name: privileged-node-agent-daemonsets
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonset, privileged-daemonset, hostpid, hostnetwork, capabilities, node-agents, pod-security]
level: advanced
status: docs-checked
description: "Run node agents needing host access (hostPID, hostNetwork, hostPath) with least privilege: capabilities over privileged, read-only mounts, isolated namespace."
sources: ["https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://kubernetes.io/docs/concepts/storage/volumes/", "https://kubernetes.io/docs/tasks/manage-daemon/update-daemon-set/", "https://man7.org/linux/man-pages/man7/capabilities.7.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privileged node agents done safely

Monitoring, logging, CNI, CSI and security agents legitimately need host access. A
`privileged: true` + hostPath `/` pod is root on the node — treat these DaemonSets as part of
the node's trusted computing base.

## Ask for exactly what is needed
| Need | Grant | Not |
|---|---|---|
| read host process list (node-exporter) | `hostPID: true` | privileged |
| host network stats / bind host ports | `hostNetwork: true` | privileged |
| read logs | hostPath `/var/log` **readOnly** | `/` |
| eBPF agents | `CAP_BPF`, `CAP_PERFMON` (both added in Linux 5.8 to split them out of `CAP_SYS_ADMIN`) | `SYS_ADMIN` where avoidable |
| iptables-based redirection (for example a mesh init container) | `NET_ADMIN`, `NET_RAW` | privileged |
| mount propagation (CSI node) | `privileged: true` + `mountPropagation: Bidirectional` — Kubernetes allows `Bidirectional` only in privileged containers | — |

```yaml
spec:
  hostPID: true
  containers:
  - name: node-exporter
    securityContext:
      runAsNonRoot: true
      runAsUser: 65534
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
      capabilities: {drop: [ALL]}
    volumeMounts:
    - {name: proc, mountPath: /host/proc, readOnly: true}
    - {name: sys, mountPath: /host/sys, readOnly: true}
  volumes:
  - {name: proc, hostPath: {path: /proc}}
  - {name: sys, hostPath: {path: /sys}}
```

## Containment
- Dedicated namespace per agent with PSA `enforce=privileged` (or `baseline` where it fits)
  and **no** human `edit` access — anyone who can create pods there can root nodes.
- Its own ServiceAccount with minimal RBAC; `automountServiceAccountToken: false` if it doesn't
  call the API.
- Admission policy exceptions scoped to that namespace + image digest, not blanket.
- Image from a trusted, signed source; pin digests; these images get root on every node.

## Gotchas
- `hostNetwork: true` pods share the node's ports — two versions during a rolling update clash
  on the port; use `maxSurge: 0` (default for DaemonSets).
- `hostPath` type `DirectoryOrCreate` silently creates paths on the host; use `Directory` to
  fail if missing.
- Writing to hostPath as root leaves root-owned files the next agent version may not read.

## Verify
- [ ] `kubectl get pods -n <agent-ns> -o jsonpath='{..securityContext}'` shows dropped caps / no privileged unless required.
- [ ] Kubescape/kube-bench exceptions list each privileged agent explicitly.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026
- Confirmed in the Kubernetes volumes page that `Bidirectional` mount propagation is allowed only in privileged containers, that hostPath `DirectoryOrCreate` creates a missing directory (permissions 0755) while `Directory` requires it to exist, and in the DaemonSet update page that `maxSurge` defaults to 0.
- Confirmed in Pod Security Standards that `hostNetwork`, `hostPID`, `hostIPC` and privileged containers are barred below `privileged`, and that `restricted` requires dropping ALL capabilities.
- Confirmed in the capabilities man page that `CAP_BPF` and `CAP_PERFMON` were added in Linux 5.8 to separate functionality from `CAP_SYS_ADMIN`. Removed unconfirmed tool attributions (Falco, Tetragon), the `SYS_PTRACE` and `CAP_SYS_RESOURCE` rows and the docker log path.

Method: documentation only; no commands were run.
