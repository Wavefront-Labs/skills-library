---
id: computing-software.cloud-infrastructure-engineering.talos-linux.kubeprism-local-apiserver-lb
name: kubeprism-local-apiserver-lb
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [kubeprism, high-availability, kube-apiserver, load-balancer, kubeprismconfig, cni, upgrade-k8s]
level: advanced
status: docs-checked
description: "KubePrism: the per-node localhost TCP load balancer for the Kubernetes API (default port 7445), how it picks endpoints, what it reconfigures, and what CNIs need."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/kubeprism.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Host-networking components (control plane, CNI) cannot use `kubernetes.default.svc` and depend on the external cluster endpoint. If that endpoint fails, pods stop scheduling and service IPs break. KubePrism gives every node an in-cluster highly available API endpoint.

It is enabled by default on port 7445. To customise, use the document below; to disable, remove it. The port must be free on every node.

```yaml
apiVersion: v1alpha1
kind: KubePrismConfig
port: 7445
```

**How it works.** Talos runs a TCP load balancer on `localhost` at that port. Its backend candidates are the external cluster endpoint from the machine config, on control plane machines `https://localhost:<api-server-local-port>` (`https://localhost:6443` by default), and `https://<controlplane-address>:<api-server-port>` for each control plane machine learnt from cluster discovery. Unhealthy or unreachable endpoints are filtered out and lower-latency ones preferred. In the worst case it behaves like the external endpoint; control plane nodes should normally use their local apiserver; workers may use a direct control plane address if faster.

Talos automatically reconfigures `kubelet`, `kube-scheduler` and `kube-controller-manager` to use it. The `kube-proxy` manifest also defaults to it, but when enabling KubePrism on a running cluster update that manifest with `talosctl upgrade-k8s`. CNIs that need the API server (Cilium, Calico) should be given the KubePrism endpoint in their configuration. The listener is bound to localhost, so it is not usable from outside the node.

## Checked

2026-11-04. KubePrism page confirms default port, the KubePrismConfig document, backend list, filtering and the kube-proxy and CNI notes.

Method: documentation only; no commands were run.
