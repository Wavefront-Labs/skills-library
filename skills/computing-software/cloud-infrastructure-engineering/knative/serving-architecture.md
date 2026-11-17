---
id: computing-software.cloud-infrastructure-engineering.knative.serving-architecture
name: serving-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [serving-architecture, activator, queue-proxy, autoscaler, kingress, networking-layer]
level: intro
status: docs-checked
description: "Name the Serving components (activator, autoscaler, controller, queue-proxy, webhooks) and the pluggable networking layer."
sources:
  - https://knative.dev/docs/serving/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand which Knative Serving component does what before debugging or tuning it.

Components:
- Activator: part of the data plane. It queues incoming requests when a Knative Service is scaled to zero, signals the autoscaler to bring it back, and forwards the queued requests.
- Autoscaler: scales Knative Services from configuration, metrics and incoming requests.
- Controller: watches Knative objects, manages dependent resources and updates resource state.
- Queue-Proxy: a sidecar in each Service pod. It collects metrics and enforces the desired concurrency when forwarding requests to the user container; it can also act as a queue.
- Webhooks: validate and mutate Knative resources.

Networking: Serving depends on a networking layer that fulfils the Knative Networking Specification. It defines an internal `KIngress` resource as an abstraction over pluggable layers; the community supports net-kourier, net-contour and net-istio. Here "Ingress" does not mean the Kubernetes Ingress resource.

Each networking layer has a controller that watches `KIngress` resources, configures the Ingress Gateway, and reports status back. The gateway routes requests to the activator or straight to a Service pod, depending on mode. To be reachable from outside the cluster it must be exposed through a Kubernetes Service of `type: LoadBalancer` or `type: NodePort`.

If you configure DNS, set the same domain in Knative as well.

## Checked

Method: docs-checked 2026-11-09 against the Knative Serving Architecture page (raw markdown in knative/docs, read in full).
