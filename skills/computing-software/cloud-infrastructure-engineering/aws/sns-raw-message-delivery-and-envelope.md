---
id: computing-software.cloud-infrastructure-engineering.aws.sns-raw-message-delivery-and-envelope
name: sns-raw-message-delivery-and-envelope
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, raw-message-delivery, sns-envelope, message-format, sqs-subscription, json-envelope, message-attributes, signature-verification, signing-cert, sns-to-sqs, sns-to-lambda, messaging]
level: practitioner
status: docs-checked
description: "Decide between raw message delivery and the SNS JSON envelope per subscription, parse each shape correctly in SQS/Lambda/HTTP consumers, and verify SNS signatures on HTTP endpoints."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-large-payload-raw-message-delivery.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message-verify-message-signature.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html", "https://docs.aws.amazon.com/sns/latest/api/API_SetTopicAttributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS raw message delivery vs the JSON envelope

**Goal:** consumers parse what they actually receive — a bare payload or an SNS envelope — and
nothing double-encodes, double-escapes or loses attributes on the way through SQS.

## 1. The envelope (default)
With `RawMessageDelivery=false`, SQS and HTTP/S subscribers receive JSON like this as the message body:
```json
{"Type":"Notification","MessageId":"...","TopicArn":"arn:aws:sns:...","Subject":"optional",
 "Message":"<your payload as a STRING>","Timestamp":"2026-10-16T09:00:00.000Z",
 "SignatureVersion":"1","Signature":"...","SigningCertURL":"https://sns.<REGION>.amazonaws.com/SimpleNotificationService-....pem",
 "UnsubscribeURL":"..."}
```
`Message` is a string, so a JSON payload is **escaped JSON inside JSON**: consumers must parse the body and then
parse `Message` again.

## 2. Raw delivery
```bash
aws sns set-subscription-attributes --subscription-arn "$SUB" --attribute-name RawMessageDelivery --attribute-value true
```
- Supported for **SQS, HTTP/S and Firehose** subscriptions (`RawMessageDelivery` subscription attribute set to `true`).
- SQS: SNS metadata is stripped and the message is sent as is, so the body is the exact published message. With
  raw delivery a maximum of **10 message attributes** can be sent; SNS discards messages with more than 10
  attributes bound for a raw-delivery SQS subscription, treating it as a client-side error. To send more, disable raw delivery.
- HTTP/S: the header `x-amz-sns-rawdelivery: true` is added, the body is the message as published, and the
  message attributes are **not sent**. Because the JSON envelope (which carries `Signature`) is gone, there is no
  signature to verify in the body: authenticate the endpoint another way or stay enveloped.
- Firehose: the message body is delivered and message attributes are not sent.

## 3. Choosing
Raw when: the SQS consumer also receives from other producers (uniform shape) or should see the bare payload.
Envelope when: HTTP endpoints must verify the signature, or consumers need `TopicArn`, `Subject`, `Timestamp`
or message attributes (which HTTP/S and Firehose raw delivery do not send).

## 4. Verifying signatures (HTTP, enveloped)
1. Check that `SigningCertURL` is on a trusted AWS domain (for example `https://sns.us-east-1.amazonaws.com`),
   fetch it over HTTPS, and reject anything else; do not trust certificates supplied in the message without validation.
2. Build the string to sign from key/value pairs in byte-sort (alphabetical) order, each key and value followed
   by a newline: `Message, MessageId, Subject (only if present), Timestamp, TopicArn, Type` for a Notification;
   `Message, MessageId, SubscribeURL, Timestamp, Token, TopicArn, Type` for SubscriptionConfirmation and
   UnsubscribeConfirmation. No extra fields, and a single trailing newline after the last value.
3. Base64-decode `Signature` and verify it with the certificate's public key: SHA1 for `SignatureVersion` 1,
   SHA256 for `SignatureVersion` 2 (AWS recommends 2; the topic attribute `SignatureVersion` defaults to 1).
4. Reject any message with an unexpected `TopicArn`.
The AWS SDKs for SNS provide built-in validation logic: prefer it to hand-rolled code.

## 5. Confirming HTTP subscriptions
First POST is `Type: SubscriptionConfirmation` with `SubscribeURL` and `Token`; confirm it by requesting the
`SubscribeURL` or with `confirm-subscription --token`. Check the `x-amz-sns-message-type` header before
trusting the body, and verify the signature first.

## Gotchas
- Flipping `RawMessageDelivery` on a live subscription changes the body shape immediately;
  deploy the consumer change first and make it accept both shapes during the switch
  (`if body.get("Type") == "Notification"`).
- `Subject` and other SNS metadata exist only in the envelope; raw delivery drops them (put what you need in the payload).

## Verify
- [ ] Publish `{"a":1}` to a raw-delivery queue: `receive-message` body is exactly `{"a":1}` and `--message-attribute-names All` shows the SNS attributes as SQS attributes.
- [ ] Same publish to an enveloped queue: body has `Type: Notification` and `Message` equals the string `{"a":1}`.
- [ ] HTTP endpoint rejects a crafted notification whose `SigningCertURL` points to a non-SNS host.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (raw message delivery, signature verification, HTTP/S endpoints).
Confirmed: protocols supporting raw delivery (SQS, HTTP/S, Firehose); `RawMessageDelivery` attribute; envelope fields; 10-attribute SQS limit and discard behaviour; `x-amz-sns-rawdelivery` header; attributes not sent for HTTP/S and Firehose raw delivery; signature versions 1 (SHA1) and 2 (SHA256, recommended); string-to-sign fields, byte-sort order and trailing newline for Notification and confirmation messages; trusted-domain rule for `SigningCertURL`; TopicArn check; `SignatureVersion` topic attribute default 1.
Corrected: the draft's confused SQS attribute sentence ("No: delivery is dropped") now states the documented behaviour; the draft said HTTP/S raw delivery moves SNS attributes into headers, but the docs say message attributes are not sent.
Removed (not in docs): Lambda-always-envelope claim, specific `x-amz-sns-*` header list in raw mode, Extended Client requirement, envelope-size figure, validator library names, 3-day unconfirmed expiry, FIFO pass-through, Binary-attribute and Lambda batch remarks.
Sources: https://docs.aws.amazon.com/sns/latest/dg/sns-large-payload-raw-message-delivery.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message-verify-message-signature.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html ; https://docs.aws.amazon.com/sns/latest/api/API_SetTopicAttributes.html

Method: documentation only; no commands were run.
