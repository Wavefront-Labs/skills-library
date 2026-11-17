---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-bootstrap
name: kubeadm-cluster-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, cluster-bootstrap, control-plane-init, kubeadm-init, kubeadm-join, bootstrap-token, discovery-token-ca-cert-hash, cri, containerd, pause-image, static-pods, cluster-config, bare-metal-kubernetes]
level: advanced
status: docs-checked
description: "Bootstrap a kubeadm cluster from scratch: pre-flight, kubeadm init with a ClusterConfiguration, CNI install, worker join, and token hygiene."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/", "https://kubernetes.io/docs/reference/networking/ports-and-protocols/", "https://kubernetes.io/docs/setup/production-environment/container-runtimes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm cluster bootstrap

**Goal:** bring up a working control plane and join nodes with `kubeadm`, reproducibly,
without the common first-cluster failures (CRI mismatch, CIDR collision, stale tokens).
HA control-plane topology is in
`computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-ha-stacked-vs-external-etcd`;
upgrading an existing cluster is in
`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-upgrade-sequencing`.

## 1. Pre-flight (do this before `kubeadm init`, not after it fails)
- Disable swap (`swapoff -a`, and remove it from `/etc/fstab`): by default the kubelet fails
  to start when it detects swap. To tolerate swap set `failSwapOn: false`; workloads still get
  no swap unless `swapBehavior` is changed from `NoSwap`.
- Enable IPv4 forwarding (`net.ipv4.ip_forward = 1`, persisted under `/etc/sysctl.d/`);
  kubeadm's preflight checks it. Some CNI plugins expect further sysctls or kernel modules:
  follow your CNI's documentation.
- Install a CRI runtime (dockershim was removed from the kubelet in 1.24; Docker Engine
  needs `cri-dockerd`). The docs recommend the `systemd` cgroup driver when systemd is the
  init system: set `SystemdCgroup = true` for containerd's runc in
  `/etc/containerd/config.toml` and `cgroupDriver: systemd` in the KubeletConfiguration (the
  kubelet's own default is `cgroupfs`). The kubelet and the runtime must use the same driver.
- Pre-pull images with `kubeadm config images pull` to catch registry/pull-secret issues
  before they show up as a hung `init`.
- Open required ports ahead of time. Control plane: 6443 (API server), 2379-2380 (etcd),
  10250 (kubelet), 10259 (kube-scheduler), 10257 (kube-controller-manager). Workers: 10250,
  10256 (kube-proxy) and the NodePort range 30000-32767. See the ports and protocols page.

## 2. `kubeadm init`
Use a config file, not flags, so the exact invocation is reviewable and repeatable:
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: stable          # or pin an exact release, for example v1.37.0
controlPlaneEndpoint: "k8s-api.internal:6443"   # LB/VIP even for a single control-plane node — required for later HA conversion
networking:
  podSubnet: 10.244.0.0/16      # must not overlap the node/service subnet or your CNI's default
  serviceSubnet: 10.96.0.0/12
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
nodeRegistration:
  criSocket: unix:///var/run/containerd/containerd.sock
```
```bash
kubeadm init --config kubeadm-config.yaml --upload-certs
```
- `--upload-certs` encrypts control-plane certs into a Secret so additional control-plane
  nodes can join without manually copying `/etc/kubernetes/pki`; the cert key it prints
  expires after 2 hours — re-run `kubeadm init phase upload-certs --upload-certs` if you
  miss the window.
- kubeadm does not support turning a single control-plane cluster created without
  `--control-plane-endpoint` into an HA cluster, so set `controlPlaneEndpoint` even for a
  one-node cluster (a DNS name that can later point at a load balancer).
- `kubeadm init` writes `/etc/kubernetes/admin.conf` (subject `O = kubeadm:cluster-admins,
  CN = kubernetes-admin`, bound to `cluster-admin`); copy it to `~/.kube/config` for the
  bootstrapping user only. It also writes `super-admin.conf` (`system:masters`, bypasses
  RBAC): keep it somewhere safe and share neither file. Generate scoped kubeconfigs for
  other users with `kubeadm kubeconfig user --client-name <name>`.

## 3. CNI install (CoreDNS does not start until this happens)
kubeadm is CNI agnostic. CoreDNS does not start until a Pod network add-on is installed, so
Pods in `kube-system` waiting on it right after `init` are expected, not a failure:
```bash
kubectl apply -f <your-cni-manifest-or-install-method>
# podSubnet above must match the CIDR your CNI is configured for
```
See `computing-software.cloud-infrastructure-engineering.kubernetes.cni-plugin-architecture-calico-cilium-flannel`
for choosing between them.

## 4. Joining nodes
```bash
kubeadm token create --print-join-command   # run on a control-plane node; the token from init has a 24h TTL
kubeadm join k8s-api.internal:6443 --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>
```
- For an additional control-plane node, append `--control-plane --certificate-key <key>`
  from the `--upload-certs` step.
- Tokens are single-purpose bootstrap credentials, not long-lived secrets — rotate them
  (`kubeadm token create`) rather than reusing one past its TTL; list/delete stale ones
  with `kubeadm token list` / `kubeadm token delete <token>`.
- `--discovery-token-ca-cert-hash` pins the API server's CA so a compromised network
  can't MITM the join; recompute it with
  `openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der | openssl dgst -sha256 -hex`
  if the token's original output is lost.

## Gotchas
- Choose a `podSubnet` that does not overlap the host or Service networks.
- Run `kubeadm reset` before re-joining a node. It does not clean `/etc/cni/net.d`, iptables
  or IPVS rules, or `$HOME/.kube`; leftover CNI configuration can conflict with a different
  CNI on the next join (see the kubeadm-reset-and-node-rejoin skill).

## Verify
- [ ] `kubectl get nodes` shows all nodes `Ready` after CNI install.
- [ ] `kubectl get pods -n kube-system` shows no CrashLoopBackOff on CoreDNS or the CNI
      daemonset.
- [ ] `kubeadm token list` has no indefinitely-lived or forgotten tokens.
- [ ] `controlPlaneEndpoint` resolves and is what every node's kubeconfig points at, not
      a single control-plane node's bare IP.
- [ ] `kubeadm init phase upload-certs` leftover Secret (`kubeadm-certs` in `kube-system`)
      has been allowed to expire or been deleted once all control-plane nodes have joined.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed: the v1beta4 kubeadm config examples, the 2 hour lifetime of the uploaded certificate key and `kubeadm-certs` Secret, the 24 hour TTL of the initial token, the CA hash `openssl` command, the control plane and worker port tables, swap and `failSwapOn` behaviour, containerd `SystemdCgroup` and the kubelet default of `cgroupfs`, the `admin.conf` and `super-admin.conf` subjects, and that an HA conversion without `--control-plane-endpoint` is unsupported. Removed as unconfirmed: the `br_netfilter` sysctl requirement, the clock-skew figure and the Cilium manifest URL.

Method: documentation only; no commands were run.
