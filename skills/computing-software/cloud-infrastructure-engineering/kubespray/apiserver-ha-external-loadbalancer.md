---
id: computing-software.cloud-infrastructure-engineering.kubespray.apiserver-ha-external-loadbalancer
name: apiserver-ha-external-loadbalancer
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ha, haproxy, kube-apiserver-endpoint, supplementary-addresses, vip]
level: advanced
status: docs-checked
description: "Configure kube_apiserver_endpoint for an external HAProxy VIP, avoid port conflicts via kube_apiserver_bind_address and add VIPs to SANs with supplementary_addresses_in_ssl_keys."
sources:
  - https://kubespray.io/docs/operations/ha-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray uses two variables for API endpoints:
- `kube_apiserver_endpoint`: used from outside the cluster (kubectl, CI/CD).
- `kube_apiserver_cluster_internal_endpoint`: used inside (nodes, hostNetwork pods); optional, defaults to `kube_apiserver_endpoint` or the localhost LB.

The legacy `loadbalancer_apiserver`, `apiserver_loadbalancer_domain_name` and `kubeadm_config_api_fqdn` variables were removed in v2.33.0.

Page example HAProxy frontend (managed outside Kubespray):

```raw
listen kubernetes-apiserver-https
  bind <VIP>:8383
  mode tcp
  option log-health-checks
  timeout client 3h
  timeout server 3h
  server master1 <IP1>:6443 check check-ssl verify none inter 10000
  server master2 <IP2>:6443 check check-ssl verify none inter 10000
  balance roundrobin
```

and the matching variables:

```yml
kube_apiserver_endpoint: "https://<VIP>:8383"
# Optional: if different from external endpoint
kube_apiserver_cluster_internal_endpoint: "https://<VIP>:8383"
```

The apiserver binds all interfaces by default, so use a different port on the VIP or set `kube_apiserver_bind_address`, otherwise HAProxy cannot bind that port on the VIP.

If the LB has both a domain name and a VIP, set the endpoint to the domain name and add the VIP to `supplementary_addresses_in_ssl_keys` so both are in the certificate SANs. Kubespray does not handle TLS termination for an unmanaged external LB.

## Checked

2026-11-04. Variables, removal version, HAProxy block and notes were confirmed on the HA endpoints page.

Method: documentation only; no commands were run.
