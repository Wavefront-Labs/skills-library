---
id: computing-software.cloud-infrastructure-engineering.contour.contour-load-balancing-and-session-affinity
name: contour-load-balancing-and-session-affinity
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [loadbalancerpolicy, roundrobin, weightedleastrequest, requesthash, cookie, session-affinity, sticky-sessions]
level: practitioner
status: docs-checked
description: "HTTPProxy loadBalancerPolicy strategies: RoundRobin, WeightedLeastRequest, Random, RequestHash header/query/source IP, Cookie session affinity and its caveats."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/request-routing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Load balancing strategies and session affinity

Set per route with `loadBalancerPolicy.strategy`:
- `RoundRobin` (default), `WeightedLeastRequest`, `Random`.
- `RequestHash`: hash of request attributes picks the endpoint; supports header, query parameter and source IP.
- `Cookie`: session affinity (sticky sessions).

```yaml
loadBalancerPolicy:
  strategy: RequestHash
  requestHashPolicies:
  - headerHashOptions:
      headerName: X-Some-Header
    terminal: true
  - headerHashOptions:
      headerName: User-Agent
  - hashSourceIP: true
```

Policies are evaluated in order; if a `terminal: true` policy yields a hash (header present), Envoy stops and skips later policies. A consistent header value gives cookie-like affinity without cookies. Query parameter hashing uses `queryParameterHashOptions.parameterName`.

Cookie affinity:

```yaml
loadBalancerPolicy:
  strategy: Cookie
```

Caveat: affinity assumes stable, robust backends. Kubernetes does not guarantee ordering or fixed pod sets, so any change to the pods behind a Service can redistribute clients around the hash ring. Applications that rely heavily on session affinity will see this.

Internal redirects: `internalRedirectPolicy` (`maxInternalRedirects`, `redirectResponseCodes: [302]`, `allowCrossSchemeRedirect: SafeOnly`, `denyRepeatedRouteRedirect: true`) makes Envoy follow a 3xx internally and send the follow-up request with `x-envoy-original-url` set, returning the final response to the client.

## Checked

2026-11-08. Read the Contour main-branch config page request-routing.md in full. Confirmed: the five strategies and the RoundRobin default, RequestHash on headers, query parameters and source IP, the `terminal` behaviour, Cookie session affinity and its caveat, and the internal redirect policy fields and flow. No claims removed.

Method: documentation only; no commands were run.
