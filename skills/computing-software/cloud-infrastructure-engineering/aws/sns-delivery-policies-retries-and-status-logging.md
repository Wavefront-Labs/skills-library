---
id: computing-software.cloud-infrastructure-engineering.aws.sns-delivery-policies-retries-and-status-logging
name: sns-delivery-policies-retries-and-status-logging
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, delivery-policy, delivery-status, sns-retries, http-subscription, retry-backoff, sns-dlq, redrive-policy, delivery-status-logging, feedback-role, number-of-notifications-failed, message-delivery-retries, messaging, numberofnotificationsfailed]
level: practitioner
status: docs-checked
description: "Control how SNS retries HTTP/S endpoints (delivery policy backoff), attach a DLQ to subscriptions for undeliverable messages, and turn on delivery status logging so failures are visible."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-configure-dead-letter-queue.html", "https://docs.aws.amazon.com/sns/latest/api/API_SetTopicAttributes.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-msg-status.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SNS delivery policies, retries, DLQs and delivery status logging

**Goal:** know within a minute when a subscriber is failing, keep the messages it missed, and
tune retries so a flaky webhook neither loses events nor gets hammered.

## 1. How SNS retries (per protocol, not configurable except HTTP/S)
| Endpoint | Attempts | Window |
|---|---|---|
| SQS, Lambda (AWS managed) | 100,015: 3 immediate, 2 at 1 s, 10 exponential 1 to 20 s, then 100,000 at 20 s | 23 days |
| HTTP/S | default `numRetries` is 3; configurable 0 to 100 via a delivery policy | total policy time at most 3,600 s |
| SMTP, SMS, mobile push | 50: 2 at 10 s, 10 exponential 10 to 600 s, then 38 at 600 s | 6 hours |
Only HTTP/S supports a custom delivery policy; SNS applies jitter to retries. For throttling errors with the
Firehose protocol SNS uses the customer-managed-endpoint policy. After the policy is exhausted the message is
**discarded** unless the subscription has a redrive policy (DLQ). Retries apply to server-side errors; SNS
does not retry client-side errors.

## 2. HTTP/S delivery policy
Topic-level default (`DeliveryPolicy` attribute) or per subscription (overrides):
```json
{"healthyRetryPolicy":{"minDelayTarget":1,"maxDelayTarget":60,"numRetries":50,
   "numNoDelayRetries":3,"numMinDelayRetries":2,"numMaxDelayRetries":35,"backoffFunction":"exponential"},
 "throttlePolicy":{"maxReceivesPerSecond":10},
 "requestPolicy":{"headerContentType":"application/json"}}
```
That example (from the SNS docs) makes 50 attempts: 3 immediate, 2 pre-backoff at 1 s, 10 backoff retries from 1 to 60 s,
35 post-backoff at 60 s. The topic-level `DeliveryPolicy` attribute wraps the same fields under `"http"` with
`defaultHealthyRetryPolicy`, `defaultThrottlePolicy`, `defaultRequestPolicy` and `disableSubscriptionOverrides`.
```bash
aws sns set-subscription-attributes --subscription-arn "$SUB" --attribute-name DeliveryPolicy --attribute-value file://policy.json
```
- `numRetries` is 0 to 100 (immediate + pre-backoff + backoff + post-backoff); `minDelayTarget` runs from 1 to
  the maximum delay, `maxDelayTarget` up to 3,600; the **total policy retry time for HTTP/S cannot exceed
  3,600 seconds** (hard limit). `backoffFunction` is `arithmetic`, `exponential`, `geometric` or `linear` (default linear).
- `throttlePolicy.maxReceivesPerSecond` limits the average deliveries per second per subscription (default no
  throttling); it is an average, not a hard cap, and throttled messages are re-queued without using retries.
- SNS retries 5xx and 429 responses; all other errors are permanent failures and are not retried.
- `headerContentType` changes the POST content type from the default `text/plain; charset=UTF-8`; with raw
  delivery off, or a topic-level policy, only `application/json` and `text/plain` are supported.

## 3. Subscription DLQ (redrive policy)
```bash
aws sns set-subscription-attributes --subscription-arn "$SUB" --attribute-name RedrivePolicy \
  --attribute-value '{"deadLetterTargetArn":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:sns-dlq"}'
```
The DLQ is an SQS queue in the same account and Region (standard for standard topics, FIFO for FIFO topics)
whose queue policy allows `sns.amazonaws.com` to `SQS:SendMessage` with `aws:SourceArn` equal to the **topic**
ARN. Use the maximum 14-day retention. Alarm on DLQ `ApproximateNumberOfMessagesVisible` (not
`NumberOfMessagesSent`, which does not count messages moved on failure). Client-side errors (endpoint deleted,
policy changed) go straight to the DLQ without retries; server-side errors go after the retry policy is exhausted.
Drain a subscription DLQ with a Lambda function using it as an event source, or with your own consumer:
SQS `StartMessageMoveTask` does not support DLQs whose source is SNS.

## 4. Delivery status logging
Without delivery status logging a failing subscriber is visible only through metrics such as
`NumberOfNotificationsFailed`. Enable per protocol on the topic (`HTTP`, `SQS`, `Lambda`, `Firehose` and
`Application` prefixes):
```bash
aws sns set-topic-attributes --topic-arn "$TOPIC" --attribute-name HTTPSuccessFeedbackRoleArn --attribute-value arn:aws:iam::<ACCOUNT_ID>:role/SNSFeedback
aws sns set-topic-attributes --topic-arn "$TOPIC" --attribute-name HTTPFailureFeedbackRoleArn --attribute-value arn:aws:iam::<ACCOUNT_ID>:role/SNSFeedback
aws sns set-topic-attributes --topic-arn "$TOPIC" --attribute-name HTTPSuccessFeedbackSampleRate --attribute-value 5
```
The role gives SNS write access to CloudWatch Logs. `<PROTOCOL>SuccessFeedbackSampleRate` is the percentage
(0 to 100) of successful deliveries logged; once `<PROTOCOL>FailureFeedbackRoleArn` is set, every failed
delivery is logged. Log records are JSON with `status` (`SUCCESS` or `FAILURE`), `notification.messageId` and a
`delivery` object containing `statusCode`, `dwellTimeMs` (publish to hand-off), `attempts` and `providerResponse`:
the place to see why a delivery failed. Logging is documented for Firehose, SQS, Lambda, HTTPS and platform
application endpoints.

## 5. Alarms
- `NumberOfNotificationsFailed` (Sum, dimension `TopicName`) > 0 for 5 min. For SQS, email, SMS and push it
  increments once when SNS stops attempting; for HTTP/S it counts every failed attempt including retries; it
  excludes messages rejected by filter policies.
- `NumberOfNotificationsFailedToRedriveToDlq` > 0 means the DLQ itself is misconfigured;
  `NumberOfNotificationsRedrivenToDlq` counts messages moved to a DLQ.
- Valid metric dimensions are Application, PhoneNumber, Platform and TopicName, so there is no per-subscription
  dimension: use the delivery logs for that.

## Gotchas
- Only HTTP/S subscriptions can have a custom delivery policy; the SQS and Lambda policies are fixed.
- The usage metric `ApproximateNumberOfPendingSubscriptions` (namespace `AWS/Usage`) tracks pending subscriptions.

## Verify
- [ ] Stop the HTTP endpoint; delivery logs show `FAILURE` with the configured number of attempts and increasing `dwellTimeMs`; the message appears in the DLQ.
- [ ] Restore the endpoint; new messages succeed and `NumberOfNotificationsFailed` returns to 0.
- [ ] `get-subscription-attributes` shows the `DeliveryPolicy` you set.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide and API Reference, SQS key-management and StartMessageMoveTask references.
Confirmed: retry phase counts and windows per protocol; HTTP/S delivery policy fields, ranges, defaults, 3,600 s total limit, retryable codes (5xx, 429), throttle policy semantics, content-type handling; topic-level `DeliveryPolicy` shape; DLQ queue policy, same account and Region, FIFO matching, 14-day recommendation, client-vs-server error behaviour, draining options; delivery-status attribute names (`HTTP`, `SQS`, `Lambda`, `Firehose`, `Application` prefixes), sample rate 0 to 100, log record fields; metric names and definitions; `StartMessageMoveTask` does not support SNS-fed DLQs.
Corrected: the example policy exceeded the 3,600 s hard limit and is replaced by the documented example; the SQS/Lambda row is now exact; "4xx never retries except 429" is now "only 5xx and 429 are retried"; redrive by `start-message-move-task` is not supported for SNS DLQs.
Removed (not in docs): 15 s endpoint timeout, DLQ error attributes, log group name pattern, KMS/Authorization error examples, unsubscribe and Lambda on-failure remarks, MessageId dedupe remark, `EffectiveDeliveryPolicy`.
Sources: https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-configure-dead-letter-queue.html ; https://docs.aws.amazon.com/sns/latest/api/API_SetTopicAttributes.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-msg-status.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html

Method: documentation only; no commands were run.
