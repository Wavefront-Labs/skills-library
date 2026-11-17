---
id: computing-software.software-engineering.mobile-development.in-app-purchases-and-subscriptions
name: in-app-purchases-and-subscriptions
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-platform-services, in-app-purchases, storekit, google-play-billing, subscriptions, receipt-validation]
level: practitioner
status: draft
description: "Implement in-app purchases and subscriptions with StoreKit 2 and Play Billing: product setup, purchase flow, server-side verification, entitlements, renewals and refunds."
sources:
  - https://developer.apple.com/documentation/storekit/in-app-purchase
  - https://developer.apple.com/documentation/appstoreserverapi
  - https://developer.android.com/google/play/billing/integrate
  - https://developer.android.com/google/play/billing/rtdn-reference
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# In-app purchases and subscriptions

**Goal:** users get exactly what they paid for on every device, renewals and refunds are reflected automatically, and fraud is filtered server-side.

## 1. Products
Create products in App Store Connect / Play Console: consumables, non-consumables, auto-renewable subscriptions (grouped into subscription groups / base plans with offers). IDs are permanent; plan naming (`pro_monthly`, `pro_yearly`).

## 2. iOS: StoreKit 2
```swift
let products = try await Product.products(for: ["pro_monthly", "pro_yearly"])
let result = try await product.purchase(options: [.appAccountToken(user.uuid)])   // ties purchase to your user
switch result {
case .success(let verification):
    let transaction = try checkVerified(verification)   // JWS signed by Apple, verified on device
    await sendToServer(transaction.jwsRepresentation)
    await transaction.finish()                           // always finish after granting
case .pending, .userCancelled: break
@unknown default: break
}
// on launch: listen for renewals, refunds, purchases from other devices
Task { for await update in Transaction.updates { await handle(update) } }
// current entitlements
for await e in Transaction.currentEntitlements { ... }
```
Provide "Restore Purchases" (`AppStore.sync()`), required by review for non-consumables/subscriptions.

## 3. Android: Play Billing Library
```kotlin
val params = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(listOf(
        BillingFlowParams.ProductDetailsParams.newBuilder()
            .setProductDetails(details).setOfferToken(offerToken).build()))
    .setObfuscatedAccountId(user.hashedId)
    .build()
billingClient.launchBillingFlow(activity, params)
// PurchasesUpdatedListener -> send purchase.purchaseToken to the server -> server verifies -> acknowledge
```
Purchases must be **acknowledged within 3 days** (`acknowledgePurchase` or server-side `purchases.subscriptions.acknowledge`) or Google refunds them automatically. Consumables: `consumeAsync` after granting. Query `queryPurchasesAsync` on app start to recover missed purchases.

## 4. Server is the source of truth
- Verify: Apple App Store Server API (`Get Transaction Info`, signed JWS verification with Apple's root cert) and Google Play Developer API (`purchases.subscriptionsv2.get`).
- Real-time updates: App Store Server Notifications V2 and Google Real-time Developer Notifications (Pub/Sub) for renewals, grace period, billing retry, cancellations, refunds, revocations.
- Store entitlements per user (`pro_until`, state); the app asks your server, not just local receipts.
- Idempotency: the same transaction may arrive from the app and from notifications; key on transaction ID / purchase token.

## 5. Subscription states to handle
Active, in free trial/intro offer, in grace period (keep access), in billing retry / account hold (revoke or limit), paused (Play), cancelled but active until period end, expired, refunded/revoked (remove access), upgraded/downgraded/crossgraded.

## 6. Testing
- iOS: StoreKit configuration files in Xcode (local, time-accelerated renewals), sandbox accounts, TestFlight (renewals accelerated).
- Android: license testers in Play Console, test card "always approves/declines", accelerated renewal periods in test.

## Gotchas
- Digital content unlocked in-app must use IAP (store policies); physical goods use regular payments.
- Never trust client-side "purchase success" alone to unlock server-side features; verify.
- Price display: use the localized price string from the product, never hard-coded prices.
- Family Sharing (iOS) and multiple Google accounts complicate ownership; use account tokens.

## Verify
- Sandbox/test purchases unlock on two devices for the same user, a refund issued from the store console revokes access via server notification, and unacknowledged Android purchases are not left behind (monitor).
