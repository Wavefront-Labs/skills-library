---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-idempotent-consumers-and-duplicate-handling
name: sqs-idempotent-consumers-and-duplicate-handling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, idempotent-consumer, idempotency, at-least-once, duplicate-messages, powertools-idempotency, partial-batch-response]
level: practitioner
status: docs-checked
description: "Make SQS consumers safe under at-least-once delivery: idempotency keys, DynamoDB conditional writes, Powertools idempotency, partial batch failures and FIFO dedup limits."
sources: ["https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html", "https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent SQS consumers

**Goal:** processing the same message twice has the same effect as processing it once,
because standard queues deliver at least once and every queue can redeliver after a timeout.

## Where duplicates come from
- Standard queues: SQS stores copies on multiple servers; on rare occasions a copy is not deleted and you may receive it again.
- Any queue: consumer crashes or exceeds the visibility timeout before `DeleteMessage`.
- Producers retrying `SendMessage` after a network timeout (the first send may have succeeded).
- FIFO dedup protects only producer retries within a 5-minute window, not consumer-side redelivery (a message that is in flight and not deleted before its visibility timeout is delivered again).

## Choose the idempotency key
- Prefer a business key from the payload (order id + event type); it also catches producer
  duplicates with different `MessageId`s.
- `MessageId` catches only redelivery of the same SQS message.

## DynamoDB conditional write pattern
```python
table.put_item(
    Item={"pk": f"msg#{key}", "status": "IN_PROGRESS", "ttl": now + 86400},
    ConditionExpression="attribute_not_exists(pk)")
# ConditionalCheckFailedException -> already seen: look up status, delete message, return
do_side_effect()
table.update_item(Key={"pk": f"msg#{key}"}, UpdateExpression="SET #s = :d",
                  ExpressionAttributeNames={"#s": "status"}, ExpressionAttributeValues={":d": "DONE"})
```
- Record `IN_PROGRESS` with an expiry shorter than the visibility timeout so a crashed attempt can be retried.
- Where possible make the side effect itself idempotent (upsert, `PUT` with a client token, a
  unique constraint) and skip the ledger.

## Powertools for Lambda
```python
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer, IdempotencyConfig, idempotent_function)
layer = DynamoDBPersistenceLayer(table_name="idempotency")
cfg = IdempotencyConfig(event_key_jmespath="order_id", expires_after_seconds=3600)
@idempotent_function(data_keyword_argument="record", persistence_store=layer, config=cfg)
def process(record: dict): ...

def handler(event, context):
    cfg.register_lambda_context(context)   # required with idempotent_function, protects against timeouts
    process(record=event)                  # must be called with the keyword argument
```
Defaults: `expires_after_seconds` 3600, `use_local_cache` False; the DynamoDB table needs partition key `id` and
TTL attribute `expiration`; the role needs `dynamodb:GetItem`, `PutItem`, `UpdateItem` and `DeleteItem`.
The Powertools docs show the SQS batch processor with `idempotent_function`, using `event_key_jmespath="messageId"`.
Combine with the batch processor and partial batch responses so one bad record does not
replay the whole batch: enable `ReportBatchItemFailures` in the event source mapping's
`FunctionResponseTypes`, e.g. `aws lambda update-event-source-mapping --uuid <UUID> --function-response-types "ReportBatchItemFailures"`.
Return `{"batchItemFailures": [{"itemIdentifier": messageId}]}` for failed records only.

## Gotchas
- Ledger TTL must exceed the longest realistic redelivery window (queue retention plus any DLQ redrive), or a
  redriven message is processed again; keep keys at least for the queue retention period.
- Ordering of check and side effect matters: write the ledger first, or two concurrent consumers both pass.
- Non-idempotent external calls (payments, emails) need the provider's idempotency key header too.
- Returning an empty or null `batchItemFailures` list is a complete success (the batch is deleted); an exception, invalid response or unknown `itemIdentifier` makes the whole batch fail and return to the queue.

## Verify
- [ ] Test: send the same payload twice (different MessageIds), side effect happens once.
- [ ] Test: kill the consumer mid-processing; after visibility timeout the message completes once.
- [ ] Ledger table has TTL enabled and is sized for peak message rate.

## Checked

Date 2026-10-23. Documentation release: Powertools for AWS Lambda (Python) idempotency docs, Amazon SQS Developer Guide, Lambda Developer Guide.
Confirmed: at-least-once delivery wording; Powertools imports, `idempotent_function` keyword-argument rule, `register_lambda_context`, `IdempotencyConfig` defaults, DynamoDB key and TTL attribute names, IAM actions, SQS batch processor example; `ReportBatchItemFailures` and `batchItemFailures` success and failure conditions. The DynamoDB conditional-write example uses standard `ConditionExpression` syntax and a self-chosen `ttl` attribute, so the TTL attribute name must match your table setting.
The four non-URL `sources` entries were replaced by the pages above.
Sources: https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/ ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html ; https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html

Method: documentation only; no commands were run.
