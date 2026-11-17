---
id: computing-software.cloud-infrastructure-engineering.aws.sns-fifo-topics-ordering
name: sns-fifo-topics-ordering
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, sns-fifo, fifo-topic, fifo-queue, message-group-id, deduplication, ordered-fan-out, sqs-fifo, exactly-once, content-based-deduplication, fifo-throughput, messaging]
level: practitioner
status: docs-checked
description: "Fan out ordered, deduplicated events with SNS FIFO topics to SQS FIFO queues: group IDs, dedup IDs, throughput limits, the FIFO-only subscriber rule and Lambda/HTTP workarounds."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html", "https://docs.aws.amazon.com/sns/latest/dg/fifo-message-dedup.html", "https://docs.aws.amazon.com/sns/latest/dg/fifo-high-throughput.html", "https://docs.aws.amazon.com/sns/latest/dg/large-message-payloads.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS FIFO topics: ordered fan-out

**Goal:** several consumers each receive the same stream of events in the same order per
entity, exactly once per subscriber, with one publish.

## 1. Create and subscribe
```bash
aws sns create-topic --name order-events.fifo --attributes '{"FifoTopic":"true","ContentBasedDeduplication":"false"}'
aws sqs create-queue --queue-name billing.fifo --attributes '{"FifoQueue":"true"}'
aws sns subscribe --topic-arn "$TOPIC" --protocol sqs --notification-endpoint "$BILLING_ARN" --attributes '{"RawMessageDelivery":"true"}'
aws sns publish --topic-arn "$TOPIC" --message '{"orderId":"42","event":"paid"}' \
  --message-group-id order-42 --message-deduplication-id order-42-paid-v1
```
FIFO topics deliver to **SQS FIFO queues** (strict ordering and deduplication) and to **SQS standard
queues** (best-effort ordering, at-least-once, cheaper). They cannot deliver to customer managed endpoints:
email, mobile push, SMS and HTTP(S) subscriptions are rejected with an error. For Lambda, subscribe an SQS
queue to the topic and have the queue trigger the function.

## 2. Ordering model
- Order is preserved **within a message group**; SNS delivers the group's messages to each
  subscribed queue in publish order. Different groups are independent.
- The deduplication ID you publish is included in the message delivered to subscribed FIFO queues.
- FIFO topics support the same message filtering capabilities as standard topics. With a filter policy,
  FIFO topics give at-most-once delivery (messages can be filtered out), so the exactly-once guarantee below
  only holds on subscriptions without filtering.
- Ordering across publisher and topic is only as good as the publisher: a producer with several threads
  publishing the same group concurrently has already lost order. Use one publisher thread per group or
  sequence numbers in the body.

## 3. Deduplication
- A deduplication ID is required on publish (explicit `MessageDeduplicationId`, or `ContentBasedDeduplication=true`,
  which hashes the message body only: message attributes are not included). A published ID overrides the generated one.
- A message with the same deduplication ID published within the five-minute interval is **accepted but not
  delivered**; the topic keeps tracking the ID after delivery. The dedup scope is the whole topic when
  `FifoThroughputScope` is `Topic` (default) and each message group when it is `MessageGroup`.
- Exactly-once delivery and processing holds only if: the subscribed SQS FIFO queue exists and allows the SNS
  service principal; the consumer deletes the message before the visibility timeout expires; the subscription
  has no message filtering; and there are no network disruptions that prevent delivery acknowledgement.
- Publisher retries with the same dedup ID are therefore safe.

## 4. Throughput
By default a FIFO topic has `FifoThroughputScope=Topic` (topic-level dedup; maximum 3,000 messages per second
or 20 MB per second, whichever comes first, per the SetTopicAttributes reference). Setting `FifoThroughputScope` to
`MessageGroup` enables high throughput, can be done at topic creation (recommended by AWS), and **cannot be
reverted**. Throughput grows with the number of message groups, so use group IDs with many distinct values.
Enable high-throughput mode on subscribed SQS FIFO queues too so delivery keeps up.

## 5. Encryption and policy
FIFO topics support SSE with KMS keys and private access through VPC endpoints (AWS PrivateLink). If a
subscribed SQS queue is encrypted with a customer managed key, its key policy must allow `sns.amazonaws.com`
to use `kms:Decrypt` and `kms:GenerateDataKey` (see the SQS key-management guide). Delivery status
logging is covered in the `sns-delivery-policies-retries-and-status-logging` skill.

## Gotchas
- Customer managed endpoints (email, SMS, mobile push, HTTP/S) cannot subscribe to a FIFO topic.
- Cross-account subscriptions need the queue policy to allow the topic's `sns.amazonaws.com` principal, as for standard topics.
- SNS Extended Client Libraries for Java and Python (payloads up to 2 GB) work with Standard and FIFO topics;
  set an explicit dedup ID because a content-based hash would cover only the small S3 reference.

## Verify
- [ ] Publish 1,000 messages for group `order-1` from a single thread; both subscribed FIFO queues receive them in sequence (compare `SequenceNumber`s or a counter in the body).
- [ ] A repeated publish with the same dedup ID within 5 minutes is not delivered to any queue.
- [ ] Subscribing an HTTP endpoint or email address to the FIFO topic fails; a standard SQS queue subscribes but gets only best-effort ordering.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (FIFO topics pages).
Confirmed: FIFO topics deliver to SQS FIFO and standard queues but not to email, SMS, mobile push or HTTP(S); Lambda via a queue; filtering support and the at-most-once caveat; 5-minute dedup, accepted-but-not-delivered behaviour, content-based hash covers body only; `FifoThroughputScope` values `Topic` and `MessageGroup`, irreversible, recommended on subscribed queues; exactly-once conditions; SSE and PrivateLink support; SNS Extended Client for Standard and FIFO.
Corrected: the old text said standard queues could not subscribe ("in newer releases" hedge), the `MessageGroupId` pass-through, a 300 msg/s or 10 MB/s figure and a returned `SequenceNumber` claim could not be confirmed and were removed along with the draft's stray self-corrections (`wait`, `?`), the quoted error string, EventBridge remark and 256 KB size remark.
Throughput figure for `Topic` scope added from https://docs.aws.amazon.com/sns/latest/api/API_SetTopicAttributes.html.
Sources: https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html ; https://docs.aws.amazon.com/sns/latest/dg/fifo-message-dedup.html ; https://docs.aws.amazon.com/sns/latest/dg/fifo-high-throughput.html ; https://docs.aws.amazon.com/sns/latest/dg/large-message-payloads.html

Method: documentation only; no commands were run.
