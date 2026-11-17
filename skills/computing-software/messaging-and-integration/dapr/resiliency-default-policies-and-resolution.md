---
id: computing-software.messaging-and-integration.dapr.resiliency-default-policies-and-resolution
name: resiliency-default-policies-and-resolution
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, default-policies, defaultretrypolicy, built-in-retries, policy-hierarchy, keywords]
level: advanced
status: docs-checked
description: "Use reserved Default*Policy names in a Resiliency spec to cover all apps, actors or components, build names from keywords like App, and how resolution order works."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/policies/default-policies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reserved policy names apply broadly without a target entry. Three base names: `DefaultRetryPolicy`, `DefaultTimeoutPolicy`, `DefaultCircuitBreakerPolicy`. Insert a keyword after `Default` to narrow them; the pattern is `Default<Keyword><Type>Policy`, for example:

- `App` (service invocation): `DefaultAppRetryPolicy`
- `Actor`: `DefaultActorTimeoutPolicy`
- `Component` (all component operations): `DefaultComponentCircuitBreakerPolicy`
- `ComponentInbound` / `ComponentOutbound`
- `StatestoreComponentOutbound`, `PubsubComponentOutbound`, `PubsubComponentInbound`, `BindingComponentOutbound`, `BindingComponentInbound`, `SecretstoreComponentOutbound`, `ConfigurationComponentOutbound`, `LockComponentOutbound`

Resolution: a default applies only if the operation matches and no more specific policy targets it. A named policy in a target always wins. Apps: named in app target, then Default App policies / built-in service retries, then Default policies. Actors: same with actor policies and built-in actor retries. Components: named in component target, then component type plus direction, then direction, then component, then Default.

Built-in retries are not switched off by defaults. For service and actor invocation they handle connection problems to the remote sidecar and are only disabled when a named policy is applied to the target.

Example excerpt:

```yaml
spec:
  policies:
    retries:
      DefaultRetryPolicy:
        policy: constant
        duration: 1s
        maxRetries: 3
      DefaultAppRetryPolicy:
        policy: constant
        duration: 100ms
        maxRetries: 5
      fastRetries:
        policy: constant
        duration: 10ms
        maxRetries: 3
  targets:
    apps:
      appA:
        retry: fastRetries
```

There appA uses `fastRetries`, while an untargeted appC falls to `DefaultAppRetryPolicy`; pub/sub publish with no more specific default uses `DefaultRetryPolicy`.

## Checked

2026-11-04. Keyword table, resolution hierarchies and the worked example table confirmed on the Default resiliency policies page.

Method: documentation only; no commands were run.
