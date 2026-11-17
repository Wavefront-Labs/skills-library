---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cis-kube-apiserver-flag-remediation
name: cis-kube-apiserver-flag-remediation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cis-benchmark, profiling-disabled, authorization-mode, kube-apiserver, kube-bench]
level: practitioner
status: docs-checked
description: "Remediate CIS benchmark kube-apiserver findings (profiling, authorization mode, anonymous auth, audit flags, admission plugins, TLS) on kubeadm clusters."
sources: ["https://www.cisecurity.org/benchmark/kubernetes", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/master.yaml", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/", "https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIS kube-apiserver flag remediation

Section 1.2 of the CIS Kubernetes Benchmark (ids below are kube-bench's `cis-1.9` master checks; other
benchmark versions renumber). On kubeadm, set flags in ClusterConfiguration (`apiServer.extraArgs`) so
upgrades keep them, then edit `/etc/kubernetes/manifests/kube-apiserver.yaml` for the running node.

| Check | Setting |
|---|---|
| 1.2.15 profiling | `--profiling=false` (also controller-manager 1.3.2 and scheduler 1.4.1) |
| 1.2.6-1.2.8 authorization | `--authorization-mode=Node,RBAC` (never `AlwaysAllow`) |
| 1.2.1 anonymous auth (Manual) | `--anonymous-auth=false`, or limit anonymous requests to health paths with an `AuthenticationConfiguration` `anonymous` block (see below) |
| 1.2.9-1.2.14 admission | `NodeRestriction` set (1.2.14); `ServiceAccount` and `NamespaceLifecycle` not disabled (1.2.12, 1.2.13); `AlwaysAdmit` not set (1.2.10); `EventRateLimit` (1.2.9) and `AlwaysPullImages` (1.2.11) are Manual |
| 1.2.16-1.2.19 audit | `--audit-log-path`, then `--audit-log-maxage=30`, `--audit-log-maxbackup=10`, `--audit-log-maxsize=100` ("or as appropriate"); the apiserver's own defaults are 366, 100 and 100 |
| 1.2.4-1.2.5 kubelet TLS | `--kubelet-client-certificate` and `--kubelet-client-key`; `--kubelet-certificate-authority=/etc/kubernetes/pki/ca.crt` |
| 1.2.21-1.2.22 SA tokens | `--service-account-lookup=true` (default true), `--service-account-key-file` set |
| 1.2.29 ciphers (Manual) | a strong `--tls-cipher-suites` list; `--tls-min-version` accepts `VersionTLS10` to `VersionTLS13` (hardening, not a numbered 1.9 check) |
| 1.2.27-1.2.28 encryption (Manual) | `--encryption-provider-config` set and providers configured |

```yaml
# kubeadm v1beta4: extraArgs is a list of name/value pairs
apiServer:
  extraArgs:
  - {name: profiling, value: "false"}
  - {name: authorization-mode, value: "Node,RBAC"}
  - {name: audit-log-maxage, value: "30"}
```

Anonymous access limited to health endpoints (a file passed with `--authentication-config`; you cannot
also set `--anonymous-auth`):
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AuthenticationConfiguration
anonymous:
  enabled: true
  conditions:
  - path: /livez
  - path: /readyz
  - path: /healthz
```

## Care points
- `--anonymous-auth=false` rejects health checks that call `/livez`, `/readyz` or `/healthz` without
  credentials (load balancer probes); check them first, or use the `conditions` form above.
- `--kubelet-certificate-authority` breaks `kubectl logs` and `kubectl exec` until kubelet serving
  certificates are issued by a CA the apiserver trusts (`serverTLSBootstrap: true` in the
  KubeletConfiguration plus CSR approval).
- Some checks are Manual or not applicable on managed clusters (use the EKS/GKE/AKS benchmark).

## Verify
```bash
kube-bench run --targets master --check 1.2.1,1.2.6,1.2.15 2>/dev/null | grep -E 'PASS|FAIL|WARN'
```

## Checked
2026-10-28. Confirmed: check ids, wording and the 30/10/100 audit values against kube-bench
`cfg/cis-1.9/master.yaml`; every flag, the 366/100/100 audit defaults, `--service-account-lookup`
default and `--tls-min-version` values against the kube-apiserver reference; the
`AuthenticationConfiguration` anonymous example and the "cannot also set the flag" rule against the
Authentication page; the list form of `extraArgs` against the kubeadm v1beta4 page; `--targets` and
`--check` against the kube-bench docs. Removed: the "1.32+" version gate (not stated on the pages read) and
the unsourced claim that kubelets probe the apiserver anonymously. The CIS PDF is not readable without
registration, so ids come from kube-bench.
Method: documentation only; no commands were run.
