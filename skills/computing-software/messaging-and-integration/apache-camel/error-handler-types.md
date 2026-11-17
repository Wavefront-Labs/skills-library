---
id: computing-software.messaging-and-integration.apache-camel.error-handler-types
name: error-handler-types
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, error-handling, dead-letter-channel, redelivery, onexception]
level: practitioner
status: docs-checked
description: "Camel error handler types (Default, Dead Letter Channel, No, Transaction), redelivery options, onException scoping and which features each handler supports."
sources:
  - https://camel.apache.org/manual/error-handler.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camel error handlers

Four handlers exist:

- **DefaultErrorHandler**: used for non-transacted routes. No dead letter queue; exceptions propagate to the caller.
- **Dead Letter Channel** (`DeadLetterChannelBuilder`): moves failed exchanges to the endpoint set with `deadLetterUri` after redelivery attempts; the error handler manual page says it redelivers at most 6 times with a 1 second delay and logs a failed exchange at ERROR, but the Dead Letter Channel EIP page lists `maximumRedeliveries` 0 as the default policy value, so set `maximumRedeliveries` and `redeliveryDelay` explicitly rather than rely on a default.
- **NoErrorHandler**: `noErrorHandler()` in Java, `type="NoErrorHandler"` in XML.
- **TransactionErrorHandler**: default for transacted routes; needs camel-spring or camel-jta.

Redelivery options: `maximumRedeliveries` (`-1` retries forever, which blocks later messages) and `redeliveryDelay` in milliseconds. Settings live in a `RedeliveryPolicy`. Headers `CamelRedeliveryCounter` and `CamelRedelivered` are set when an external system redelivers.

Per-exception rules: `onException(IOException.class).maximumRedeliveries(2).redeliveryDelay(0)`.

Scope: context-level (in Java only within the same `RouteBuilder`, via `errorHandler(...)`) or route-level (`.errorHandler(...)`, or `errorHandlerRef` in XML). Handlers are inherited unless overridden.

Feature notes: onException, onWhen, handled, continued, useOriginalBody, retryWhile and onRedelivery work on Default, Transaction and Dead Letter Channel. A dead letter queue is Dead Letter Channel only. `onPrepareFailure` is not supported by TransactionErrorHandler.

To retry a whole sub-route, give it `noErrorHandler()` and call it from a parent route through `direct:`; otherwise redelivery restarts at the failing node.

Verify: in the page's sub-route example, a processor that fails its first 2 calls under `maximumRedeliveries(2)` makes the whole sub-route run again, so `mock:b` receives the message again.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel error handler manual page and the Dead Letter Channel EIP page: the four handler types and which are used for transacted or non-transacted routes, the feature support table (including onPrepareFailure missing for TransactionErrorHandler and the dead letter queue being Dead Letter Channel only), scopes, inheritance, noErrorHandler syntax, the -1 retry-forever note, the CamelRedeliveryCounter and CamelRedelivered headers and the retry-a-sub-route pattern match. The 6-redeliveries default on the manual page contradicts the DLC page's default of 0, so the skill now says so instead of asserting either. The old verify line was replaced by the page's sub-route example. No commands were run.
