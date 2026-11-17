---
id: computing-software.cloud-infrastructure-engineering.contour.contour-websockets-and-externalname-routing
name: contour-websockets-and-externalname-routing
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [enablewebsockets, externalname, enableexternalnameservice, host-header, security-advisory, upstream-protocol-tls]
level: practitioner
status: docs-checked
description: "Enabling WebSockets per route with enableWebsockets, and routing to ExternalName services (disabled by default for security) with Host header rewrite and TLS upstreams."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/websockets.md", "https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/external-service-routing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WebSockets and ExternalName routing

WebSockets: enable per route.

```yaml
routes:
- conditions: [{prefix: /websocket}]
  enableWebsockets: true
  services: [{name: chat-app, port: 80}]
```

It applies to all paths matching that route. With Gateway API, websockets are enabled by default at the Listener level.

ExternalName: HTTPProxy can route to Services of type `ExternalName`, but it is off by default because it can expose the Envoy admin UI (remote shutdown/restart) and can reach services in namespaces a user cannot access (e.g. `service.namespace.svc.cluster.local`). Not recommended without a strong use case. Enable with `enableExternalNameService: true` in the Contour config file.

Behaviour:
- Contour uses the `spec.externalName` DNS name instead of EDS. `localhost` and synonyms are rejected.
- Service ports must be specified.
- Use `requestHeadersPolicy` to rewrite `Host` to the external resource's expected name (for example a hosted object-store bucket).
- If the upstream speaks TLS, set `protocol: tls` on the HTTPProxy service, or annotate the ExternalName Service with `projectcontour.io/upstream-protocol.tls: 443,https`.

## Checked

2026-11-08. Read the Contour main-branch config pages websockets.md and external-service-routing.md in full. Confirmed: `enableWebsockets` per route, Gateway API default, ExternalName disabled by default and the reasons, `enableExternalNameService`, `spec.externalName` in place of EDS, localhost rejection, required ports, Host rewrite via `requestHeadersPolicy`, and the TLS options. Removed the `cluster.dns-lookup-family` line, which neither page states.

Method: documentation only; no commands were run.
