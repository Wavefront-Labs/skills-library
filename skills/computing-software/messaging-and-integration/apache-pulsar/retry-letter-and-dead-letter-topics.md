---
id: computing-software.messaging-and-integration.apache-pulsar.retry-letter-and-dead-letter-topics
name: retry-letter-and-dead-letter-topics
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [retry-letter-topic, dead-letter-topic, reconsumelater, enable-retry, dead-letter-policy, max-redeliver-count]
level: practitioner
status: docs-checked
description: "Retry failed Pulsar messages with enableRetry and reconsumeLater, bound attempts with DeadLetterPolicy maxRedeliverCount, and handle retry topic naming."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-messaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: retry failed messages with a delay and park poison messages after a bounded number of attempts.

Retry letter topic: failed messages are republished to a retry topic and consumed again later; consumers of the original topic are automatically subscribed to the retry topic. Automatic retry is off by default; enable it with `.enableRetry(true)`. It currently works with Shared subscriptions. When `maxRedeliverCount` is reached the message moves to the dead letter topic.

Java consumer:
```java
pulsarClient.newConsumer(Schema.BYTES).topic("my-topic").subscriptionName("my-subscription")
  .subscriptionType(SubscriptionType.Shared).enableRetry(true)
  .deadLetterPolicy(DeadLetterPolicy.builder().maxRedeliverCount(maxRedeliveryCount).build())
  .subscribe();
```
Schedule a retry with `consumer.reconsumeLater(msg, 3, TimeUnit.SECONDS)`; an overload accepts a custom properties map. Name the retry topic with `.retryLetterTopic("my-retry-letter-topic-name")`, and tune its producer with `.retryLetterProducerBuilderCustomizer(...)`.

Retried messages carry the properties REAL_TOPIC, ORIGIN_MESSAGE_ID, RECONSUMETIMES and DELAY_TIME.

Naming gotcha: 2.6.x and 2.7.x named the retry topic `<subscriptionname>-RETRY`. After upgrading to 2.8.x or later, delete the historical retry topics. The old format is discouraged because topics sharing a subscription name in one namespace collide and consume each other's retries.

Unlike a negative ack, whose redelivery counter is kept only in memory and can be reset unexpectedly, the retry count here is stored as a message property, so `maxRedeliverCount` is reliably honored.

Verify: call reconsumeLater until the limit and confirm the message appears in the dead letter topic.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/concepts-messaging.md (Retry letter topic and Dead letter topic sections read)
