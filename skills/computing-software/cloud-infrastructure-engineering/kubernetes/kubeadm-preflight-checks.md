---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-preflight-checks
name: kubeadm-preflight-checks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-preflight, ignore-preflight-errors, cluster-bootstrap]
level: practitioner
status: docs-checked
description: "Run and interpret kubeadm preflight checks, fix the usual failures (swap, ports, CRI, sysctls) and use --ignore-preflight-errors only deliberately."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/preflight/checks.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm preflight checks

## Run them on their own first
```bash
sudo kubeadm init phase preflight --config kubeadm.yaml      # control plane
sudo kubeadm join phase preflight <endpoint>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```
Running the phase alone lets you fix every problem before anything is written to
`/etc/kubernetes`. Errors abort; warnings (`[WARNING ...]`) do not.

## Common failures and fixes
| Check | Message | Fix |
|---|---|---|
| Swap | `[ERROR Swap]` (current source: "swap is supported for cgroup v2 only. The kubelet must be properly configured to use swap ... or disable swap on the node") | `swapoff -a` and remove the fstab line, or tolerate swap deliberately with `failSwapOn: false` and `swapBehavior` |
| Ports | `[ERROR Port-6443]` / `Port-10250` / `Port-10259` / `Port-10257` / `Port-2379` | something already listening: an old kubelet, a previous etcd; then `kubeadm reset` |
| Existing manifests | `[ERROR FileAvailable--etc-kubernetes-manifests-kube-apiserver.yaml]` (one check per control-plane static pod manifest) | leftover from a previous init; `kubeadm reset -f` |
| CRI | `[ERROR CRI]` (kubeadm cannot connect to the runtime endpoint, or it is not running) | start the runtime; check the CRI socket path (containerd default `unix:///var/run/containerd/containerd.sock`) |
| IP forward | `[ERROR FileContent--proc-sys-net-ipv4-ip_forward]` | set `net.ipv4.ip_forward = 1` and persist it under `/etc/sysctl.d/` |
| Resources | `[ERROR NumCPU]` / `[ERROR Mem]` | the control plane needs at least 2 CPUs and 1700 MB of memory (kubeadm constants) |
| Images | `[ERROR ImagePull]` | registry unreachable; pre-pull with `kubeadm config images pull` or set `imageRepository` |

## Ignoring checks
```bash
kubeadm init --ignore-preflight-errors=NumCPU,Mem      # names are the bracketed check IDs
kubeadm init --ignore-preflight-errors=all             # skips every check: avoid outside labs
```
The same list can live in `InitConfiguration.nodeRegistration.ignorePreflightErrors` so it is
reviewed in Git instead of typed ad hoc. Ignore only checks you understand: ignoring `Swap`
or `CRI` produces a node that registers and then fails in confusing ways.

## Gotchas
- `SystemVerification` checks the kernel version and required cgroup subsystems; read its
  output rather than ignoring it.
- `Hostname` warns when the host name cannot be reached through a network lookup; fix
  `/etc/hosts` or DNS now. Dual-stack clusters also check IPv6 forwarding.
- A preflight pass does not validate the pod CIDR against your network; check for overlap
  with node and VPN ranges yourself.

## Verify
Re-run the preflight phase until it prints only expected warnings, then run the full
`kubeadm init --config kubeadm.yaml`.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed from `cmd/kubeadm/app/preflight/checks.go` and `constants.go`: check names `Swap`, `CRI`, `NumCPU`, `Mem`, `Hostname`, `SystemVerification`, `ImagePull`, `FileContent--proc-sys-net-ipv4-ip_forward`, `Port-<n>`, the 2 CPU and 1700 MB control-plane minimums, and that `--ignore-preflight-errors` and `ignorePreflightErrors` exist. Wrong or stale and fixed: the Swap message text (current source says swap is supported for cgroup v2 only), the manifests-directory check (now per-file `FileAvailable` checks), and the `bridge-nf-call-iptables` row (no such check in current Linux checks).

Method: documentation only; no commands were run.
