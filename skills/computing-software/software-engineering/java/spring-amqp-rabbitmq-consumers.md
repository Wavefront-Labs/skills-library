---
id: computing-software.software-engineering.java.spring-amqp-rabbitmq-consumers
name: spring-amqp-rabbitmq-consumers
category: computing-software
field: software-engineering
product: java
tags: [java, spring-messaging, spring-amqp, rabbitmq, rabbitlistener, dead-letter-exchange, publisher-confirms]
level: advanced
status: docs-checked
description: "Use Spring AMQP with RabbitMQ: listener container ack and requeue settings, dead-letter exchanges, publisher confirms, prefetch and idempotent handlers."
sources: ["https://github.com/spring-projects/spring-amqp/tree/main/src/reference/antora/modules/ROOT/pages/amqp", "https://www.rabbitmq.com/docs/reliability", "https://www.rabbitmq.com/docs/dlx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring AMQP with RabbitMQ

## Listener container behaviour
- `acknowledgeMode` `AUTO`: the container acknowledges the message automatically unless the listener throws an exception.
- `defaultRequeueRejected` (property `requeue-rejected`) decides whether a message rejected because the listener threw is requeued. The default is `true`, which redelivers a message that always fails over and over. Set it to `false` and the message is discarded or routed to a dead letter exchange.
- A listener can throw `AmqpRejectAndDontRequeueException` (do not requeue) or `ImmediateRequeueAmqpException` (requeue) to control this per message. The `ConditionalRejectingErrorHandler` throws `AmqpRejectAndDontRequeueException` when the fatal exception strategy says the failure is fatal.
- `prefetchCount` (`prefetch`) is ignored when `acknowledgeMode` is `NONE`. The docs say there are cases for setting it back to 1, and that with low-volume messaging and several consumers you may reduce it to spread messages more evenly.

## Dead-letter exchanges (RabbitMQ)
A queue's messages are dead-lettered (republished to an exchange) when a consumer uses `basic.reject` or `basic.nack` with `requeue=false`, when the message expires from per-message TTL, when the queue exceeds a length limit, or when a quorum queue's delivery-limit is exceeded. Configure with a policy (`dead-letter-exchange`, `dead-letter-routing-key`) or queue arguments (`x-dead-letter-exchange`, `x-dead-letter-routing-key`). DLXs are ordinary exchanges. A dead-letter cycle through a TTL queue is a common retry pattern, but the RabbitMQ docs recommend the delayed retry that quorum queues support natively, which avoids the risk of message loss from at-most-once dead-lettering.

## Publisher confirms
`RabbitTemplate` needs a `CachingConnectionFactory` whose `publisherConfirm` property is `ConfirmType.CORRELATED`; confirms arrive through a callback with the `CorrelationData`. Publisher returns report messages that could not be routed to any queue. Spring AMQP keeps a channel open while confirms are outstanding (up to five seconds deferral when the channel cache is full).

## Reliability rules (RabbitMQ)
- Use durable queues (or a replicated queue type) for important data, and publish messages as persistent.
- Consumer acknowledgements and publisher confirms are the delivery guarantee mechanisms; when a producer recovers from a connection failure it may send duplicates, so deduplicate or handle messages idempotently.
- A redelivered message has the `redelivered` flag set; if the flag is not set the message has definitely not been seen before, so deduplication can be limited to flagged messages.

## Verify
Publish a poison message and assert it lands on the dead-letter queue and does not loop.

## Checked
Read the RabbitMQ reliability and dead letter exchange pages and the Spring AMQP exception-handling, container-attributes (acknowledgeMode, defaultRequeueRejected, prefetchCount rows) and template (confirms) pages from the docs source on GitHub; docs.spring.io/spring-amqp/reference is an index only. Removed as unconfirmed: the Java configuration snippet and Boot YAML properties, Jackson2JsonMessageConverter advice, concurrency range syntax, retry settings, the delivery mode 2 default claim, quorum queue 3.8 claim, channel thread-safety note and Testcontainers advice.
Method: docs-checked 2026-11-09 against the Spring AMQP exception handling, container attribute and template pages and the RabbitMQ reliability and DLX guides.
