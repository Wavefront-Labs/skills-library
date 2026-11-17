---
id: computing-software.software-engineering.mobile-development.push-notifications-apns-and-fcm
name: push-notifications-apns-and-fcm
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-platform-services, push-notifications, fcm, apns, notification-channels, rich-notifications]
level: practitioner
status: draft
description: "Implement push notifications with APNs and FCM: token lifecycle, permission prompts, payload types, Android channels, iOS service extensions, delivery limits and testing."
sources:
  - https://developer.apple.com/documentation/usernotifications
  - https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns
  - https://firebase.google.com/docs/cloud-messaging
  - https://developer.android.com/develop/ui/views/notifications/notification-permission
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Push notifications with APNs and FCM

**Goal:** notifications that arrive reliably, respect user permission and preferences, and can be tested end to end.

## 1. Architecture
App registers -> gets a device token (APNs) / registration token (FCM) -> sends it to your backend with the user ID -> backend sends via APNs HTTP/2 (token-based `.p8` auth) or FCM HTTP v1 API (OAuth service account). FCM can also deliver to iOS via APNs if you configure the APNs key in Firebase.

## 2. Permission
- iOS: `UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound])`, then `UIApplication.shared.registerForRemoteNotifications()`. Provisional authorization (`.provisional`) delivers quietly to Notification Center without a prompt.
- Android 13+: runtime permission `POST_NOTIFICATIONS`; ask in context after explaining the value, not on first launch. Below 13, notifications are allowed by default.
- Users who deny once are hard to win back; a pre-prompt screen improves opt-in.

## 3. Tokens
- Tokens change (reinstall, restore, app data cleared, FCM rotation): handle `didRegisterForRemoteNotificationsWithDeviceToken` / `FirebaseMessagingService.onNewToken` every launch and upsert on the server.
- Remove tokens when APNs returns `410 Unregistered` / `400 BadDeviceToken` or FCM returns `UNREGISTERED`/`NOT_FOUND`.
- Associate tokens with user and device; delete on logout.

## 4. Payloads
APNs:
```json
{ "aps": { "alert": { "title": "Order shipped", "body": "Arrives Friday" }, "sound": "default",
           "thread-id": "order-42", "mutable-content": 1 },
  "orderId": "42" }
```
Headers: `apns-push-type` (`alert` / `background`), `apns-priority` (10 immediate, 5 power-saving), `apns-topic` (bundle ID), `apns-collapse-id`. Background (`content-available: 1`) pushes are throttled and not guaranteed.
FCM v1:
```json
{ "message": { "token": "...", "notification": { "title": "Order shipped", "body": "Arrives Friday" },
  "data": { "orderId": "42" }, "android": { "priority": "high", "notification": { "channel_id": "orders" } } } }
```
Android: "notification" messages are shown by the system when the app is in background; "data"-only messages are delivered to `onMessageReceived` (and you build the notification). High priority is for user-visible, time-sensitive messages; abuse gets deprioritised.

## 5. Platform specifics
- Android **notification channels** (8.0+): create at startup (`NotificationChannel("orders", ..., IMPORTANCE_DEFAULT)`); users control each channel; importance cannot be raised after creation.
- iOS **Notification Service Extension** (`mutable-content: 1`) modifies content before display: download images, decrypt end-to-end encrypted payloads; it has about 30 seconds.
- Deep link from notification tap to the right screen (see navigation/deep-link handling).
- Time-sensitive / critical interruption levels need entitlements and justification.

## 6. Testing
- iOS simulator: drag an `.apns` file onto it or `xcrun simctl push booted com.acme.app payload.apns`.
- APNs sandbox vs production environments must match the build's `aps-environment` entitlement.
- FCM: send test messages from the Firebase console or `curl` with an access token; Android emulator with Google Play services.

## Gotchas
- Battery optimisation / OEM task killers (some Android vendors) delay or drop messages; high-priority FCM and user education help.
- Payload limit: 4 KB for both; send IDs and fetch details.
- Do not send sensitive data in clear notification text; it shows on the lock screen.

## Verify
- Token refresh path tested (reinstall), sends to stale tokens are cleaned up from server responses, and notifications deep-link correctly from cold start, background and foreground.
