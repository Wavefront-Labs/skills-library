---
id: computing-software.cloud-infrastructure-engineering.kubespray.apiserver-ha-localhost-loadbalancer
name: apiserver-ha-localhost-loadbalancer
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ha, kube-apiserver, loadbalancer, nginx-proxy, localhost-lb]
level: practitioner
status: docs-checked
description: "The default localhost nginx load balancer on non-master nodes and its variables loadbalancer_apiserver_localhost, loadbalancer_apiserver_port and loadbalancer_apiserver_pod_name."
sources:
  - https://kubespray.io/docs/operations/ha-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
etcd clients (kube-apiservers) are given the list of all etcd peers, so a multi-member etcd cluster is already highly available. The apiserver needs a reverse proxy.

Kubespray ships an nginx-based proxy on each non-master node, called localhost load balancing. It is less efficient than a dedicated load balancer because it adds health checks against the apiserver, but is practical when an external LB or virtual IP is inconvenient.

Variables:
- `loadbalancer_apiserver_localhost` defaults to `True`, or `False` if `kube_apiserver_endpoint` or `kube_apiserver_cluster_internal_endpoint` is defined.
- `loadbalancer_apiserver_port` is the port of the local balancer and defaults to `kube_apiserver_port`.
- `loadbalancer_apiserver_pod_name` controls the name of the load balancer container.

Kubespray only configures kubelet and kube-proxy on non-master nodes to use the local balancer.

Defining `kube_apiserver_endpoint` or `kube_apiserver_cluster_internal_endpoint` is mutually exclusive with `loadbalancer_apiserver_localhost`, apart from the special case of an internal LB used together with an external LB that Kubespray does not manage.

To skip the local balancer, use the kube-vip role or your own load balancer.

## Checked

2026-11-04. Variables, defaults and exclusivity were confirmed on the HA endpoints page.

Method: documentation only; no commands were run.
