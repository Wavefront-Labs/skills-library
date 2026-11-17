---
id: computing-software.messaging-and-integration.apache-camel.oncompletion
name: oncompletion
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, oncompletion, unit-of-work, callbacks, eip]
level: practitioner
status: docs-checked
description: "Camel onCompletion: post-exchange callbacks with onCompleteOnly, onFailureOnly, onWhen, consumer mode, route vs context scope."
sources:
  - https://camel.apache.org/manual/oncompletion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# onCompletion

Runs callbacks when an Exchange finishes, built on the Unit of Work (`Synchronization`, `SynchronizationRouteAware`).

Options:
- **Trigger**: always by default; `onCompleteOnly()` for success only; `onFailureOnly()` for exception or FAULT body.
- **onWhen**: predicate that must match first.
- **mode**: `AfterConsumer` (default) or `BeforeConsumer` (`modeBeforeConsumer()`), which runs before the consumer writes its response so it can still add headers.
- **parallelProcessing**: default `false`; `true` uses a thread pool, `executorService` names a pool.
- **Scope**: context (global) or route. Route scope overrides all global blocks for that route.

Route-scoped blocks run on a copy of the Exchange in another thread, like a Wire Tap, so the route continues concurrently. Camel sets `Exchange.ON_COMPLETION` to `true` on those exchanges.

Java: `onCompletion().onFailureOnly().onWhen(body().contains("x")).to("direct:alert").end()`. XML uses `<onCompletion onFailureOnly="true" mode="..."/>` with an `<onWhen>` child. In YAML, route-scoped onCompletion goes in a `routeConfiguration` referenced via `routeConfigurationId`.

Verify: an `onFailureOnly` block fires only for exchanges that threw, and not for successes.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel onCompletion manual page. Confirmed: Unit of Work Synchronization and SynchronizationRouteAware, scope, trigger, onWhen, mode and parallelProcessing options with defaults, route scope overriding global, copy of the Exchange routed in another thread like a Wire Tap, Exchange.ON_COMPLETION, onCompleteOnly and onFailureOnly (exception or FAULT body), executorService, the XML attributes and the YAML routeConfiguration form. The one-line Java example combines pieces shown separately on the page.
