---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-urlrewrite-host-and-path
name: httproute-urlrewrite-host-and-path
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, urlrewrite, rewrite, replacefullpath, replaceprefixmatch, httroutepathrewrite]
level: practitioner
status: docs-checked
description: "Rewrite the upstream hostname and path with the URLRewrite filter: ReplaceFullPath versus ReplacePrefixMatch, and the rule that rewrite and redirect cannot be combined."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-redirect-rewrite.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/examples/standard/http-redirect-rewrite/httproute-rewrite-prefix-path.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `URLRewrite` filter changes the request sent **upstream**; the client does not see it (contrast with `RequestRedirect`). Path rewrite is Extended (`HTTPRoutePathRewrite`).

Hostname rewrite: a request for `https://rewrite.example/cardamom` is sent to `example-svc` with `host: elsewhere.example` instead of `host: rewrite.example`.

```yaml
filters:
- type: URLRewrite
  urlRewrite:
    hostname: elsewhere.example
```

Path rewrite uses an HTTP path modifier:

```yaml
filters:
- type: URLRewrite
  urlRewrite:
    path:
      type: ReplaceFullPath
      replaceFullPath: /fennel
```

`https://rewrite.example/cardamom/smidgen` becomes `/fennel` upstream.

```yaml
    path:
      type: ReplacePrefixMatch
      replacePrefixMatch: /fennel
```

In the guide's example, the rule matches path prefix `/cardamom` and `/cardamom/smidgen` becomes `/fennel/smidgen` upstream (host `elsewhere.example`).

Constraints:

- Rewrite and redirect filters are mutually incompatible: URLRewrite and RequestRedirect may not be combined in one rule.
- If incompatible or unsupported filters cause the `Accepted` condition to be `False`, implementations may use the reason `IncompatibleFilters`.
- The order of effects of multiple filter behaviours is currently unspecified, and repeating a core filter has unspecified or implementation-specific behaviour.

## Checked

2026-11-08. Read in full: the HTTP path redirects and rewrites guide and the HTTPRoute reference (raw markdown on GitHub), plus the three rewrite example manifests in the repo (field names urlRewrite.hostname, path.type, replaceFullPath and replacePrefixMatch checked there). Confirmed: URLRewrite changes the upstream request hostname and path, the Extended feature HTTPRoutePathRewrite, the three worked examples, redirect and rewrite incompatibility, IncompatibleFilters and the unspecified filter ordering. Removed: the claim that rule-level filters are Core and backendRef-level filters Extended, which is not on the pages.

Method: documentation only; no commands were run.
