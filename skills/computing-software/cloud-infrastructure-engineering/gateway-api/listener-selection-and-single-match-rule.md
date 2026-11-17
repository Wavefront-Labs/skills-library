---
id: computing-software.cloud-infrastructure-engineering.gateway-api.listener-selection-and-single-match-rule
name: listener-selection-and-single-match-rule
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [traffic-matching, listener-selection, relevant-listeners, attachedroutes, 404]
level: advanced
status: docs-checked
description: "How traffic selects exactly one listener and one Route, and why a request missing that listener's routes gets 404 instead of falling back."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/traffic-matching.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/implementers-guide/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Matching order: traffic flows into an IP address (selecting a Gateway, since only Gateways have addresses), then a port (selecting one or more listeners); if several, `hostname` (for HTTP, HTTPS, TLS and their Routes) refines it. A single candidate Route is then chosen; on match conflicts between Routes the oldest Route's match is chosen.

The corollary: **traffic that matches no rule on its chosen listener cannot be rerouted to another listener that also matches.**

Example from the docs: Gateway `example-com` with listeners `specific` (`specific.example.com`, HTTP/80) and `wildcard` (`*.example.com`, HTTP/80). Two HTTPRoutes use `parentRefs` with only the Gateway name (no `sectionName`): `specific` (path `Exact /specific`) and `wildcard` (path prefix `/`). A request to `http://specific.example.com/specific` matches. A request to `http://specific.example.com/otherpath` returns 404, even though `*.example.com` and `/` would match, because the traffic was captured by the `specific` listener and cannot also match HTTPRoutes attached to other listeners.

Relevant listeners for a parentRef: all listeners on the Gateway; or, with a `sectionName`, only the listener whose `name` matches (none matching means the set is empty and the parentRef is ignored). The listener then restricts attachment by `allowedRoutes.kinds` and `allowedRoutes.namespaces` (`All`, `Same`, `Selector`); HTTPRoutes can also be rejected by hostname intersection. When attachment succeeds the Route is counted in the listener `status.attachedRoutes`.

The page's own YAML leaves `*.example.com` unquoted; quote wildcard hostnames in real manifests so YAML does not read `*` as an alias.

Implementers: this is "Listener Isolation": requests SHOULD match at most one Listener (a request to `foo.example.com` is routed only by Routes on that listener, not the wildcard one). Implementations that do not support it MUST document that.

## Checked

2026-11-08. Read in full (GitHub markdown): the traffic matching page, the API overview and the implementers guide. Confirmed: matching order, single-match corollary and 404 example, relevant listeners and sectionName rule, allowedRoutes restrictions, attachedRoutes, Listener Isolation wording. Added the implementers guide as a source. Removed: nothing unsupported beyond tightening the wording.

Method: documentation only; no commands were run.
