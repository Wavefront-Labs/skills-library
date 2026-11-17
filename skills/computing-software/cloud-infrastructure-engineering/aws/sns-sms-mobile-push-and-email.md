---
id: computing-software.cloud-infrastructure-engineering.aws.sns-sms-mobile-push-and-email
name: sns-sms-mobile-push-and-email
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, sns-sms, mobile-push, sms-sandbox, origination-identity, sender-id, 10dlc, toll-free-number, platform-application, device-token, apns, fcm, email-subscription, transactional-sms, promotional-sms, opt-out, end-user-messaging, messaging]
level: practitioner
status: docs-checked
description: "Send SMS, mobile push and email through SNS: leave the SMS sandbox, register 10DLC/toll-free/sender IDs, manage push endpoints and stale tokens, handle opt-outs and spend limits."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-phone-number-as-subscriber.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html", "https://docs.aws.amazon.com/sns/latest/dg/channels-sms-originating-identities.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-email-notifications.html", "https://docs.aws.amazon.com/sns/latest/dg/sms_preferences.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS SMS, mobile push and email

**Goal:** OTP and alert messages reach phones reliably in every target country, and the SMS bill has a ceiling.

## 1. SMS: sandbox and account settings
Newly created SNS SMS accounts are placed in the **SMS sandbox**: you can only send to verified destination phone
numbers (up to 10), and the restrictions are lifted when the account moves out of the sandbox (see "Moving out of the
Amazon SNS SMS sandbox" in the SNS guide).
```bash
aws sns create-sms-sandbox-phone-number --phone-number +44... 
aws sns verify-sms-sandbox-phone-number --phone-number +44... --one-time-password <OTP>
aws sns set-sms-attributes --attributes DefaultSMSType=Transactional,MonthlySpendLimit=100,DefaultSenderID=MyApp
```
- Message types: `Transactional` (the default) is optimised for the highest reliability, for critical messages such as
  one-time passcodes; `Promotional` is optimised for lowest cost.
- The monthly spend quota defaults to 1.00 USD; request a service quota increase to raise it. SNS is distributed, so
  it stops sending within minutes of the quota being exceeded and you can overshoot in that interval.
- Pricing and routing differ per destination country; see the vendor's SMS pricing page.
- Choose a Region that supports SMS messaging.

## 2. Origination identities
- **Sender ID** (alphabetic name): supported in several countries; in some, businesses messaging individuals must use
  a sender ID pre-registered with a regulator or industry group.
- **Origination numbers** (long codes, 10DLC, toll-free, short codes) are not available in countries where local law
  requires sender IDs. SNS now uses AWS End User Messaging SMS for delivery, and phone numbers and sender IDs are
  managed there; some countries require company registration before you can buy them.

## 3. Mobile push
Create a platform application per push service (APNs, FCM, ...) with `aws sns create-platform-application`, create one
endpoint per device token with `aws sns create-platform-endpoint`, and publish to the endpoint ARN with
`--message-structure json` carrying one payload per service. The push services return a device token when an app
registers; follow the SNS "mobile push token management" guide for stale tokens.

## 4. Email
You must confirm an email subscription before the address receives messages. Exceeding 10 messages per second (TPS)
for an `email` or `email-json` endpoint suspends the subscription into `PendingConfirmation`; a bounced address is
suppressed from further delivery for 7 days.

## 5. Delivery logs
SMS delivery status logs go to CloudWatch log groups named `sns/<REGION>/<ACCOUNT_ID>/DirectPublishToPhoneNumber`
(and `.../Failure`); entries carry fields such as `providerResponse` and `dwellTimeMs`.

## Gotchas
- Use E.164 phone numbers (`+` and country code).

## Verify
- [ ] Sandbox: publish to an unverified number fails; after leaving the sandbox it succeeds and the delivery log shows success.
- [ ] A test with a deliberately low spend quota stops sending as expected.

## Checked

2026-10-28. Confirmed against the SNS Developer Guide pages sns-sms-sandbox, sms_preferences, channels-sms-originating-identities, sns-mobile-phone-number-as-subscriber, sns-mobile-application-as-subscriber and sns-email-notifications: sandbox rules, message types (Transactional is the default), 1.00 USD default spend quota and overshoot behaviour, sender ID and origination number support, End User Messaging integration, email confirmation, 10 TPS suspension and 7-day bounce suppression, log group naming.
Removed or corrected: "Transactional" was shown as an optional setting but it is the default; 140/160/70-character message-length rules, 30-day opt-in rule, SMSMonthToDateSpentUSD and 80% alarm, 10DLC/toll-free/short-code timelines, push attribute details (disabled-endpoint behaviour, EventEndpointUpdated, FCM v1 credential format), per-subscriber charging, the SES recommendation and all pricing text.
Method: documentation only; no commands were run.
