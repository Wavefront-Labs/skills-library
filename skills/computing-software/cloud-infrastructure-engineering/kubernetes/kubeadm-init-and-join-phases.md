---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-init-and-join-phases
name: kubeadm-init-and-join-phases
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-phases, skip-phases, init-phases, kubeadm-init-phase, kubeadm-join-phase, preflight, upload-certs, addon-phase]
level: advanced
status: docs-checked
description: "Run kubeadm init/join one phase at a time: skip phases you own (addons, kube-proxy), re-run a single phase to repair, and inject custom steps between phases."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/#join-phases", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#init-phases", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/cmd/init.go", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/cmd/join.go", "https://github.com/cilium/cilium/blob/main/Documentation/network/kubernetes/kubeproxy-free.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm init and join phases

**Goal:** stop treating `kubeadm init` as a black box. It is an ordered list of phases, each
runnable alone, so you can skip the ones another tool owns and re-run one to repair a node.

## 1. See the list
```bash
kubeadm init --help | sed -n '/preflight/,/show-join-command/p'
```
Order in the kubeadm source (`cmd/kubeadm/app/cmd/init.go`): `preflight` → `certs` (sub-phases
`ca`, `apiserver`, `apiserver-kubelet-client`, `front-proxy-ca`, `front-proxy-client`, `etcd-ca`,
`etcd-server`, `etcd-peer`, `etcd-healthcheck-client`, `apiserver-etcd-client`, `sa`) →
`kubeconfig` (`admin`, `super-admin`, `kubelet`, `controller-manager`, `scheduler`) → `etcd`
(`local`) → `control-plane` (`apiserver`, `controller-manager`, `scheduler`) → `kubelet-start` →
`wait-control-plane` → `upload-config` → `upload-certs` → `mark-control-plane` →
`bootstrap-token` → `kubelet-finalize` → `addon` (`coredns`, `kube-proxy`) →
`show-join-command`. Always confirm with `kubeadm init --help` for your version.

`kubeadm join` phases (same source): `preflight` → `control-plane-prepare` → `check-etcd` →
`kubelet-start` → `etcd-join` → `kubelet-wait-bootstrap` → `control-plane-join` →
`wait-control-plane`.

## 2. Skipping phases you own
```bash
kubeadm init --config kubeadm.yaml --skip-phases=addon/kube-proxy        # Cilium with kubeProxyReplacement
kubeadm init --config kubeadm.yaml --skip-phases=addon/coredns            # you install CoreDNS via Helm/GitOps
kubeadm init --skip-phases=preflight                                      # CI image lacks the kernel modules
```
Or in `InitConfiguration`:
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
skipPhases: ["addon/kube-proxy"]
```
Cilium's kube-proxy-free documentation uses `kubeadm init --skip-phases=addon/kube-proxy` for
its kube-proxy replacement mode.

## 3. Re-running one phase to repair
```bash
kubeadm init phase certs apiserver --config kubeadm.yaml      # regenerate just the apiserver cert (new SAN)
kubeadm init phase kubeconfig admin --config kubeadm.yaml     # rebuild admin.conf
kubeadm init phase control-plane apiserver --config kubeadm.yaml  # rewrite the static pod manifest
kubeadm init phase addon coredns --config kubeadm.yaml        # reinstall CoreDNS after someone deleted it
kubeadm init phase upload-certs --upload-certs                # fresh certificate-key for a control-plane join
```
Pass the same `--config` you used for `init`, otherwise the phase runs with defaults. Keep the
kubeadm config in version control; kubeadm also stores it in the `kubeadm-config` ConfigMap in
`kube-system`.

## 4. Inserting a custom step
Run everything up to a phase, do your thing, then continue:
```bash
kubeadm init --config kubeadm.yaml --skip-phases=addon,show-join-command
# ... apply your own CNI/CoreDNS/kube-proxy ...
kubeadm init phase addon coredns --config kubeadm.yaml
```
There is no "stop after phase X" flag, so `--skip-phases` of everything after X is the idiom.

## Gotchas
- Phase names are hierarchical; `--skip-phases=certs` skips all cert sub-phases.
- `kubeadm join phase` needs the full join flags (`--discovery-token-ca-cert-hash` etc.) or a
  `JoinConfiguration`; it does not remember them between invocations.
- After a phase rewrites a static pod manifest the kubelet picks it up on its next scan of
  `staticPodPath` (`fileCheckFrequency`, default 20s).
- `kubeadm upgrade` regenerates control-plane manifests from the configuration kubeadm stores in
  the cluster, so a manual phase re-run with different arguments can be overwritten later.

## Verify
- [ ] After a skipped `addon/kube-proxy`, `kubectl -n kube-system get ds kube-proxy` returns NotFound.
- [ ] After re-running `certs apiserver`, `openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text` lists the SANs you intended.
- [ ] `kubectl get --raw /healthz` returns `ok` after any control-plane phase rerun.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed from the kubeadm source: the ordered `init` phase list (including `wait-control-plane`, which an earlier version of this skill omitted) and the `join` phase list (which earlier omitted `check-etcd`, `etcd-join` and `kubelet-wait-bootstrap`); from the docs: the `certs`, `kubeconfig` and `addon` sub-phase names, `--skip-phases` and the `skipPhases` field, the `kubeadm-config` ConfigMap, the 20s default `fileCheckFrequency`; from Cilium's docs: `--skip-phases=addon/kube-proxy`. Removed as unconfirmed: the claim that phases do not restart the kubelet, and the `grep` and `sed` pipelines.

Method: documentation only; no commands were run.
