---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-ha-stacked-vs-external-etcd
name: control-plane-ha-stacked-vs-external-etcd
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, high-availability, control-plane, etcd, stacked-etcd, external-etcd, kube-vip, haproxy, keepalived, load-balancer, quorum, api-server-ha, kubeadm, topology]
level: advanced
status: docs-checked
description: "Choose and build an HA kubeadm control plane: stacked vs external etcd topology, front-end LB/VIP options, and quorum sizing math."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/", "https://github.com/kubernetes/kubeadm/blob/main/docs/ha-considerations.md", "https://etcd.io/docs/v3.5/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-plane HA design: stacked vs external etcd

**Goal:** pick a control-plane topology that survives the node-count failures you
actually expect, and front it with a VIP/LB that doesn't become the single point of
failure you just removed from etcd. Backup/restore mechanics live in
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-backup-and-restore`;
membership/quorum-loss recovery in
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-cluster-membership-and-recovery`.

## 1. Stacked vs external etcd
- **Stacked**: etcd runs as a static pod on each control-plane node, co-located with
  the API server it serves. Fewer machines, simpler kubeadm workflow (the default for
  `kubeadm init`/`join --control-plane`). Risk: losing a control-plane node loses an
  etcd member *and* an API server replica simultaneously - with 3 nodes, 2 simultaneous
  losses takes etcd below quorum and the whole cluster down, not just degraded.
- **External**: etcd runs on its own dedicated node set, API servers on a separate set,
  each scaled independently. More machines and more complexity (separate TLS material,
  separate upgrade cadence), but a control-plane node failure doesn't touch etcd quorum,
  and you can run a different number of API server replicas than etcd members (the etcd
  FAQ suggests no more than seven members and notes write performance suffers in larger
  clusters).
- The kubeadm documentation calls stacked simpler to set up and manage, with the risk of
  coupled failure (mitigate by adding control-plane nodes; run at least three), and says
  external etcd needs twice the hosts: at least three control-plane hosts plus three etcd
  hosts. Choose external when you need etcd isolated from control-plane load or want
  control-plane failures to leave etcd membership untouched.

## 2. Quorum math (the number that actually matters)
- etcd tolerates `floor(n/2)` member failures and keeps quorum: 3 members tolerate 1
  loss, 5 tolerate 2. **Even numbers buy nothing** - 4 members still only tolerate 1
  loss (quorum is 3) while adding latency; always run an odd count.
- 3 is the practical minimum for any HA claim; 5 tolerates two failures, which the etcd FAQ
  calls enough in most cases. Larger clusters replicate data to more machines, so write
  performance suffers.
- Control-plane node count for stacked topology should equal (or exceed, for API-server
  scaling) the etcd member count, spread one-per-failure-domain (AZ/rack) - two members
  in the same AZ means that AZ's loss can take quorum with it.

## 3. Front-end load balancing / VIP
`controlPlaneEndpoint` (set at first `kubeadm init`, see
`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-bootstrap`)
must point at something that survives any one control-plane node dying:
- **External LB** (cloud load balancer, on-prem appliance or HAProxy pair) - a TCP-forwarding
  load balancer over all healthy control-plane nodes on port 6443; the kubeadm guide uses a
  TCP check, and an HTTPS probe of `/readyz` is the stricter option (see
  `apiserver-load-balancer-health-checks`). Its DNS name must always match
  `controlPlaneEndpoint`.
- **kube-vip** - runs as a static pod per control-plane node and implements both virtual IP
  management and load balancing, in layer 2 (ARP with leader election) or layer 3 (BGP)
  mode. Gotcha from the kubeadm guide: kube-vip needs API server access during
  `kubeadm init`, and since Kubernetes 1.29 `admin.conf` is not usable immediately, so
  initialise with `super-admin.conf` and switch to `admin.conf` afterwards.
- **keepalived + haproxy** static pods - haproxy load-balances to all control-plane nodes'
  6443 and keepalived moves the VIP using a health-check script; the hosts sharing the
  VIP must be in the same IP subnet. Two moving parts to keep in sync (haproxy's upstream
  list must track `kubeadm join --control-plane` additions).
- Whatever you choose, it must be reachable *before* a new control-plane node joins -
  joiners discover the API through `controlPlaneEndpoint`, so a chicken-and-egg LB
  config (LB only knows about nodes already in it) blocks scale-out.

## Gotchas
- Turning a single control-plane cluster created without `--control-plane-endpoint` into an
  HA cluster is not supported by kubeadm; set the endpoint at first `kubeadm init`.
- etcd treats disk latency as part of leader liveness (etcd FAQ): slow fsync on a stacked
  member's disk can cost the cluster its leader, which looks like network flakiness.
- kube-vip behaviour is version-sensitive; confirm against the kube-vip documentation for
  your versions before relying on it.

## Verify
- [ ] etcd member count is odd and spread across failure domains 1:1.
- [ ] Killing any single control-plane node leaves `kubectl get nodes`/`etcdctl
      endpoint health` fully functional from a client hitting only the VIP/LB.
- [ ] `controlPlaneEndpoint` in `kubeadm-config.yaml` (or `kubectl -n kube-system get cm
      kubeadm-config -o yaml`) matches the actual LB/VIP, not a single node's IP.
- [ ] A new control-plane node can `kubeadm join --control-plane` while one existing
      node is powered off.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: kubeadm HA-topology and HA setup pages (stacked is the default, minimum three control-plane nodes, external needs three plus three hosts, odd member counts), kubeadm create-cluster page (single control plane to HA unsupported without --control-plane-endpoint), kubeadm HA-considerations (keepalived same subnet, kube-vip modes, super-admin.conf workaround) and the etcd v3.5 FAQ (quorum table, odd sizes, seven-member guidance, disk latency and leader liveness). Removed the unconfirmed 20-node rule, 10 ms fsync figure and /livez advice.

Method: documentation only; no commands were run.
