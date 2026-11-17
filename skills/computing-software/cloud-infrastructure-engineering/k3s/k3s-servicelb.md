---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-servicelb
name: k3s-servicelb
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, servicelb, loadbalancer-service, klipper]
level: practitioner
status: docs-checked
description: "How the built-in ServiceLB provides LoadBalancer Services via hostPort pods, and its limits."
sources:
  - https://docs.k3s.io/networking/networking-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upstream Kubernetes has no default LoadBalancer implementation, so such Services stay pending. K3s ships ServiceLB (formerly Klipper LoadBalancer), which uses available host ports, so LoadBalancer Services work without a cloud provider.

How it works:

- The controller watches Services with spec.type LoadBalancer.
- For each one it creates a DaemonSet in kube-system, which creates pods with a svc- prefix on each node. They use hostPort at the service port, so they only run on nodes where that port is free. If no node has the port available, the Service stays Pending. Several Services can share a node if their ports differ.
- If the node has an external IP, it is placed in the Service status.loadBalancer.ingress list with ipMode VIP; otherwise the node internal IP is used.
- With NAT (for example public cloud public IPs), traffic enters the pod via hostPort and the pod uses iptables to forward to the Service ClusterIP and port. Without NAT, traffic arriving for the LoadBalancer address is intercepted (normally kube-proxy iptables or ipvs) and forwarded to the ClusterIP.

Known issue: if external traffic arrives through NAT and you need externalTrafficPolicy=local (for client source IP preservation), do not define node-external-ip on any node, because it will not work correctly.

Disable with `--disable=servicelb` on all servers, needed for MetalLB; see the node pools skill.

## Checked

2026-11-08. Read the full K3s Networking Services page (docs/networking/networking-services.md in the k3s-io/docs repo). Confirmed: ServiceLB description, DaemonSet in kube-system with svc- prefixed hostPort pods, Pending behaviour, status.loadBalancer.ingress with ipMode VIP, NAT and non-NAT traffic paths, the externalTrafficPolicy and node-external-ip known issue, and --disable=servicelb for MetalLB. Removed the --servicelb-namespace sentence (not on the page).

Method: documentation only; no commands were run.
