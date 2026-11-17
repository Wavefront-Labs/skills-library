---
id: computing-software.software-engineering.mobile-development.passing-app-store-and-play-review
name: passing-app-store-and-play-review
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-release, app-review-guidelines, app-store-review, google-play-policy, data-safety, account-deletion]
level: practitioner
status: docs-checked
description: "Get mobile apps approved first time: common App Store and Google Play rejection reasons, required declarations (privacy, sign-in details, account deletion), and appeals."
sources:
  - https://developer.apple.com/app-store/review/guidelines/
  - https://developer.apple.com/distribute/app-review/
  - https://support.google.com/googleplay/android-developer/answer/9859455
  - https://support.google.com/googleplay/android-developer/answer/13327111
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passing App Store and Google Play review

**Goal:** submissions approved without rejections that delay launches, by meeting the policies reviewers check most.

## 1. Frequent App Store rejections
- **2.1 App Completeness**: Apple states that over 40% of unresolved issues are 2.1 (crashes, placeholder content, incomplete information). Submit final builds with working URLs, include demo account info (and turn on your back end) in App Review Information, and describe special configuration or hardware. If you cannot give a demo account for legal or security reasons, a built-in demo mode needs Apple's prior approval.
- **2.3 Accurate Metadata**: screenshots must show the app in use (not only title art, login or splash screens); metadata must not name other mobile platforms; describe new features specifically in Notes for Review; answer age-rating questions honestly; app names are limited to 30 characters.
- **3.1.1 In-App Purchase**: features, subscriptions, currencies and premium content unlocked in the app must use in-app purchase (not license keys, QR codes or crypto). 3.1.3 lists exceptions, including "Reader" apps (3.1.3(a)) and physical goods or services consumed outside the app (3.1.3(e)). Link-out rules differ by storefront (the guideline gives special treatment to the United States storefront) and by entitlement, so read the current 3.1.1(a) text.
- **4.2 Minimum Functionality**: apps that are repackaged websites, web clippings or link collections without app-like features are rejected.
- **5.1.1 Data Collection and Storage**: privacy policy link in App Store Connect and in the app; user consent for data collection with clear purpose strings; request only data relevant to core functionality; do not force unrelated permissions; if the app supports account creation it must offer account deletion within the app.
- **4.8 Login Services**: if the app uses a third-party or social login for the primary account, it must also offer an equivalent login service that limits collection to name and email, lets users keep their email private and does not track app interactions for advertising without consent. The guideline lists exemptions (own account system only, education or enterprise sign-in, and others).

## 2. Frequent Google Play rejections
- **App content declarations** (Play Console, Monitor and improve > Policy and programs > App content): privacy policy (live public URL, standard non-PDF page, linked in the store listing and in the app), Ads declaration, Sign-in details (provide credentials if any part of the app is restricted; up to five sets of instructions), Target audience and content, Permissions declaration form, content ratings, and the Data safety privacy and security practices.
- **High-risk permissions**: SMS and Call Log permissions are named by Google as needing the Permissions Declaration Form and approval; permission requests are evaluated when you add the app bundle.
- **Misrepresenting ads**: wrongly answering the "Contains ads" declaration (including ads from third-party SDKs) can lead to suspension; Google may verify it and add the label itself.
- **Account deletion**: if users can create an account in the app (or are sent to an outside creation flow) you must provide an in-app path to delete the account and associated data, plus a web link where users can request deletion without reinstalling the app. Answer the data deletion questions in the Data safety form; incomplete answers block new apps and updates. Exempt: permanently private and enterprise device-management apps. Non-mobile surfaces (Android TV, Wear OS) need only the outside-app option.
- **Unrated apps**: complete the content rating questionnaire or the app may be listed as "Unrated" and removed.

## 3. Pre-submission checklist
- Release build tested on devices with the latest OS; all links functional; no placeholder content.
- Demo or sign-in credentials working at review time, with notes for OTP or multi-factor logins (Play sign-in details has an "Any other instructions" field for this).
- Privacy policy URL live and accurate about data collected and shared with third-party SDKs; retention and deletion described.
- In-app account deletion works end to end where account creation exists.
- Age rating and content rating questionnaires answered honestly.

## 4. When rejected
- App Store Connect shows the guidelines not met; you can correspond with App Review there and resubmit.
- Apple appeals go to the App Review Board: give specific reasons, one appeal per rejected submission, and answer any information requests first. You can also book a 30-minute Webex appointment with App Review.
- Apple bug fix submissions: if review finds additional issues in a bug fix update (and there are no legal or safety concerns), you can accept approval now and fix the rest in the next submission by replying to the offer message.
- Apple expedited review is for extenuating circumstances (a critical bug fix with reproduction steps, or an event launch); use it sparingly.
- Google: after a rejection, update the affected declaration (for example Sign-in details), then Send for review from the Publishing overview page; no policy-team reply is needed for that flow.

## Gotchas
- Rejections often come from third-party SDK behaviour (data collection, ads); audit SDKs against your privacy policy and Play declarations.
- Review times are typical, not guaranteed: Apple reports reviewing at least 50% of submissions in under 24 hours and 90% in under 48 hours.

## Checked
Confirmed against the four cited pages on 2026-11-08: Apple guidelines 2.1(a), 2.3.x, 3.1.1, 3.1.3(a) and (e), 4.2, 4.8, 5.1.1; Apple App Review page (40% figure, appeals, expedited, bug fix, appointments, review times); Play "Prepare your app for review" and account deletion articles. Removed as not stated in these pages: Play target API level rule, specific permission names beyond SMS/Call Log, foreground service type declaration, privacy manifest and ITSAppUsesNonExemptEncryption items, Google policy-status appeal path, and the "server-side flags hidden from reviewers" claim.
Method: docs-only read of cited pages, 2026-11-08
