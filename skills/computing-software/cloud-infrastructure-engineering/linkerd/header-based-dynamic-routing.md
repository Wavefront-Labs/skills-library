---
id: computing-software.cloud-infrastructure-engineering.linkerd.header-based-dynamic-routing
name: header-based-dynamic-routing
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, httproute, routing, headers, ab-testing]
level: practitioner
status: docs-checked
description: "Route requests to an alternative backend when a header matches, using an HTTPRoute with header matches."
sources:
  - https://linkerd.io/2.19/tasks/configuring-dynamic-request-routing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic request routing lets an HTTPRoute choose a backend from request properties such as headers, which supports A/B testing and testing a new version on selected requests.

A route's rules can contain `matches` with `headers`. If several headers are listed they must all match (the matchers are ANDed). A request that matches is sent to that rule's `backendRefs`; requests without the header fall through to the default rule.

The guide's example sends requests carrying `x-request-id: alternative` to a second backend and everything else to the original. You can then confirm the routing by sending a request with and without the header and comparing which backend answers:

```bash
curl -H "x-request-id: alternative" http://frontend:9898/
```

Key points:

- `parentRefs` names the resource the HTTPRoute acts on (in the guide, a backend Service).
- Matchers inside one `matches` entry are ANDed; separate `matches` entries are ORed.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/configuring-dynamic-request-routing/.

Removed or reworded: Meshed-client, header-propagation, weighted-backend and contract claims.

Method: documentation only; no commands were run.
