---
id: computing-software.messaging-and-integration.apache-camel.jms-component
name: jms-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, jms, queue, request-reply, transactions]
level: practitioner
status: docs-checked
description: "Camel jms component: queue and topic URIs, connection pooling, consumer and producer defaults, transacted options and request-reply with temporary or shared reply queues."
sources:
  - https://camel.apache.org/components/next/jms-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jms:

`jms:[queue:|topic:]destinationName[?options]`. No prefix means queue; topics need `topic:`.

Connection: `connectionFactory` has no default; wrap the broker factory in a pool or Camel opens a connection per message. `allowAutoWiredConnectionFactory` true uses a single factory found in the registry.

Consumer (defaults): `concurrentConsumers` 1, `maxConcurrentConsumers` unset, `acknowledgementModeName` AUTO_ACKNOWLEDGE, `cacheLevelName` CACHE_AUTO (CACHE_CONSUMER non-transacted, CACHE_NONE transacted; no caching for XA), `selector`, `asyncConsumer` false, `receiveTimeout` 1000 ms.

Producer: `deliveryPersistent` true, `timeToLive` -1, `explicitQosEnabled` false (endpoint QoS only, ignores headers), `priority` 4 (needs explicit QoS), `preserveMessageQos` false (JMSPriority, JMSDeliveryMode, JMSExpiration headers win), `disableReplyTo` false.

Transactions: `transacted` false, `transactedInOut` false, `lazyCreateTransactionManager` true (builds a `JmsTransactionManager`), `transactionTimeout` -1.

Request-reply (InOut): Camel creates a temporary reply queue and sets `JMSReplyTo`. `replyTo` fixes a queue; then `replyToType` defaults to Shared (slower than Temporary or Exclusive). `requestTimeout` 20000 ms (header `CamelJmsRequestTimeout` overrides), `requestTimeoutCheckerInterval` 1000.

Durable topics need `durableSubscriptionName` (JMS 1.1 also a unique `clientId`). Use the activemq component for ActiveMQ Classic; this one for Artemis. From Camel 4.9 `JmsHeaderFilterStrategy` removes `Camel...` headers.

Verify: an InOut send returns the consumer route's final body within 20 seconds.

## Checked

Method: docs-checked 2026-11-09 against the camel.apache.org jms-component page (connection, URI, cache level, durable subscription and header mapping sections plus the option tables via grep and targeted reads).
