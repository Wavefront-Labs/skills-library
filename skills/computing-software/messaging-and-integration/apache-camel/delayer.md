---
id: computing-software.messaging-and-integration.apache-camel.delayer
name: delayer
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, delay, asyncdelayed, simple-language]
level: intro
status: docs-checked
description: "Camel Delay EIP: millisecond expression, asyncDelayed and callerRunsWhenRejected defaults, dynamic delays and the end() trap."
sources:
  - https://camel.apache.org/components/next/eips/delay-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delay

Options:
- `expression` (required): delay in milliseconds, no default.
- `asyncDelayed` default `true` per the page: delays on a thread pool without blocking the caller.
- `callerRunsWhenRejected` default `true`.
- `executorService`: custom pool, used when asyncDelayed is on.
- `disabled` default `false`.

Body is unchanged; there are no exchange properties.

```java
from("seda:b").delay(1000).to("mock:result");
.delay(simple("${random(1000,5000)}"))
.delay().method("someBean", "computeDelay")
.delay(1000).asyncDelayed()
```

`${random(1000,5000)}` picks 1 to 5 seconds. A bean method can compute the value.

Java DSL trap: in loops the delay block must be closed with `end()`, otherwise later steps such as `log` run inside the block on each iteration.

Verify: a message sent to a route with `delay(1000)` reaches the mock about 1 second later.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Delay EIP page source (delay-eip.adoc) and the Delay model definition (delay.json) from the apache/camel repository, which generate the cited page. Confirmed expression in milliseconds, asyncDelayed default true, callerRunsWhenRejected default true, executorService, disabled default false, no exchange properties, unchanged body, the random and bean examples and the end() note for Java DSL blocks. Nothing was removed. No commands were run.
