---
id: computing-software.cloud-infrastructure-engineering.etcd.gateway-tcp-proxy
name: gateway-tcp-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [gateway, tcp-proxy, etcd-gateway, endpoints, listen-addr, retry-delay, discovery-srv, l4-proxy]
level: practitioner
status: docs-checked
description: "The etcd gateway: a simple TCP proxy to cluster endpoints, with --endpoints, --listen-addr, --retry-delay and SRV discovery."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/gateway/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `etcd gateway` is a simple, stateless, transparent TCP proxy: it neither inspects client requests nor interferes with responses. It lets applications use a fixed local address so they need not know the cluster membership.

```bash
etcd gateway start --endpoints=10.0.1.10:2379,10.0.1.11:2379,10.0.1.12:2379
```

Flags:

- `--endpoints`: comma-separated etcd members to forward to (default `127.0.0.1:2379`; the port must be included; an `https://` URL is invalid because the gateway does not terminate TLS).
- `--listen-addr`: the address to listen on (default `127.0.0.1:23790`).
- `--retry-delay`: how long to wait before retrying a failed endpoint (default 1m0s).
- `--discovery-srv`: find endpoints with DNS SRV.
- `--insecure-discovery`: accept SRV records that are not secured.
- `--trusted-ca-file`: CA used only to authenticate the endpoints discovered through SRV, not to create data connections.

Behaviour: it uses a simple round-robin policy over the endpoints, only routes to available ones and hides failures from clients; `--retry-delay` is the delay before retrying a failed endpoint. It does not terminate TLS, do handshakes on behalf of clients or verify that a connection is secured.

When to use it: run a gateway on each machine and point every local application at it (default `127.0.0.1:23790`), so only the gateway needs updating when cluster endpoints change. The page advises against it for performance and on systems like Kubernetes that already provide service discovery.

The gateway provides no caching, watch coalescing or batching, so it does not improve cluster performance; the gateway page says the etcd team is developing a separate caching proxy for scalability.

Do not confuse with the grpc-gateway HTTP/JSON mapping.

## Checked

2026-11-03. Confirmed on the v3.5 etcd gateway page: TCP proxy, stateless and transparent, does not terminate TLS, round-robin over available endpoints, use case and non-use cases, `etcd gateway start --endpoints` and `--discovery-srv` forms, and the flag defaults (--endpoints 127.0.0.1:2379, --listen-addr 127.0.0.1:23790, --retry-delay 1m0s, --insecure-discovery false) and flag descriptions. Removed: layer 4 wording, namespacing and protocol-agnostic claims, and the gRPC-proxy comparison, which the page does not make.

Method: documentation only; no commands were run.
