---
id: computing-software.messaging-and-integration.apache-camel.dead-letter-channel
name: dead-letter-channel
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, error-handling, dead-letter-channel, redelivery, delay-pattern]
level: advanced
status: docs-checked
description: "Camel Dead Letter Channel details: redelivery defaults, delayPattern, useOriginalMessage, onRedelivery and onPrepare processors, redelivery headers and failure properties."
sources:
  - https://camel.apache.org/components/next/eips/dead-letter-channel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead Letter Channel

An error handler that moves failed messages to a dead letter endpoint (any component). Unlike the default handler it handles exceptions by default and is the only one with a dedicated dead letter queue.

Java: `errorHandler(deadLetterChannel("log:dead?level=ERROR"))`. XML: `type="DeadLetterChannel"` with `deadLetterUri`, referenced by `errorHandlerRef`.

Defaults: `maximumRedeliveries` 0 (negative = unlimited), `redeliveryDelay` 1000 ms, `maximumRedeliveryDelay` 60000 ms, no exponential backoff, `retriesExhaustedLogLevel` ERROR, `retryAttemptedLogLevel` DEBUG, `allowRedeliveryWhileStopping` true, `logExhaustedMessageHistory` false.

After failure the caught exception is cleared and kept in `Exchange.EXCEPTION_CAUGHT`; the client sees no failure. If sending to the dead letter queue itself fails, `deadLetterHandleNewException` (default true) logs at WARN and completes; false propagates it.

Original message: `useOriginalMessage(true)` sends original body and headers; `useOriginalBody` keeps only the original body. Bounded by the unit of work (JMS/HTTP start a new one); Splitter and multicast can use `shareUnitOfWork`.

Processors: `onRedelivery` before each attempt, `onExceptionOccurred` right after a throw, `onPrepare` to modify the exchange before the dead letter queue.

`delayPattern=5:1000;10:5000;20:20000` gives 0 ms for attempts 1-4, 1000 for 5-9, 5000 for 10-19, 20000 from 20; it overrides delay and backoff settings.

Headers: `Exchange.REDELIVERED`, `REDELIVERY_COUNTER`, `REDELIVERY_MAX_COUNTER`. Failure context: `CamelFailureEndpoint`, `CamelFailureRouteId`, `CamelFailureNodeId`.

Verify: after retries are exhausted the dead letter endpoint receives the message and the caller sees success.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Dead Letter Channel page: redelivery defaults (maximumRedeliveries 0, redeliveryDelay 1000, maximumRedeliveryDelay 60 seconds, backoff off, ERROR and DEBUG log levels, allowRedeliveryWhileStopping true, logExhaustedMessageHistory false), deadLetterHandleNewException behaviour, EXCEPTION_CAUGHT, useOriginalMessage and useOriginalBody, unit of work boundary and shareUnitOfWork, onRedelivery, onExceptionOccurred, onPrepare(Failure), delayPattern arithmetic, redelivery headers and failure properties all match. No commands were run.
