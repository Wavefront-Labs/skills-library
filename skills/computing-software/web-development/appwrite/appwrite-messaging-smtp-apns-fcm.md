---
id: computing-software.web-development.appwrite.appwrite-messaging-smtp-apns-fcm
name: appwrite-messaging-smtp-apns-fcm
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, messaging, smtp, apns, fcm, push]
level: advanced
status: docs-checked
description: "Set up the SMTP, APNs and FCM providers with the specific fields and credentials each requires."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/smtp/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/apns/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/fcm/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: wire real delivery providers. Each is added at Messaging > Providers > Add provider, then you name it, choose the type and click Save and continue; the provider is saved but not enabled until its configuration is complete.

SMTP (for a third-party SMTP provider Appwrite does not support, or your own server; Email type): fields are Host, Port, Username, Password, Encryption (SSL or TLS), Auto TLS (uses TLS if available), Mailer (the SMTP server or provider), Sender email, Sender name, Reply-to email and Reply-to name. Sender and reply-to emails must be under the configured domain. Click Save and continue to enable it.

APNs (Push notification type): needs these from the Apple Developer Member Center: Team ID (Membership details), Bundle ID (Identifiers), Authentication key ID and the Authentication key (.p8 file), both from Keys, where the key must have Apple Push Notification Service enabled. Sandbox mode is for apps signed with development provisioning profiles: APNs has Development (sandbox) and Production environments, and development Xcode builds use the development environment while production builds use the production one. In the iOS app, add the Push Notifications capability under Signing & Capabilities. APNs is best effort and keeps the last message for 30 days or less for an offline device.

FCM (Push notification type): FCM must be enabled on the Firebase project (Project settings > Cloud Messaging). Generate a key at Project settings > Service accounts > Generate new private key, then provide it to the provider. App setup: Android needs the `com.google.firebase:firebase-messaging` SDK, `google-services.json` at the project root, the Google Services class path and plugin in Gradle, and a notification handler service in `AndroidManifest.xml`. iOS needs `GoogleService-Info.plist`, an APNs key uploaded in the Firebase console (Cloud Messaging > APNs authentication key), the Push Notifications capability, and for SwiftUI `FirebaseAppDelegateProxyEnabled` set to `NO` in `Info.plist`. Flutter uses `flutterfire configure`, `firebase_messaging` and `firebase_core`.

Managing providers: update or delete in the Console (Messaging > Providers > your provider) or with a Server SDK (for example `updateSmtpProvider`, `updateApnsProvider`, `updateFCMProvider`, `deleteProvider`). To test, follow the Send push notification flow; for email, create a test message in Messaging > Messages > Create message > Email, select a test target, schedule Now and click Send.

Other email and SMS providers have their own docs pages and are not covered here.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages SMTP, Apple Push Notification service and Firebase Cloud Messaging: the add-provider steps, every SMTP field, the APNs fields and sandbox explanation, the 30 day retention note, the FCM enable and key steps, the per-platform app setup, and the manage and test sections. Removed: the "paste its private key JSON" wording, the claim that `google-services.json` is the iOS file (the FCM page says `GoogleService-Info.plist`), the silent-failure gotcha about sandbox mismatches, and the Verify step.
Method: documentation only; no commands were run.
