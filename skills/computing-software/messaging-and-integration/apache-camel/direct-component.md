---
id: computing-software.messaging-and-integration.apache-camel.direct-component
name: direct-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, direct, synchronous, in-vm]
level: intro
status: docs-checked
description: "Camel direct component: synchronous in-context invocation, block true and timeout 30000 defaults, failIfNoConsumers true and when to prefer seda instead."
sources:
  - https://camel.apache.org/components/next/direct-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# direct:

`direct:someId[?options]` gives direct, synchronous invocation of consumers in the same CamelContext. For asynchronous use SEDA.

Producer options (defaults):
- `block` true: wait for a consumer to become active if none is
- `timeout` 30000 ms, used when `block` is on
- `failIfNoConsumers` true: throw if there is no active consumer
- `lazyStartProducer` false
- `synchronous` false

Component level: `block` true, `timeout` 30000, `lazyStartProducer` false, `bridgeErrorHandler` false, `autowiredEnabled` true.

Body: the consumer sees what the caller sent; the producer gets whatever body the called route ends with.

Example: a route consumes `activemq:queue:order.in`, validates with a bean and forwards to `direct:processOrder`; a second route consumes `direct:processOrder`, processes and sends to `activemq:queue:order.out`.

Verify: sending to `direct:x` with no route consuming it blocks for up to `timeout` (30000 ms by default) waiting for a consumer; `failIfNoConsumers` (default true) controls whether the producer then throws.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel direct component page: the block, timeout, failIfNoConsumers, lazyStartProducer, synchronous, bridgeErrorHandler and autowiredEnabled defaults, the component-level option list, the body table and the order-processing example all match. The old verify line claimed the failure outcome after the wait; it was reworded to the option semantics the page states. No commands were run.
