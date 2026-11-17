---
id: computing-software.messaging-and-integration.dapr.resiliency-targets-apps-components-actors
name: resiliency-targets-apps-components-actors
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, targets, apps, components, actors, inbound, outbound, pubsub, circuitbreakerscope]
level: practitioner
status: docs-checked
description: "Bind Dapr resiliency policies to targets: apps by app-id, components with outbound or inbound sections, pub/sub both ways, and actors with circuitBreakerScope and cache size."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/targets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Targets say where named policies apply. There are three types.

Apps: applies `retry`, `timeout` and `circuitBreaker` to service invocation calls, keyed by the target service `app-id`. Dapr already has built-in service invocation retries, so policies here are additional.

```yaml
specs:
  targets:
    apps:
      appB: # app-id of the target service
        timeout: general
        retry: general
        circuitBreaker: general
```

Components: use `outbound` for sidecar-to-component calls (persisting or retrieving state, publishing, invoking an output binding) and `inbound` for sidecar-to-app calls (pub/sub subscription delivery, input bindings). Some components have their own built-in retries.

```yaml
spec:
  targets:
    components:
      myStateStore:
        outbound:
          retry: retryForever
          circuitBreaker: simpleCB
      myInputBinding:
        inbound: 
          timeout: general
          retry: general
          circuitBreaker: general
```

A pub/sub component can carry both:

```yaml
      myPubsub:
        outbound:
          retry: pubsubRetry
          circuitBreaker: pubsubCB
        inbound: # inbound only applies to delivery from sidecar to app
          timeout: general
          retry: general
          circuitBreaker: general
```

Actors: same three policy keys per actor type, plus `circuitBreakerScope` choosing what a tripped breaker covers (`id` an individual actor, `type` all actors of the type, `both`) and `circuitBreakerCacheSize`, an integer such as `5000`, for how many breakers are kept in memory.

```yaml
    actors:
      myActorType:
        timeout: general
        retry: general
        circuitBreaker: general
        circuitBreakerScope: both
        circuitBreakerCacheSize: 5000
```

## Checked

2026-11-08. The three target types, the apps, components (outbound and inbound), pubsub and actors YAML, the additional-to-built-in service invocation retries note and the circuitBreakerScope values confirmed on the Resiliency Targets page. All claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
