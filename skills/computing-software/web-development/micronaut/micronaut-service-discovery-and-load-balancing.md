---
id: computing-software.web-development.micronaut.micronaut-service-discovery-and-load-balancing
name: micronaut-service-discovery-and-load-balancing
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, service-discovery, load-balancing, outlier-detection, http-services, load-balancer-strategy, client]
level: advanced
status: docs-checked
description: "Configure Micronaut services manually with micronaut.http.services, add health checks and outlier detection, and pick or write a client-side load balancer strategy."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cloud/serviceDiscovery/serviceDiscoveryManual.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cloud/clientSideLoadBalancing.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual service discovery and client-side load balancing

Goal: call a service by id across several instances without a discovery server, with health checking and a chosen balancing strategy.

## Declare the service

```yaml
micronaut:
  http:
    services:
      foo:
        urls:
          - http://foo1
          - http://foo2
```

Inject a client with `@Client("foo")`. The id in `@Client` must be kebab-case; the configuration key may be camel case. Override in production with an environment variable such as `MICRONAUT_HTTP_SERVICES_FOO_URLS=http://prod1,http://prod2`.

## Health checks (off by default)

```yaml
micronaut:
  http:
    services:
      foo:
        health-check: true
        health-check-interval: 15s
        health-check-uri: /health      # default path
```

A background thread checks; services responding with an error code are removed from the available list.

## Outlier detection

Clients report every exchange outcome to the load balancer, so a failing instance is skipped without waiting for the next health check:

```yaml
        outlier-detection:
          enabled: true
          consecutive-failures: 5
          base-ejection-time: 30s
          max-ejection-time: 5m
          max-ejection-percent: 50
```

- `consecutive-failures` transport failures in a row (connection cannot be opened, response times out, reset before the response completes) eject the instance for `base-ejection-time` times the number of ejections, up to `max-ejection-time`. A success resets the count.
- `consecutive-server-errors` (off by default) also counts responses with status 500 or above.
- At most `max-ejection-percent` of instances are ejected; if all are ejected, selection behaves as if none were.

## Strategy

Default is round robin over `DiscoveryClientRoundRobinLoadBalancer`. Choose another per service (works for static URLs and discovery clients):

```yaml
        load-balancer-strategy: p2c
```

| Name | Selection |
|---|---|
| `round-robin` | each in turn (default) |
| `random` | random instance |
| `p2c` | of two random instances, the one with fewer exchanges in flight |
| `weighted` | smooth weighted round robin by instance `weight` metadata; missing/invalid weight = 1; weight 0 only chosen if all are 0 |
| `sticky` | same instance for the same key (rendezvous hashing); no key = round robin |

Sticky key: request attribute set with `LoadBalancerKey.set(request, key)` (attribute takes precedence), or a header named by `load-balancer-key-header: X-Session-Id`. Use a stable key (String or Long). Instances with `backup` metadata `true` are used only when none else is available, but only if a strategy is configured. Ejected instances are never selected by any strategy.

## Custom strategy

```java
@Prototype            // each service gets its own instance
@Named("primary")     // name = value of load-balancer-strategy
public class PrimaryStrategy implements LoadBalancerStrategy {
    // select(...) picks among the available instances (here: the first);
    // the default report method receives the outcome of each exchange
}
```

Then set `load-balancer-strategy: primary`. A bean beats a built-in of the same name. Strategies apply to the framework's round-robin load balancers; a custom `LoadBalancer` controls its own selection (replace `DiscoveryClientLoadBalancerFactory` to supply one).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against both cited pages: the services YAML, kebab-case rule, environment override, health-check keys, outlier-detection keys and semantics, strategy table, sticky key and header rules, backup metadata, ejection rule and bean naming. Removed: the `select(List, Object)` method signature and body, which the page only embeds from an unread source file.
