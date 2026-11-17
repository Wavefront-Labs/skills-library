---
id: computing-software.cloud-infrastructure-engineering.istio.istio-virtualservice-routing
name: istio-virtualservice-routing
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, virtualservice-routing, virtualservice, request-routing]
level: practitioner
status: docs-checked
description: "Route traffic by header, path or weight with a VirtualService: rule ordering, match semantics, FQDN hosts and the DestinationRule subsets it depends on."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/request-routing/", "https://istio.io/latest/docs/reference/config/networking/virtual-service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A VirtualService holds an ordered list of HTTP routes; the first rule matching a request is used. Inside one `match` block conditions are ANDed, and separate match blocks are ORed.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: {name: reviews}
spec:
  hosts: [reviews.shop.svc.cluster.local]
  http:
  - match: [{headers: {end-user: {exact: jason}}}]
    route: [{destination: {host: reviews.shop.svc.cluster.local, subset: v2}}]
  - route: [{destination: {host: reviews.shop.svc.cluster.local, subset: v1}}]
```

Gotchas: put the catch-all route last. A `subset` must be declared in a corresponding DestinationRule. Use a fully qualified domain name for the destination: the reference shows a rule in `istio-system` using `productpage.prod.svc.cluster.local`, where the rule's namespace has no effect on name resolution. Without an explicit default version, Istio routes to all versions round robin (the request-routing task). Header keys in a match must be lowercase with hyphens.

Task flow: apply routes to v1 for every service, then add the `end-user: jason` match to send that user to reviews:v2; the task confirms the rule and subsets with `kubectl get virtualservices -o yaml` and `kubectl get destinationrules -o yaml`.

## Checked

2026-11-03. Confirmed against the VirtualService reference (first match wins, AND/OR match semantics, FQDN note, subset must be defined in a DestinationRule, header match key rules) and the Request Routing task (round robin without defaults, jason to v2). Removed: unsourced claims about short-name resolution, black-holed subsets, dropped destinations, `v1beta1`, multi-VirtualService merging, the invented curl and `istioctl analyze` steps.
Method: documentation only; no commands were run.
