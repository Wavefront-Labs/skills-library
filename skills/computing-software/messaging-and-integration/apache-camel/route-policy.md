---
id: computing-software.messaging-and-integration.apache-camel.route-policy
name: route-policy
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, route-policy, throttling, circuit-breaker, clustering]
level: advanced
status: docs-checked
description: "Camel RoutePolicy: callbacks, ThrottlingInflightRoutePolicy defaults (1000 in flight, resume at 70 percent), exception and clustered policies, and applying policies or factories."
sources:
  - https://camel.apache.org/manual/route-policy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RoutePolicy

`org.apache.camel.spi.RoutePolicy` controls routes at runtime. Extend `RoutePolicySupport`. Callbacks: onInit, onRemove, onStart, onStop, onSuspend, onResume, onExchangeBegin, onExchangeDone.

Built in:
- **ThrottlingInflightRoutePolicy**: suspends and resumes a route by in-flight count. Options: `scope` `Route` (default) or `Context`; `maxInflightExchanges` 1000; `resumePercentOfMax` 70; `loggingLevel` INFO. Approximate and non-blocking, unlike the precise Throttler EIP.
- **ThrottlingExceptionRoutePolicy**: circuit-breaker style; stops consuming when configured exceptions pass a threshold (matched like onException/doCatch).
- **ClusteredRoutePolicy**: basis of `camel-cluster`; route is active only on the leader node.
- **ScheduledRoutePolicy** (Quartz component): start, stop, suspend, resume at set times.

For fine dynamic suspend/resume use `SuspendableService`.

Apply to a route: `.routePolicy(a, b)` in Java, `routePolicyRef="a,b"` in XML and YAML.

`RoutePolicyFactory` creates one policy per route: `context.addRoutePolicyFactory(...)`, `@Component` on Spring Boot, `@ApplicationScoped` on Quarkus, or a bean in XML/YAML.

Verify: a consumer under ThrottlingInflightRoutePolicy is suspended when the in-flight count is higher than `maxInflightExchanges` and resumes per `resumePercentOfMax` (70 by default); the policy is triggered when an exchange completes, so at least one exchange must complete before it acts.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel RoutePolicy manual page: the eight callbacks, RoutePolicySupport, the four built-in policies, ThrottlingInflightRoutePolicy options and defaults (scope Route, maxInflightExchanges 1000, resumePercentOfMax 70, loggingLevel INFO), the comparison with the Throttler EIP, SuspendableService advice, routePolicy and routePolicyRef syntax and RoutePolicyFactory registration match. The verify line was tightened to the page's wording. No commands were run.
