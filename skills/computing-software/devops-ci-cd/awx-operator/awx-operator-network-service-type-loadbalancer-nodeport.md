---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-network-service-type-loadbalancer-nodeport
name: awx-operator-network-service-type-loadbalancer-nodeport
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, service-type, loadbalancer, nodeport, clusterip, service-annotations]
level: practitioner
status: docs-checked
description: "Choose and tune the AWX Service type: ClusterIP default, LoadBalancer options with HTTPS port rules, and NodePort."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/network-and-tls-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator network service type loadbalancer nodeport

`service_type` accepts `ClusterIP` (the default when unset), `LoadBalancer` and `NodePort`. For any type, `service_labels` and `service_annotations` can be set (default empty).

LoadBalancer-only variables: `loadbalancer_protocol` (http), `loadbalancer_port` (80), `loadbalancer_ip` (empty) and `loadbalancer_class` (empty).

```yaml
spec:
  service_type: LoadBalancer
  loadbalancer_ip: '192.168.10.25'
  loadbalancer_protocol: https
  loadbalancer_port: 443
  loadbalancer_class: service.k8s.aws/nlb
  service_annotations:
    environment: testing
  service_labels:
    environment: testing
```

For an HTTPS load balancer you are required to set `loadbalancer_port` away from 80. The HTTPS load balancer also uses SSL termination at the load balancer level and offloads traffic to AWX over HTTP.

NodePort: `nodeport_port` defaults to 30080.

```yaml
spec:
  service_type: NodePort
  nodeport_port: 30080
```

## Checked

2026-11-04. Confirmed against the AWX Operator "Network and TLS Configuration" page (Service Type section): supported types, ClusterIP default, `service_labels`/`service_annotations`, the four LoadBalancer variables and defaults, the HTTPS port and SSL-termination notes, and `nodeport_port` 30080. Removed the Kind/Minikube remark, the Ingress/Route relationship paragraph and the basic-install localhost port detail (not on this page), and changed the annotations example to the mapping form the page shows.
Method: documentation only; no commands were run.
