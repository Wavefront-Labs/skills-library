---
id: computing-software.cloud-infrastructure-engineering.aws.sns-subscription-confirmation-and-https-endpoints
name: sns-subscription-confirmation-and-https-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, https-endpoint, subscription-confirmation-flow, message-signature, signature-version, webhook]
level: practitioner
status: docs-checked
description: "Build an HTTPS endpoint that receives SNS: confirm subscriptions, verify message signatures (SignatureVersion 2), handle retries/delivery policy, and avoid spoofing."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message-verify-message-signature.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS to HTTPS endpoints

## 1. Message types your endpoint receives
SNS POSTs JSON with header `x-amz-sns-message-type`:
- `SubscriptionConfirmation`: contains `SubscribeURL` and `Token`.
- `Notification`: the actual message.
- `UnsubscribeConfirmation`: after someone unsubscribes.
Content-Type is `text/plain; charset=UTF-8` even though the body is JSON (frameworks that
only parse `application/json` see an empty body).

## 2. Confirm the subscription
```bash
aws sns subscribe --topic-arn arn:aws:sns:eu-west-1:111122223333:orders \
  --protocol https --notification-endpoint https://hooks.example.com/sns
```
The endpoint receives a `SubscriptionConfirmation`. After verifying the signature, either
GET the `SubscribeURL`, or call:
```bash
aws sns confirm-subscription --topic-arn <topic> --token <Token> --authenticate-on-unsubscribe true
```
`--authenticate-on-unsubscribe` sets the subscription's `AuthenticateOnUnsubscribe` flag, which forces
authentication on unsubscribe requests (it cannot be set when the confirmation link is followed without authentication).

## 3. Verify every message signature
Never trust the body without checking:
1. `SigningCertURL` must be fetched over HTTPS from a trusted AWS domain (for example
   `https://sns.us-east-1.amazonaws.com`); reject anything else and do not trust unvalidated certificates.
2. Build the string to sign in byte-sort (alphabetical) key order: for a Notification `Message`,
   `MessageId`, `Subject` (only if present), `Timestamp`, `TopicArn`, `Type`; for SubscriptionConfirmation and
   UnsubscribeConfirmation `Message`, `MessageId`, `SubscribeURL`, `Timestamp`, `Token`, `TopicArn`, `Type`.
   Each is `Name\nValue\n`, with a single trailing newline and no extra fields.
3. Verify `Signature` (base64) with the certificate's public key: SHA1 for `SignatureVersion` 1,
   **SHA256 for version 2** (recommended). The topic attribute `SignatureVersion` defaults to 1;
   `aws sns set-topic-attributes --topic-arn <topic> --attribute-name SignatureVersion --attribute-value 2`.
4. Reject messages with an unexpected `TopicArn`.
The AWS SDKs for SNS provide built-in validation logic; prefer it to hand-rolled code.

## 4. Retries and delivery policy
HTTP/S endpoints get retries per the **delivery policy**; the default is `numRetries` 3 with `minDelayTarget` and
`maxDelayTarget` of 20 s and a linear backoff, so a minute-long outage can lose messages. SNS retries 5xx and 429 responses; all
other errors are permanent failures. The total retry time cannot exceed 3,600 s. Customise:
```json
{"healthyRetryPolicy": {"numRetries": 10, "minDelayTarget": 5, "maxDelayTarget": 60,
  "numMinDelayRetries": 2, "numMaxDelayRetries": 3, "backoffFunction": "exponential"},
 "throttlePolicy": {"maxReceivesPerSecond": 20}}
```
Return 2xx quickly (enqueue work internally). Add a **subscription DLQ** (redrive policy to SQS) so messages
that exhaust retries are kept.

## 5. Security
- SNS supports SNI, and Basic and Digest authentication with credentials in the HTTPS URL
  (`https://user:password@host/path`; the client must handle a `401 Unauthorized` challenge). SNS does not
  support private HTTP(S) endpoints. The URL with credentials can be read only through `GetSubscriptionAttributes`.
- Rate-limit with `throttlePolicy.maxReceivesPerSecond` and make the handler idempotent (use `MessageId`).

## Verify
- [ ] Subscription status `Confirmed` with authenticated unsubscribe.
- [ ] A forged POST (modified Message) is rejected by signature verification.
- [ ] Endpoint outage test: messages land in the subscription DLQ after retries.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (HTTP/S endpoints, signature verification, delivery retries).
Confirmed: header `x-amz-sns-message-type` and message types; `text/plain; charset=UTF-8` content type; confirmation flow and `AuthenticateOnUnsubscribe`; signature fields, order, versions and `SigningCertURL` rule; `SignatureVersion` topic attribute (default 1); delivery-policy defaults and limits; retryable codes (5xx, 429); SNI, Basic and Digest authentication, no private endpoints.
Removed (not in docs): 3-day confirmation-token and pending-subscription expiry, 15-second timeout, self-signed certificate rejection, named validator libraries.
Sources: https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message-verify-message-signature.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html

Method: documentation only; no commands were run.
