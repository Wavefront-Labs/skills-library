---
id: computing-software.cloud-infrastructure-engineering.gateway-api.hostnames-wildcards-and-intersection
name: hostnames-wildcards-and-intersection
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [hostnames, wildcard, intersection, listener, httproute, matching]
level: practitioner
status: docs-checked
description: "Hostname rules: a wildcard is leftmost only and matches one or more labels, and Route hostnames must intersect the listener hostname."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/hostnames.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/traffic-matching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hostnames appear on listeners (`listeners[].hostname`, at most one per listener, in a Gateway or ListenerSet) and on Routes (`spec.hostnames`, treated as an OR). A Route can attach to a listener only if the hostnames intersect, and the intersected hostname is what matters for routing.

Wildcard rules from the hostnames page:

- A wildcard is valid only as the leftmost character and must be followed by a `.`: `*.example.com` is valid, `f*.example.com` and `*oo.example.com` are not.
- Unlike many systems, it matches one or more DNS labels: `*.example.com` matches `www.example.com` and `sub.domain.example.com`, but not `example.com`; `*.com` matches `example.com` and `www.example.com`.
- IP addresses are never valid hostnames (validation may allow them today; the docs call that a bug, so do not depend on it). There are two types, `Hostname` and `PreciseHostname`; the latter does not allow wildcards.

Intersection rules and examples (listener, Route, intersected):

- `www.example.com`, `www.example.com` gives `www.example.com` (precise hostnames must match exactly).
- `*.example.com`, `www.example.com` gives `www.example.com`.
- `*.example.com`, `sub.domain.example.com` gives `sub.domain.example.com`.
- `www.example.com`, `*.example.com` gives `www.example.com` (works in both directions).
- `*.com`, `*.example.com` gives `*.example.com` (two wildcards intersect when they overlap).
- A missing hostname is equivalent to `*` and intersects everything. For HTTPRoute and GRPCRoute `hostnames` is optional; for TLSRoute it is required.

If the hostnames do not intersect, the Route is not accepted on that listener. Routes attach only where the listener allows them (`allowedRoutes`) and hostnames intersect.

Specificity: more labels without a wildcard is more specific, and exact beats wildcard when choosing a listener. For competing Routes, precedence uses the Routes' original hostnames, then creation timestamp, then name (see the route merging skill).

## Checked

2026-11-08. Read in full (GitHub markdown): the Hostnames page and the Traffic Matching page. Confirmed: wildcard validity and multi-label matching, hostname types, intersection rules and table rows, optional versus required hostnames, specificity ordering. Removed: the claim that a Route without hostnames "inherits" the listener hostname (the page says no hostname matches any), the `Accepted: False` reason `NoMatchingListenerHostname` (not on the fetched pages).

Method: documentation only; no commands were run.
