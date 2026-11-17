---
id: computing-software.cloud-infrastructure-engineering.kubespray.environment-proxy-and-no-proxy
name: environment-proxy-and-no-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [proxy, http-proxy, no-proxy, custom-ca, additional-no-proxy]
level: practitioner
status: docs-checked
description: "Set http_proxy and https_proxy for all nodes, trust a custom CA with https_proxy_cert_file, extend no_proxy with additional_no_proxy and use no_proxy_exclude_workers."
sources:
  - https://kubespray.io/docs/advanced/proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When you set `http_proxy` and `https_proxy`, Kubespray excludes all nodes and load balancers from proxying by generating `no_proxy` in `roles/kubespray_defaults/tasks/no_proxy.yml`.

Settings from the page:

```
http_proxy:"http://example.proxy.tld:port"
https_proxy:"http://example.proxy.tld:port"
```

Custom CA, which must already be present on every target node:

```
https_proxy_cert_file: /path/to/host/custom/ca.crt
```

Override the generated list completely by filling only `no_proxy`; then no node or load balancer addresses are added:

```
no_proxy: "node1,node1_ip,node2,node2_ip...additional_host"
```

Keep the generated list but add entries:

```
additional_no_proxy: "additional_host1,additional_host2"
```

**Worker churn.** Because workers are in `no_proxy` by default, the docker engine restarts on all nodes (and all pods restart) when workers are added or removed. To include only control plane nodes in `no_proxy` and avoid that:

```
no_proxy_exclude_workers: true
```

## Checked

2026-11-04. Every variable was confirmed on the Setting up Environment Proxy page; removed an unsupported closing inference.

Method: documentation only; no commands were run.
