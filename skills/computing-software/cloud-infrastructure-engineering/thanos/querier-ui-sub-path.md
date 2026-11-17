---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-ui-sub-path
name: querier-ui-sub-path
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, route-prefix, external-prefix, reverse-proxy]
level: practitioner
status: docs-checked
description: "Serve the Thanos Query UI under a sub-path using web.route-prefix, web.external-prefix and a prefix header."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Query UI on a sub-path

Static prefixing follows Prometheus: `--web.route-prefix` sets the HTTP request path prefix for endpoints, and `--web.external-prefix` prefixes URLs in HTML and redirects.

Thanos also supports dynamic prefixing via a request header, which Prometheus does not. This helps behind a reverse proxy or Kubernetes ingress that strips a path. With Traefik, the `PathPrefixStrip: /some-path` rule (or the `traefik.frontend.rule.type: PathPrefixStrip` ingress annotation) writes the stripped prefix to the `X-Forwarded-Prefix` header. Then start the Querier with:

```
thanos query --web.prefix-header=X-Forwarded-Prefix ...
```

so redirects and links carry the stripped path.

**Related.** `--query.active-query-path` takes a directory in which a `queries.active` file tracks in-flight queries; it is disabled while the value is the default empty string.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
