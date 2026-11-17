---
id: computing-software.cloud-infrastructure-engineering.etcd.grpc-proxy
name: grpc-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [grpc-proxy, proxy, watch-coalescing, lease-coalescing, namespace, cache, scalability, etcd-grpc-proxy]
level: advanced
status: docs-checked
description: "Run the etcd gRPC proxy to fan in many clients: watch and lease coalescing, namespacing, caching and TLS termination."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/grpc_proxy/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The gRPC proxy is a stateless etcd reverse proxy operating at the gRPC layer (L7), designed to reduce the total processing load on the core cluster. It supports several endpoints: it randomly picks one at start and switches to another if it detects a failure.

```bash
etcd grpc-proxy start --endpoints=localhost:2379   --listen-addr=127.0.0.1:23790
```

Features:

- Watch coalescing: many client watchers on the same key or range become a single watcher on the server (load from N to 1). Limitation: when the watch revision is unspecified, a watcher through the proxy may start slightly behind the server's latest revision, and cancellation revisions may lag.
- Lease coalescing: client lease keep-alive streams are coalesced into one stream to the server.
- Abusive client protection: the proxy caches key range responses when that does not break consistency requirements.
- Namespacing: `--namespace=my-prefix/` adds a prefix to every key from clients and strips it in responses, giving each client its own subtree.
- Endpoint registration: `--advertise-client-url`, `--resolver-prefix` and `--resolver-ttl` (the example uses `___grpc_proxy_endpoint` and 60) register the proxy so clients can discover proxies with `Sync`; without a prefix, member list returns the proxy's own advertise URL.
- TLS termination: the proxy can serve an unencrypted local endpoint while connecting to a secure cluster using `--cert`, `--key` and `--cacert` (the page's example also passes `--insecure-skip-tls-verify`).
- `/health` and Prometheus `/metrics` endpoints for the members in `--endpoints`, or an extra URL via `--metrics-addr`.

Known issue: with TLS on the main listening interface, curl needs `--http1.1` to read `/metrics` or `/health`; the `--metrics-addr` interface does not have this requirement.

You can deploy multiple gRPC proxies to distribute server load further.

## Checked

2026-11-03. Confirmed on the v3.5 gRPC proxy page: stateless L7 reverse proxy, random endpoint pick and failover, watch and lease coalescing with the revision limitation, response caching, the start command and --listen-addr, endpoint registration flags and Sync, --namespace behaviour, TLS termination command, /health and /metrics and --metrics-addr, and the HTTP/1.1 known issue. Removed: the cache-size options, the linearizability statement, the supported-API list and the transactions remark, none of which appear on the page.

Method: documentation only; no commands were run.
