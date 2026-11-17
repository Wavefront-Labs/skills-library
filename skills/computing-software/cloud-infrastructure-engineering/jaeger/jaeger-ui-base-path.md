---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-ui-base-path
name: jaeger-ui-base-path
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, base-path, reverse-proxy, url-prefix, jaeger-query-base-path]
level: advanced
status: docs-checked
description: "Serve Jaeger UI under a URL prefix by setting base_path to the path the proxy forwards, not the path the browser sees."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: host the UI at something like https://example.com/jaeger/.

Two prefixes are involved:
- External prefix: what the browser shows. Configured at the proxy; Jaeger does not need to know it, because since v2.18.0 the UI detects the prefix from the browser URL on every page load. Several external prefixes can serve one instance.
- Internal prefix: the path Jaeger registers its routes under (HTML page, static assets, REST API), set by `base_path`. Default `/`.

The proxy may forward the path unchanged, strip the external prefix, or rewrite it to a different internal value. `base_path` always describes the path Jaeger sees:
```
extensions:
  jaeger_query:
    base_path: /jaeger
```
Rules: it must start with `/`, contain no `..` or duplicate slashes; a trailing `/` is allowed but stripped. If Jaeger receives requests at the root, leave it at the default.

The rewrite scenario (proxy changes the external prefix to a different internal one) was previously impossible (issue #5157) and is now supported. A Docker Compose example with Apache httpd configs for forward, strip and rewrite routing is in the repository at examples/reverse-proxy/. Design background: ADR-009.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Configuration page, read in full: external and internal prefixes, v2.18.0 prefix detection, base_path rules and default, the rewrite scenario with issue #5157, examples/reverse-proxy/ and ADR-009.

Method: documentation only; no commands were run.
