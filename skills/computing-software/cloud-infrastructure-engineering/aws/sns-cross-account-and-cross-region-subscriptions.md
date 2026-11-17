---
id: computing-software.cloud-infrastructure-engineering.aws.sns-cross-account-and-cross-region-subscriptions
name: sns-cross-account-and-cross-region-subscriptions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, sns-cross-account, cross-region-subscription, cross-account-sqs, topic-policy, queue-policy, subscription-confirmation, multi-account, event-distribution, aws-principalorgid, messaging]
level: practitioner
status: docs-checked
description: "Subscribe an SQS queue or Lambda in another account or region to an SNS topic: both policies required, who runs subscribe, pending-confirmation traps, and org-wide publish/subscribe grants."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-send-message-to-sqs-cross-account.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-cross-region-delivery.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-access-policy-use-cases.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-key-management.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS cross-account and cross-region subscriptions

**Goal:** a central event topic in account A delivers to queues and functions in accounts B,
C and other regions, with no "pending confirmation" surprises and no over-broad policies.

## 1. Cross-account SQS subscriber (the common case)
Two policies, one subscribe call. In **account B** (queue owner), allow the topic to send:
```json
{"Effect":"Allow","Principal":{"Service":"sns.amazonaws.com"},"Action":"sqs:SendMessage",
 "Resource":"arn:aws:sqs:<REGION>:<B>:events-queue",
 "Condition":{"ArnEquals":{"aws:SourceArn":"arn:aws:sns:<REGION>:<A>:events"}}}
```
In **account A** (topic owner), allow B to subscribe (a topic policy statement naming B's account ID):
```json
{"Effect":"Allow","Principal":{"AWS":"<B>"},"Action":"sns:Subscribe",
 "Resource":"arn:aws:sns:<REGION>:<A>:events","Condition":{"StringEquals":{"sns:Protocol":"sqs"}}}
```
Only the account's root user or administrators can call `sns:Subscribe` by default; the IAM user or role
in B must also be granted `sns:Subscribe`. Then run the subscribe **from account B** (the queue owner):
`aws sns subscribe --topic-arn arn:aws:sns:<REGION>:<A>:events --protocol sqs --notification-endpoint arn:aws:sqs:<REGION>:<B>:events-queue --attributes '{"RawMessageDelivery":"true"}'`
When the queue owner creates the subscription it needs no confirmation, the queue receives notifications as
soon as `Subscribe` completes, and `AuthenticateOnUnsubscribe` is set to true automatically. AWS recommends
the queue owner creates the subscription, especially for high-volume queues.

## 2. Pending confirmation
If the subscription is created by someone who does **not** own the queue, it must be confirmed: SNS sends a
subscription confirmation message to the queue (the subscription shows as Pending Confirmation); a user who can read
the queue retrieves the `SubscribeURL` and passes it to the **subscription owner**, who confirms it (console
**Confirm subscription**, or the `ConfirmSubscription` API / `aws sns confirm-subscription` with the token).
Until confirmed no notifications reach the queue. The usage metric `ApproximateNumberOfPendingSubscriptions`
(`AWS/Usage`) tracks pending subscriptions across the account.

## 3. Cross-region
SNS supports cross-Region delivery of notifications to **SQS queues and Lambda functions**. The subscribe
command must be executed in the Region where the SNS topic is hosted, in the topic owner's account or as above.
Opt-in Regions (for example af-south-1, ap-east-1, eu-south-1, me-south-1; Regions launched after 20 March 2019)
need a Region-specific SNS service principal in the subscribed resource's policy: replace `sns.amazonaws.com`
with `sns.<topic-region>.amazonaws.com` when the topic is in an opt-in Region and the queue is in a default
Region (and `sns.<queue-region>.amazonaws.com` when the queue or function is in an opt-in Region). Keep the
`aws:SourceArn` condition on the topic ARN (the docs example uses `ArnLike`). The Lambda function policy follows the
same principal rule. See the cross-Region page for the full table.

## 4. Organisation-wide
```json
{"Effect":"Allow","Principal":{"AWS":"*"},"Action":"sns:Publish",
 "Resource":"arn:aws:sns:<REGION>:<A>:events",
 "Condition":{"StringEquals":{"aws:PrincipalOrgID":"o-xxxxxxxx"}}}
```
This is the documented pattern for letting any account in an organisation publish (the docs example uses
`sns:Publish`); the same `aws:PrincipalOrgID` condition can be used on other actions such as `sns:Subscribe`.

## 5. Encryption across accounts
If the **queue** uses SSE-KMS with a customer managed key, the key policy must allow the service principal
`sns.amazonaws.com` to use `kms:Decrypt` and `kms:GenerateDataKey` (see the SQS key-management guide); an
encrypted queue using the AWS managed SQS key cannot be used from another account's Lambda function.

## Gotchas
- A topic policy `Principal` of an account ID lets that account delegate the permission to its IAM users and roles.
- Deleting a topic removes its subscriptions; recreating the topic does not restore them, so keep subscriptions in
  the consumer account's IaC.
- An unconfirmed subscription delivers nothing: if the queue owner did not create it, someone must confirm it.

## Verify
- [ ] `list-subscriptions-by-topic` shows the B queue subscription with `SubscriptionArn` (not `PendingConfirmation`) and `Owner` = B.
- [ ] Publish in A arrives in B's queue; removing the queue policy statement for `sns.amazonaws.com` stops delivery (then restore).
- [ ] Cross-region subscription delivers and the queue message `TopicArn` shows the source region.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (cross-account SQS, cross-Region delivery, access-control examples) and SQS key-management guide.
Confirmed: queue policy for `sns.amazonaws.com` with `aws:SourceArn`; topic policy granting `sns:Subscribe` to another account with an `sns:Protocol` condition; queue-owner subscription needs no confirmation and sets `AuthenticateOnUnsubscribe`; confirmation flow for non-owners; cross-Region support for SQS and Lambda, subscribe executed in the topic's Region, opt-in Region principal rules; `aws:PrincipalOrgID` example (with `sns:Publish`); KMS permissions for SNS to an encrypted queue; topic deletion removes subscriptions; usage metric for pending subscriptions.
Corrected: the draft's `sns:Receive` requirement and the duplicate `StringEquals` org-wide policy (not valid JSON) were removed; "subscribing from account A also works and auto-confirms" was replaced by the documented confirmation flow.
Removed (not in docs): 3-day pending expiry, data-transfer charge remark, SCP advice, `list-subscriptions-by-topic` alarm advice, Lambda `add-permission` details, filter-policy ownership claim, console quirk.
Sources: https://docs.aws.amazon.com/sns/latest/dg/sns-send-message-to-sqs-cross-account.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-cross-region-delivery.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-access-policy-use-cases.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-key-management.html ; https://docs.aws.amazon.com/sns/latest/dg/message-archiving-and-replay-topic-owner.html

Method: documentation only; no commands were run.
