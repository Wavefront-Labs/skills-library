---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubescape-scanning-and-cis-remediation
name: kubescape-scanning-and-cis-remediation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubescape, cis-remediation, cis-benchmark, nsa-cisa, posture-management, kube-bench, cks]
level: practitioner
status: docs-checked
description: "Scan clusters and manifests with Kubescape frameworks (CIS, NSA, MITRE) and remediate the common CIS findings in apiserver, kubelet, etcd and RBAC without breaking the cluster."
sources: ["https://github.com/kubescape/kubescape", "https://raw.githubusercontent.com/kubescape/kubescape/master/README.md", "https://www.cisecurity.org/benchmark/kubernetes", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/master.yaml", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/node.yaml", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/policies.yaml", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/", "https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubescape scanning and CIS remediation

## Kubescape
```bash
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash   # read the script first
kubescape list frameworks                                # find the CIS framework name for your Kubernetes version
kubescape scan framework nsa --format json --output results.json
kubescape scan framework mitre
kubescape scan control C-0057 -v                         # privileged container
kubescape scan control C-0013 -v                         # non-root containers
kubescape scan framework nsa ./manifests/ --compliance-threshold 80 --severity-threshold high   # CI on YAML/Helm files
kubescape scan image nginx:1.27                          # image vulnerabilities (uses Grype)
```
Exceptions: `kubescape scan --exceptions <file>`; objects matched by a `disable` exception are shown as passed
with exceptions, so document why each exists. For continuous scanning in the cluster use the
`kubescape-operator` Helm chart. For some controls Kubescape collects node-level data (a CRD-based host
sensor when node-agent CRDs exist; `--host-scan=false` disables it).

kube-bench is the node-level CIS checker (reads files and flags on each node); Kubescape covers cluster
objects and some node data. Use both for CIS.

## Common CIS findings and the safe fix (kube-bench `cis-1.9` ids)
| Finding | Remediation (kubeadm) |
|---|---|
| 1.2.15 apiserver `--profiling` not false | add `profiling: "false"` to apiServer.extraArgs (also controller manager 1.3.2, scheduler 1.4.1) |
| 1.2.16-1.2.19 audit log flags missing | audit policy plus `--audit-log-*` (see the audit skill) |
| 1.2.1 `--anonymous-auth` | `false` only if load-balancer health checks use credentials; otherwise keep anonymous limited to `/livez`, `/readyz`, `/healthz` with an `AuthenticationConfiguration` `anonymous` block |
| 1.2.9, 1.2.14 admission plugins (`EventRateLimit`, `NodeRestriction`) | `--enable-admission-plugins=NodeRestriction,...`; `EventRateLimit` needs an admission control configuration file |
| 1.2.27 encryption provider | EncryptionConfiguration (see the encryption skill) |
| 4.2.4 kubelet read-only port, 4.2.1 anonymous auth, 4.2.2 authorization mode | KubeletConfiguration `readOnlyPort: 0`, `authentication.anonymous.enabled: false`, `authorization.mode: Webhook` |
| `protectKernelDefaults` (no numbered check in 1.9) | set true only after tuning the sysctls on the host, or the kubelet errors on start |
| 1.1.x and 4.1.x file permissions | mode 600 and root:root ownership for kubeconfigs and configs (see the file-permission skill) |
| 5.1.x RBAC: cluster-admin use, wildcard roles, secrets access | review bindings (see the escalation skill) |
| 5.2.x pod security | Pod Security Standards labels |
| 5.3.x NetworkPolicy missing | default-deny per namespace |
Apply control-plane changes one node at a time; the kubelet applies static-pod manifest changes by scanning
the manifests directory.
Managed clusters: use the provider's CIS benchmark (EKS, GKE and AKS variants are listed on the CIS page);
control-plane items are largely the provider's to fix.

## Verify
- [ ] Kubescape compliance score tracked over time; CI blocks new high-severity failures.
- [ ] kube-bench re-run shows remediated items PASS; nothing broken (load-balancer health checks, metrics scraping).

## Checked
2026-10-28. Confirmed: install script URL, `scan framework nsa|mitre`, `--format`/`--output`, `scan control
C-0057` (privileged) and `C-0013` (non-root), `--compliance-threshold`, `--severity-threshold`, scanning a
manifests path, `scan image` with Grype, `--exceptions`, `kubescape list frameworks`, the operator chart and
`--host-scan=false` against the Kubescape README; check ids and wording against kube-bench `cfg/cis-1.9`
(`master`, `node`, `policies`); the anonymous `conditions` form against the Authentication page; the
kubelet field names against the kube-bench remediation text; static-pod directory scanning against the
Kubernetes static-pod page; the managed variants against the CIS page. Removed: the guessed CIS framework
id `cis-v1.10.0`, `--fail-threshold` and the `allcontrols` framework, comma-separated framework and
control lists, the `workloadconfigurationscans` CRD command, the "default RBAC limits anonymous to health
endpoints" and "kubeadm defaults" claims, and the old 4.2.x id for `protectKernelDefaults`. The
kubescape.io docs home page returns only a stub, so the README was used.
Method: documentation only; no commands were run.
