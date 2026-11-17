---
id: computing-software.messaging-and-integration.dapr.resiliency-override-built-in-retries
name: resiliency-override-built-in-retries
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, built-in-retries, daprbuiltinserviceretries, actor-reminders, initialization-retries, override]
level: advanced
status: docs-checked
description: "Override Dapr built-in retries with reserved names such as DaprBuiltInServiceRetries: the four defaults (service, actor, reminder, init) and no weakening them."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/policies/retries/override-default-retries.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dapr retries some failures even with no Resiliency spec. You can replace these with reserved policy names inside `spec.policies.retries`.

| Capability | Override keyword | Default |
|---|---|---|
| Service invocation | `DaprBuiltInServiceRetries` | 1 second backoff, up to 3 times per call |
| Actors | `DaprBuiltInActorRetries` | 1 second backoff, up to 3 times per call |
| Actor reminders | `DaprBuiltInActorReminderRetries` | exponential, initial 500ms, up to 60s, for 15 minutes |
| Initialization | `DaprBuiltInInitializationRetries` | 3 times, exponential, initial 500ms, for 10s |

The service and actor defaults cover sidecar-to-sidecar calls that fail with gRPC code Unavailable or Unauthenticated; reminders cover requests that fail to persist an actor reminder to a state store; initialization covers failures requesting a spec from an application (for example a subscription, component or resiliency spec).

Rule: you may make them more robust, but you cannot set values lower than the defaults or remove default retries entirely, which protects against unexpected downtime.

```yaml
spec:
  policies:
    retries:
      DaprBuiltInServiceRetries: # Overrides default retry behavior for service-to-service calls
        policy: constant
        duration: 5s
        maxRetries: 10
      retryForever: # A user defined retry policy replaces default retries. Targets rely solely on the applied policy. 
        policy: exponential
        maxInterval: 15s
        maxRetries: -1 # Retry indefinitely
  targets:
    apps:
      appB: # app-id of the target service
        retry: retryForever
```

Here all service invocation uses the overridden constant policy, except calls to appB, which rely solely on `retryForever`.

## Checked

2026-11-04. Default retry table, override keywords and example YAML confirmed on the Override default retry resiliency policies page.

Method: documentation only; no commands were run.
