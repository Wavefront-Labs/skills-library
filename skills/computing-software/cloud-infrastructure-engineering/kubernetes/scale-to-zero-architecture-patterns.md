---
id: computing-software.cloud-infrastructure-engineering.kubernetes.scale-to-zero-architecture-patterns
name: scale-to-zero-architecture-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, scale-to-zero, knative, keda, activator, serverless, idle-detection, queue-proxy, cold-start, faas]
level: advanced
status: docs-checked
description: "How KEDA and Knative each implement scale-to-zero, the request-buffering activator pattern that makes zero safe, and when zero is the wrong target."
sources: ["https://github.com/knative/docs/blob/main/docs/versioned/serving/autoscaling/scale-to-zero.md", "https://github.com/knative/docs/blob/main/docs/versioned/serving/autoscaling/autoscaler-types.md", "https://github.com/knative/docs/blob/main/docs/versioned/serving/autoscaling/concurrency.md", "https://github.com/knative/serving/blob/main/docs/scaling/SYSTEM.md", "https://keda.sh/docs/latest/concepts/scaling-deployments/", "https://keda.sh/http-add-on/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scale-to-zero architecture patterns

**Goal:** understand the mechanism that makes "zero replicas" survivable for a request-driven
workload — it is not just `minReplicas: 0`, it requires something to catch traffic while nothing
is running.

## 1. The fundamental problem zero creates
A Deployment at zero replicas has no Endpoints — a Service routing to it drops traffic with
connection refused/no endpoints, instantly, for any request that arrives before something scales
it back up. Plain HPA can scale to zero only for object or external metrics (`minReplicas: 0`,
`HPAScaleToZero`, beta and on by default from Kubernetes 1.37; never CPU or memory), and it has
nothing that holds an inbound HTTP request. Every real request-driven scale-to-zero system solves
the same problem: **buffer or hold the request while a cold pod starts**, then release it once
ready. The two production patterns differ in where that buffer lives.

## 2. KEDA: event-driven, no request buffering for HTTP by default
KEDA's core scale-to-zero (ScaledObject `minReplicaCount: 0`) is built for **event sources with
their own durability** — a queue, a topic, a cron window. The event sits in the queue/broker while
the Deployment is at zero; KEDA polls the source and, when a scaler reports active, scales the
workload from 0 to 1 itself (the activation phase), after which the HPA it generated handles 1 to N.
No request is "waiting" in the Kubernetes sense — the broker already held it. This is why KEDA's
zero works safely for Kafka/SQS/RabbitMQ consumers: the queue is the buffer.
For **HTTP** scale-to-zero (a synchronous request needing a live pod right now), KEDA needs the
separate **KEDA HTTP Add-on** (beta per its README), which deploys an **interceptor** that sits in
front of your application as a reverse proxy, routing requests and tracking concurrency, plus a
scaler that feeds those metrics to KEDA. This is functionally the same idea as Knative's activator,
because plain queue-based scale-to-zero has nothing to hold an inbound HTTP request. The add-on's
`HTTPScaledObject` is marked deprecated in its 0.16 docs in favour of `InterceptorRoute`; follow
the add-on docs for your version.

## 3. Knative Serving: the activator is the buffer
Knative's Pod Autoscaler (KPA, class `kpa.autoscaling.knative.dev`, the default) can scale a
Revision to zero; the HPA class (`hpa.autoscaling.knative.dev`) does not support scale to zero.
Scale to zero is on by default (`enable-scale-to-zero`) and is configured globally only, with a
`scale-to-zero-grace-period` of 30s. Each revision has a public and a private Service managed by a
ServerlessService, which has two modes: `Serve` (traffic goes to the revision's pods) and `Proxy`
(traffic goes to the **activator**), used while scaled to zero:
1. Request arrives at the activator (via the Knative ingress/gateway), not directly at the pod.
2. Activator sees zero ready pods, **holds the request** (buffers the connection), and signals the
   autoscaler to scale the Revision to 1.
3. Once the new pod is `Ready`, the activator forwards the held request to it and gets out of the
   path for subsequent requests (direct pod routing resumes once scaled up, activator steps back
   in only when scaling to zero again).
- Concurrency drives scaling: a soft target is set per revision with the
  `autoscaling.knative.dev/metric` and `autoscaling.knative.dev/target` annotations (global default
  `container-concurrency-target-default` is 100), and a hard limit with the revision's
  `containerConcurrency` field. If both are set the smaller applies; when the hard limit is reached,
  surplus requests are buffered until capacity is free.

## 4. When zero is the wrong target
- **Latency-sensitive synchronous paths** (user-facing API calls with a tight SLA) pay the full
  cold-start cost (image pull if not cached, container start, app init, JIT/connection-pool
  warmup) on every scale-from-zero — often seconds, sometimes much more for heavy runtimes (JVM,
  large ML model loads). If p99 latency matters more than idle cost, keep `minReplicas: 1` instead
  of 0, or use a low non-zero floor with cold-start mitigation (see the companion skill).
- **Workloads with expensive, slow-to-rebuild in-memory state** (large caches, loaded models) lose
  that state every time they scale to zero — the cost of rebuilding it on every cold start can
  exceed the idle-compute savings.
- Zero is a strong fit for: internal/low-traffic admin tools, batch consumers triggered by rare
  events, preview/staging environments, anything where occasional multi-second latency on the
  first request is acceptable and idle periods are long relative to active periods.

## Gotchas
- Scaling to zero removes **all** pods, including however many you'd normally keep for
  availability — a zero-floor workload has a guaranteed single-point-of-failure window on every
  cold start; this is an explicit tradeoff, not a bug to "fix."
- In Knative, all traffic for scaled-to-zero revisions flows through the activators, a shared
  dependency; size and monitor them accordingly.
- KEDA's core scaler (non-HTTP) genuinely has no request in flight when scaled to zero — don't
  wire a synchronous HTTP path through plain KEDA ScaledObject scale-to-zero expecting Knative-like
  buffering; that traffic will simply fail until the add-on or an activator-equivalent is added.
- Node-level scale-to-zero (no nodes at all, not just no pods) interacts with the node autoscaler's
  own cold-start cost on top of the pod cold-start cost — see the cold-start mitigation skill for
  how these stack.

## Verify
- [ ] A cold request to a zero-scaled HTTP workload (through the activator/interceptor, not
      directly to a pod IP) succeeds rather than erroring, with the delay matching expected
      cold-start time.
- [ ] Queue-backed KEDA scale-to-zero shows zero message loss across a scale-to-zero-and-back
      cycle — verified by draining the queue fully after the cold start, not assuming it.
- [ ] The activator (or HTTP add-on interceptor) itself has enough replicas/resources to avoid
      being the bottleneck under a cold-start burst.
- [ ] Workloads chosen for zero have been checked against the "when zero is wrong" list above, not
      defaulted to zero cluster-wide for cost reasons alone.

## Checked

Checked 2026-10-27. Documentation checked: Knative docs repository (versioned serving autoscaling pages: scale-to-zero, autoscaler types, concurrency) and the Knative serving scaling system doc (main), KEDA scaling-deployments docs (2.22 tree; latest release v2.21.0), the KEDA HTTP Add-on README and 0.16 documentation index, Kubernetes website main tree (v1.38 dev; v1.37 latest release) HPA page. Confirmed: activator buffers requests and SKS Proxy/Serve modes; KPA supports scale to zero, HPA class does not; `enable-scale-to-zero` default true and 30s grace period; soft vs hard concurrency limits; KEDA 0<->1 activation vs HPA 1<->N; HTTP add-on interceptor; HPAScaleToZero beta from 1.37. Fixed: "HPA cannot express minReplicas 0" (now possible for object and external metrics), the claim that the Knative HPA class can scale to zero, and the description of who scales KEDA workloads from zero. Removed as unconfirmed: the queue-proxy sidecar description and the HPA polling comparison.

Method: documentation only; no commands were run.
