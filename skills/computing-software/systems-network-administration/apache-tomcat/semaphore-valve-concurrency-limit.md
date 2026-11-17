---
id: computing-software.systems-network-administration.apache-tomcat.semaphore-valve-concurrency-limit
name: semaphore-valve-concurrency-limit
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, semaphorevalve, concurrency, concurrency-limit, throttling, highconcurrencystatus]
level: practitioner
status: docs-checked
description: "Cap concurrent requests in Tomcat 10.1 with SemaphoreValve: concurrency, block, fairness, interruptible and highConcurrencyStatus."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SemaphoreValve

Class `org.apache.catalina.valves.SemaphoreValve`. Limits the number of concurrent request processing threads.

| Attribute | Default | Meaning |
|---|---|---|
| `concurrency` | 10 | Permits |
| `block` | true | Whether a thread is blocked until a permit is available |
| `fairness` | false | Fairness of the semaphore |
| `interruptible` | false | Whether a thread may be interrupted until a permit is available |
| `highConcurrencyStatus` | -1 | HTTP status returned when a permit cannot be acquired; -1 sends no error status |

```xml
<Context>
  <Valve className="org.apache.catalina.valves.SemaphoreValve"
         concurrency="20" block="false" highConcurrencyStatus="503"/>
</Context>
```

Subclasses of `org.apache.catalina.valves.SemaphoreValve` can override `controlConcurrency` (add conditions) and `permitDenied` (error handling when a permit is not granted).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Valve reference (Semaphore Valve): attributes, defaults, overridable methods. Removed unsupported design advice (thread occupation, placement) and the generic verify line.

Method: documentation only; no commands were run.
