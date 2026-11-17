---
id: computing-software.cloud-infrastructure-engineering.contour.contour-upstream-weighting-and-mirroring
name: contour-upstream-weighting-and-mirroring
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [weight, canary, traffic-mirroring, multiple-upstreams, requestredirectpolicy, httpproxy]
level: practitioner
status: docs-checked
description: "HTTPProxy multiple upstreams, relative weights for canaries, traffic mirroring with weight percentage, and requestRedirectPolicy host redirects."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/request-routing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upstream weighting, mirroring and redirects

Multiple services on one route are load balanced across all. Add `weight` for canaries:

```yaml
services:
- {name: s1, port: 80, weight: 10}
- {name: s2, port: 80, weight: 90}
```

Weight rules:
- No weights: even distribution.
- Weights are relative, not required to sum to 100 (20, 30, 20 gives the 30 about 42.9%).
- If only some services have weights, those without get implicit weight 0 and receive no traffic.

Mirroring: mark one service `mirror: true`.

```yaml
services:
- {name: www, port: 80}
- {name: www-mirror, port: 80, mirror: true, weight: 5}
```

The mirror gets a copy of traffic sent to non-mirror services; responses are discarded. `weight` (1-100) mirrors that percentage; omitting it mirrors 100%. Explicit `weight: 0` also mirrors 100% because zero is indistinguishable from unset.

Redirects: `requestRedirectPolicy` on a route implements an HTTP redirect:

```yaml
routes:
- conditions: [{prefix: /}]
  requestRedirectPolicy:
    hostname: www.example.com
```

The scheme, port, status code and a path or prefix replacement can also be set. The page's example also defines a separate root HTTPProxy for the destination host.

## Checked

2026-11-08. Read the Contour main-branch config page request-routing.md in full. Confirmed: multiple upstreams, weight rules and the 42.9% example, traffic mirroring semantics (copy of read traffic, discarded responses, weight 1-100, omitted or 0 mirrors 100%), and `requestRedirectPolicy` options. Removed the claim that a redirect route must have no services.

Method: documentation only; no commands were run.
