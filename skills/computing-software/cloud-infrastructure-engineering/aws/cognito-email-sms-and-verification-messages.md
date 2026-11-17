---
id: computing-software.cloud-infrastructure-engineering.aws.cognito-email-sms-and-verification-messages
name: cognito-email-sms-and-verification-messages
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cognito, cognito-ses, verification-messages, cognito-sms, sns-sms, custom-message-trigger, email-configuration]
level: practitioner
status: docs-checked
description: "Configure Cognito user pool email via SES and SMS via SNS for production: the default 50 emails per day cap, sandbox exits, verification templates and custom message triggers."
sources: ["https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-email.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-customizations.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cognito email, SMS and verification messages

## Email: switch to SES before launch
The default Cognito email sender is capped at 50 email messages per day per AWS account (the
quota resets daily at 0900 UTC), sends from `no-reply@verificationemail.com` and is meant for
testing; use your own SES identity for production volumes.
```bash
aws cognito-idp update-user-pool --user-pool-id "$POOL" --email-configuration \
  EmailSendingAccount=DEVELOPER,SourceArn=arn:aws:ses:<REGION>:<ACCOUNT_ID>:identity/example.com,From="Example <no-reply@example.com>",ConfigurationSet=cognito
```
- Use a verified SES identity in the same Region as the user pool where possible; some
  Regions require an identity in an alternate Region (see the Cognito email settings page),
  and the identity's sending authorization policy must trust the Cognito service principal.
- SES limits apply to your user pool's email delivery; confirm your SES account is out of
  the SES sandbox before launch.
- An SES configuration set (`ConfigurationSet`) can be attached for SES event publishing.
- `update-user-pool` replaces unspecified settings with defaults; pass the full current config (fetch with `describe-user-pool`) or use IaC.

## SMS via SNS
- Since November 2024 SMS is delivered by AWS End User Messaging SMS. A user pool uses one of
  two mutually exclusive paths in `SmsConfiguration`: the Amazon SNS path (`SnsCallerArn` role
  allowing `sns:Publish`, optional `SnsRegion`/`ExternalId`) or the direct path (`EumsSms` with
  `CallerArn` role allowing `sms-voice:SendTextMessage`, optional `OriginationIdentity`,
  `ConfigurationSetName`; `InEntityId`/`InTemplateId` are required for India DLT).
- The first SMS sent through Cognito puts the account in the **SMS sandbox** for that Region:
  you can send to a limited number of verified destination numbers (10 per the docs) if you have
  an origination identity, or simulate sending without one. Move the account out of the sandbox
  and obtain an origination identity for the destination countries before production.
- AWS End User Messaging SMS charges per text message; prefer TOTP or email OTP (email MFA needs the Essentials or Plus feature plan) where possible.

## Verification and invitation messages
```bash
aws cognito-idp update-user-pool --user-pool-id "$POOL" --verification-message-template \
  'DefaultEmailOption=CONFIRM_WITH_CODE,EmailSubject=Your code,EmailMessage=Your code is {####}'
```
- `{####}` is the code placeholder (required for code messages); link messages
  (`CONFIRM_WITH_LINK`) need link text in the form `{##Click here##}` (the text is yours to choose).
- Admin-created user invites use `AdminCreateUserConfig.InviteMessageTemplate`, which must contain `{username}` and `{####}`.
- **Custom message trigger** (Lambda) personalises per `triggerSource` (`CustomMessage_SignUp`,
  `CustomMessage_ForgotPassword`, ...), must keep `codeParameter` in the output, and runs within a 5 s limit.
- **Custom email/SMS sender triggers** hand the code (KMS-encrypted) to your Lambda so a third-party provider sends it.

## Gotchas
- Codes expire (24 h for sign-up verification, 1 h for forgot-password); resend with `ResendConfirmationCode`.
- Attribute changes (`email`) are unverified until confirmed; `AttributesRequireVerificationBeforeUpdate` keeps the old value until then.
- Email message limit is 20,000 UTF-8 characters and the subject limit is 140 characters; the SMS verification message limit is 140 characters.

## Verify
- [ ] `describe-user-pool` shows `EmailSendingAccount: DEVELOPER` with your SES identity.
- [ ] Sign-up email arrives from your domain, passes DKIM/SPF; SMS arrives on an unverified number (production SNS).

## Checked

Checked 2026-10-27 against the Amazon Cognito Developer Guide (email, SMS, message customization, custom message trigger, quotas), the aws-cli update-user-pool reference and the botocore cognito-idp model.
- Corrected: the default email cap is 50 messages per day per AWS account (resets 0900 UTC) from no-reply@verificationemail.com; SES Region rules (same or alternate Region) rewritten.
- Corrected: SMS has been delivered by AWS End User Messaging SMS since November 2024; SmsConfiguration has an SNS path (SnsCallerArn) and a direct path (EumsSms); the sandbox is the End User Messaging SMS sandbox (10 verified destination numbers per the docs).
- Confirmed: `{####}` placeholder, `{##text##}` link format, 20,000-character email and 140-character subject/SMS limits, 24 h sign-up and 1 h forgot-password code validity, 5 second trigger timeout, `AttributesRequireVerificationBeforeUpdate`.
- Removed: SMS pumping and per-message price claims, DKIM wording that no page confirmed.

Method: documentation only; no commands were run.
