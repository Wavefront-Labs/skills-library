---
id: computing-software.software-engineering.mobile-development.in-app-review-prompts
name: in-app-review-prompts
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, android, in-app-review, requestreview, reviewmanager, app-ratings, play-core, storekit]
level: intro
status: draft
description: "Ask for ratings correctly on iOS and Android: StoreKit requestReview and Play ReviewManager, when to trigger, quota limits, and why you cannot detect the outcome."
sources: ["https://developer.apple.com/documentation/storekit/requesting-app-store-reviews", "https://developer.android.com/guide/playcore/in-app-review", "https://developer.apple.com/app-store/review/guidelines/#1.1.7"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# In-app review prompts

Use the system-provided prompts; custom "rate us" dialogs that gate on sentiment break store rules.

## iOS (StoreKit)
```swift
// SwiftUI, iOS 16+
@Environment(\.requestReview) private var requestReview
...
requestReview()

// UIKit / older
if let scene = view.window?.windowScene { SKStoreReviewController.requestReview(in: scene) }
```
The system decides whether to show it (a small number of times per 365 days per app); calls may do nothing. Do not attach it to a button, since the button may appear dead. For a user-initiated action, open the review page with `https://apps.apple.com/app/id<ID>?action=write-review`.

## Android (Play In-App Review API)
```kotlin
val manager = ReviewManagerFactory.create(context)
manager.requestReviewFlow().addOnSuccessListener { info ->
    manager.launchReviewFlow(activity, info)      // quota-limited; may show nothing
}
```
Test with an internal test track or an internal app share build; the flow shows a dialog without submitting from debug builds.

## When to ask
- After a clear success moment (task completed, milestone), never on first launch or mid-task.
- Gate on engagement: for example 3+ sessions and 7+ days since install, and not shortly after a crash or error.
- Track the last-asked date and app version locally to avoid repeat asks.

## Gotchas
- Neither API tells you whether the user rated, dismissed, or saw anything. Do not condition behaviour or rewards on it. Apple guideline 1.1.7 and Play policy forbid incentivised ratings.
- Do not ask a pre-question like "Do you like the app?" that routes unhappy users away from the store.
- Quotas apply in development too; do not conclude it is broken after a few calls.

Verify: on iOS TestFlight builds the prompt never actually submits; on Android check Play Console review logs with an internal-test account, and confirm your app only triggers after the engagement conditions.
