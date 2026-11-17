---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.discovery-kubernetes
name: discovery-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, service-discovery, kubernetes, namespace-selector, endpoint-slices]
level: advanced
status: docs-checked
description: "Discover Kubernetes endpoints from APISIX: the discovery.kubernetes block (service, client token, default_weight, namespace_selector, shared_size) and the service_name format."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/discovery/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes service discovery

`conf/config.yaml`:

```yaml
discovery:
  kubernetes:
    service:
      schema: https                 # default: https
      host: ${KUBERNETES_SERVICE_HOST}
      port: ${KUBERNETES_SERVICE_PORT}
    client:
      token_file: /path/to/serviceaccount/token
    default_weight: 50              # default: 50, minimum: 0
    namespace_selector:
      equal: default
    shared_size: 64m                # default: 64m
    watch_endpoint_slices: false    # default: false
```

Upstream:

```json
{ "type": "roundrobin", "discovery_type": "kubernetes", "service_name": "default/plat-dev:port" }
```

`service_name` follows `[namespace]/[name]:[portName]`, where `portName` is the `ports.name` of the Kubernetes endpoints (if there is no `ports.name`, `targetPort` or `port` is used; if `ports.name` exists, a port number cannot be used). Inside a pod the minimal config `discovery: { kubernetes: { } }` is enough.

## Checked

2026-11-04: read the Kubernetes discovery page; the config block, defaults (https, 50, 64m, false), the namespace_selector and the service_name pattern match. The token_file value is a placeholder; the page uses the in-pod serviceaccount token path. Added the portName rule and the in-pod minimal config from the page.

Method: documentation only; no commands were run.
