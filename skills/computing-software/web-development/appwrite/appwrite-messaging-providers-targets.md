---
id: computing-software.web-development.appwrite.appwrite-messaging-providers-targets
name: appwrite-messaging-providers-targets
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, messaging, providers, targets, subscribers]
level: practitioner
status: docs-checked
description: "Configure messaging providers for push, email and SMS and understand targets that represent delivery addresses."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/providers/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/targets/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: prepare Appwrite Messaging.

Providers: before you can deliver messages, you must connect a third-party messaging provider.
- Push: APNs (Apple Push Notification service) and FCM (Firebase Cloud Messaging; Android, Apple or Web apps).
- Email: Mailgun, Resend, SendGrid and SMTP.
- SMS: Twilio, MSG91, Telesign, Textmagic and Vonage.

Targets are the different ways a user can be reached. A user with two emails, a phone number, a phone and a tablet with your app installed has five targets. Target types: Email, SMS and Push notification. Targets can subscribe to a topic, so a message published to the topic reaches all subscribed targets.

Adding targets:
- Email: verified emails of users who signed up with email password, magic URL, email OTP or OAuth2 already have an email target.
- SMS: verified phone numbers of users who signed up with Phone OTP already have a phone target.
- Push: needs configuration on both the Appwrite platform and the client app. For iOS with APNs: in the Apple Developer Member Center > Keys, create a key with Apple Push Notification Service enabled, note the key ID and download the key, then add the Push Notifications capability in Xcode (Signing & Capabilities). For FCM on iOS or Android, the page lists the Firebase console steps (add the app, download `google-services.json`, upload the APNs key for iOS, or add the Google Services plugin and a notification handler service to `AndroidManifest.xml` for Android).

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Providers and Targets: the provider lists, the target concept and types, the topic relationship, and the email, SMS and push target setup. Removed: the Console path for adding a provider, the "at least one provider per message type" rule, `users.createTarget` and `messaging.createSubscriber` (neither is named on these pages), the gotcha about unverified contacts, and the Verify step.
Method: documentation only; no commands were run.
