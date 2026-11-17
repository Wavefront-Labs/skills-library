---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cni-installation-and-migration
name: cni-installation-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cni, cni-installation, cni-config-dir, cni-migration, cilium, calico, flannel, pod-cidr]
level: advanced
status: docs-checked
description: "Install a CNI with pod CIDRs aligned to kubeadm and the IPAM mode, recognise what /etc/cni/net.d and /opt/cni/bin do, and migrate live clusters between CNIs node by node."
sources: ["https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/", "https://docs.cilium.io/en/stable/installation/k8s-install-kubeadm/", "https://docs.cilium.io/en/stable/installation/k8s-install-migration/", "https://docs.cilium.io/en/stable/network/concepts/ipam/kubernetes/", "https://github.com/projectcalico/calico/blob/master/manifests/custom-resources.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CNI installation and migration

## Installing (new cluster)
1. Pick pod CIDR not overlapping node/VPC/VPN ranges; pass it to kubeadm:
   `kubeadm init --pod-network-cidr=10.244.0.0/16` (sets controller-manager `--cluster-cidr`
   and per-node `spec.podCIDR` allocation).
2. Install the CNI with **the same CIDR** and an IPAM mode that matches:
```bash
# Cilium (the kubeadm guide runs a plain kubeadm init; ipam.mode=kubernetes makes the agent use the node PodCIDRs)
cilium install --version <cilium-version> --set ipam.mode=kubernetes
cilium status --wait
# Calico via operator
kubectl create -f <tigera-operator.yaml of your Calico version, from the Calico install guide>
kubectl create -f custom-resources.yaml     # Installation.spec.calicoNetwork.ipPools[0].cidr: 10.244.0.0/16
# Flannel (expects 10.244.0.0/16 unless net-conf.json edited)
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```
3. Nodes become `Ready` only after the CNI writes its config to **`/etc/cni/net.d/`**
   (containerd loads only `max_conf_num` files from `conf_dir`, default 1) and binaries exist in
   **`/opt/cni/bin/`** (the documented defaults for the kubelet's `cni-conf-dir` and `cni-bin-dir`).
   Before that: `NetworkPluginNotReady ... cni plugin not initialized`, CoreDNS Pending.

Because containerd loads only a limited number of CNI config files, leftover configs from a
previous CNI in `/etc/cni/net.d` can leave pods wired by the wrong plugin; clean the directory
when changing CNIs.

## Migrating a live cluster (e.g. Flannel -> Cilium)
Approach from Cilium's migration guide (per-node, dual overlay). Requirements: a new, distinct
cluster CIDR for Cilium, Cilium's cluster-pool IPAM mode, a distinct overlay (protocol or port),
and an existing plugin that uses the Linux routing stack (such as Flannel, Calico or AWS-CNI).
The guide says it was not tested with BGP-based routing, changing IP families, chained mode or an
existing NetworkPolicy provider, and Cilium policy enforcement is disabled during the migration.
1. Install Cilium in "secondary" mode: different pod CIDR (e.g. 10.245.0.0/16), different tunnel
   port, `cni.customConf=true` so it **doesn't** take over `/etc/cni/net.d` yet; both overlays
   route to each other.
2. Create a `CiliumNodeConfig` that switches selected nodes to write Cilium's CNI config.
3. Per node: cordon, drain, label `io.cilium.migration/cilium-default=true`, restart cilium agent,
   reboot or restart pods -> new pods get Cilium IPs, can still reach Flannel pods.
4. After all nodes: update the Cilium configuration (Cilium primary, policy enforced), delete the
   per-node config, then delete the previous plugin; leftover iptables rules and interfaces are
   cleaned up when each node next reboots (optionally do a rolling reboot).
Other existing plugins that use the Linux routing stack follow the same pattern. Review
CNI-specific policy resources before cutover, since policy enforcement is off during migration.

## Verify
- [ ] `cilium connectivity test` (or e2e network focus) passes; every pod IP is from the new CIDR.
- [ ] `ls /etc/cni/net.d` on each node shows only the new CNI's config.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: kubeadm create-cluster page (--pod-network-cidr and the CNI add-on requirement), kubeadm source (podSubnet sets controller-manager --allocate-node-cidrs and --cluster-cidr), network-plugins page (default /etc/cni/net.d and /opt/cni/bin), containerd CRI config (cni_conf_dir and cni_max_conf_num default 1), Cilium kubeadm, Kubernetes host-scope IPAM and migration guides (requirements, limitations, per-node CiliumNodeConfig flow) the Flannel manifest URL used in the Cilium guide and the Calico custom-resources manifest (Installation calicoNetwork ipPools cidr). Replaced pinned Cilium and Calico versions and removed the unconfirmed lexical-order and interface-name claims.

Method: documentation only; no commands were run.
