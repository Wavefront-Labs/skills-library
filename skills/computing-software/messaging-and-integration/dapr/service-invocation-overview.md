---
id: computing-software.messaging-and-integration.dapr.service-invocation-overview
name: service-invocation-overview
category: computing-software
field: messaging-and-integration
product: dapr
tags: [service-invocation, sidecar, mtls, name-resolution, mdns, load-balancing, app-id, building-blocks]
level: practitioner
status: docs-checked
description: "How Dapr service invocation routes calls sidecar to sidecar: app ID, name resolution, mDNS round robin, mTLS, retries, tracing, access control and HTTP streaming."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/service-invocation/service-invocation-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service invocation lets one app call another through the local Dapr sidecar over HTTP or gRPC. The sidecar acts like a reverse proxy with built-in discovery; the caller targets the other app by its app ID.

Call flow: service A calls its own sidecar; the sidecar finds service B through a name resolution component for the hosting platform; it forwards to B's sidecar; B's sidecar calls the specified endpoint on B; the response returns the same way. Sidecar to sidecar traffic always uses gRPC; only app to sidecar legs may be HTTP or gRPC.

Example from the page: a Python app invokes the Node.js app with app ID `nodeapp` by POSTing:

```
http://localhost:3500/v1.0/invoke/nodeapp/method/neworder
```

Features listed:

- HTTP: add the `dapr-app-id` header without changing existing endpoint URLs. gRPC: keep your own proto services, no SDK needed.
- mTLS between sidecars through Sentry, with automatic certificate rollover on hosted platforms.
- Resiliency policies for retries and backoff; tracing and metrics on every call by default.
- Access control: which apps may call you and what they may do.
- Namespace scoping, so services in different namespaces can call each other.
- Round robin load balancing with mDNS across instances sharing one app ID (the app ID is per application, not per instance).
- Swappable discovery: Kubernetes DNS on Kubernetes, mDNS self-hosted, SQLite for single node or local development, Consul for multi-machine setups anywhere.
- Streaming of large HTTP request and response bodies.

For a quick test use `dapr invoke --method <method-name>`.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; wording tightened where it went beyond the page, the remaining claims are unchanged.

Method: documentation only; no commands were run.
