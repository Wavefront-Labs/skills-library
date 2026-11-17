---
id: computing-software.messaging-and-integration.apache-camel.failover-load-balancer
name: failover-load-balancer
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, load-balancer, failover, round-robin, sticky]
level: practitioner
status: docs-checked
description: "Camel Failover Load Balancer: exception filter, roundRobin and sticky modes, maximumFailoverAttempts (-1 unlimited) and inheritErrorHandler default true."
sources:
  - https://camel.apache.org/components/next/eips/failoverLoadBalancer-eip.html
  - https://camel.apache.org/components/next/eips/loadBalance-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failover load balancer

Policies under `loadBalance`: custom, failover, round robin, random, sticky (correlation key from an Expression), topic (all destinations), weighted.

Failover options (defaults):
- `exception`: classes to monitor; none listed means any exception fails over.
- `roundRobin` false: true keeps state and moves to the next endpoint per message; false starts at the first each time.
- `sticky` false: starts from the last endpoint that succeeded.
- `maximumFailoverAttempts` -1: unlimited; 0 disables failover; positive caps it.
- `inheritErrorHandler` true: set false to fail over immediately rather than after the Camel error handler exhausts retries.

No exchange properties.

Java:
```java
failover(10, false, true)        // max attempts, inheritErrorHandler, roundRobin
failover(10, false, true, true)  // adds sticky
failover(IOException.class, HttpOperationFailedException.class)
```
XML/YAML: `roundRobin="true"`, `maximumFailoverAttempts="10"`, `inheritErrorHandler="false"`, `sticky="true"`. Always set a maximum with round robin to prevent endless retries.

Matching uses the same rules as `onException` and `doCatch`, checks causes, and ignores suppressed exceptions (one thrown in `doFinally` won't trigger failover).

Example: `http:service1`, `service2`, `service3` tried in order; if all fail the exchange fails. With sticky, if service1 is down and service2 up, calls start at service2 until it fails.

Verify: with service1 down, requests are served by service2 and the exchange succeeds.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Failover Load Balancer and Load Balance EIP pages: the seven built-in policies, option defaults (roundRobin false, sticky false, maximumFailoverAttempts -1, inheritErrorHandler true), the meaning of the failover(10, false, true) and four-argument arguments, XML attribute names, exception matching including causes and suppressed exceptions, and the sticky example match. No commands were run.
