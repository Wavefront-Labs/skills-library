---
id: computing-software.cloud-infrastructure-engineering.external-dns.set-identifier-annotation
name: set-identifier-annotation
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, set-identifier, routing-policy, weighted-records, route53-routing]
level: practitioner
status: docs-checked
description: "Use external-dns.kubernetes.io/set-identifier to publish several record sets for one name and type, with AWS routing policies and Gateway API Route placement."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# set-identifier annotation

A set identifier distinguishes multiple record sets that share the same domain and type. The configured routing policy then decides which sets answer queries.

- Required for AWS Route 53 weighted, latency, failover, geolocation, geoproximity and multi-value routing. The AWS tutorial's Routing policies section lists the annotations.
- The value is arbitrary but must be unique per record set for the same domain and type.
- It is provider-agnostic in design but mainly used with Route 53.

**Gateway API:** put it on the Route (for example `HTTPRoute`), never on the Gateway. The Gateway source reads only `target`.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
  annotations:
    external-dns.kubernetes.io/target: "alb-123.us-east-1.elb.amazonaws.com"
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-route
  annotations:
    external-dns.kubernetes.io/set-identifier: backend-v1
    external-dns.kubernetes.io/aws-weight: "100"
spec:
  parentRefs:
    - name: my-gateway
  hostnames:
    - app.example.com
```

The docs call placing it on the Gateway a common mistake.

## Checked

2026-11-04. Confirmed against the ExternalDNS annotations page (set-identifier section, Gateway API with HTTPRoute example and placement section). Removed an unsourced verification line.
Method: documentation only; no commands were run.
