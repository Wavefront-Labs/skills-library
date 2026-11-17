---
id: computing-software.messaging-and-integration.dapr.resiliency-spec-structure-and-scopes
name: resiliency-spec-structure-and-scopes
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, resiliency-yaml, policies, targets, scopes, kubectl-apply, limitations]
level: practitioner
status: docs-checked
description: "Structure of a Dapr Resiliency resource: scopes, named timeouts, retries and circuitBreakers, targets for apps, actors and components, file location, gRPC limitation."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/resiliency-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Resiliency resource defines named policies and then binds them to targets. In self-hosted mode it sits with the components and must be named `resiliency.yaml`; on Kubernetes apply it with `kubectl apply -f <resiliency-spec-name>.yaml` and Dapr finds the specs used by an app. `scopes` limits it to listed app IDs.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Resiliency
metadata:
  name: myresiliency
scopes:
  - app1
  - app2
spec:
  policies:
    timeouts:
      general: 5s
      important: 60s
      largeResponse: 10s
    retries:
      pubsubRetry:
        policy: constant
        duration: 5s
        maxRetries: 10
      retryForever:
        policy: exponential
        maxInterval: 15s
        maxRetries: -1 # retry indefinitely
    circuitBreakers:
      simpleCB:
        maxRequests: 1
        timeout: 30s 
        trip: consecutiveFailures >= 5
  targets:
    apps:
      appB:
        timeout: general
        retry: important
        circuitBreaker: simpleCB
    actors:
      myActorType:
        timeout: general
        retry: important
        circuitBreaker: simpleCB
        circuitBreakerScope: both
        circuitBreakerCacheSize: 5000
    components:
      statestore1:
        outbound:
          timeout: general
          retry: retryForever
          circuitBreaker: simpleCB
```

Scoping rules visible in the example: app circuit breakers are per app instance and a tripped route leaves load balancing for the breaker `timeout`; actor breakers are scoped by type, id or both and remove the type or id from the placement table; component breakers block all interaction with that component. Component targets have `outbound` and (pub/sub delivery to the app) `inbound` sections. Breaker counters live in the sidecar and are not persisted.

Limitation: resiliency policies are not supported for service invocation via gRPC.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
