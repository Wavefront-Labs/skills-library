---
id: computing-software.cloud-infrastructure-engineering.knative.request-flow
name: request-flow
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [request-flow, cold-start, scale-from-zero, activator-in-path, selectorless-service]
level: practitioner
status: docs-checked
description: "Trace how requests reach a revision at zero, low and high traffic and when the activator leaves the path."
sources:
  - https://knative.dev/docs/serving/request-flow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict whether a request passes through the activator and when a cold start happens.

The HTTP router (the pluggable ingress layer), the activator and the autoscaler are shared cluster-level resources, so an idle Knative Service costs only metadata. Routing is decided once per request at the router and recorded in an internal header.

Scale from zero: with low or zero traffic the router sends requests to the activator, with a header naming the selected Revision. The activator delays the request and signals the autoscaler that capacity is needed. The autoscaler raises the pod count requested from Kubernetes; once a new pod is ready or an existing pod has capacity, the activator forwards the delayed request. Starting a new pod to serve a request is a cold start.

High scale: when spare capacity exceeds `target-burst-capacity`, the ingress is programmed with pod addresses directly and the activator leaves the path. The queue-proxy always stays in the path. Traffic returns to the activator when:

```text
current_demand + target-burst-capacity > (pods * concurrency-target)
```

The Revision's Kubernetes Service is selectorless, holding either pod endpoints or activator endpoints. Reasons: some ingresses forbid cross-namespace references (the activator lives in `knative-serving`), some handle changing a backing Service poorly, and subsetting funnels requests to a few activators per Revision for better capacity decisions.

## Checked

2026-11-04. Confirmed against the HTTP Request Flows page (knative/docs source): shared cluster-level HTTP router, activator and autoscaler with only metadata cost when idle, per-request routing recorded in an internal header, the scale-from-zero sequence, cold start definition, activator removal when spare capacity exceeds `target-burst-capacity`, queue-proxy always staying in the path, the re-programming formula, and the three reasons for the selectorless Service. Widened the forwarding sentence to include an existing pod with capacity, as the page states. Nothing removed.

Method: documentation only; no commands were run.
