---
id: computing-software.digital-privacy-hygiene.privacy-configuration.account-privacy-and-tracking-review
name: account-privacy-and-tracking-review
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, privacy-settings, google-my-activity, auto-delete, google-ad-settings, apple-privacy, app-tracking-transparency, location-services, precise-location, mail-privacy-protection, microsoft-privacy-dashboard, facebook-privacy, off-facebook-activity, meta-accounts-center, advertising-id, data-brokers, people-search-opt-out, email-aliases, simplelogin, hide-my-email, firefox-relay, data-download, gdpr, ccpa, subject-access-request, privacy-checkup]
level: intro
status: draft
description: "Review Google, Apple, Microsoft and Meta privacy settings, cut ad tracking and location sharing, opt out of data brokers, use email aliases and request your data."
sources:
  - "https://myactivity.google.com/"
  - "https://myadcenter.google.com/"
  - "https://account.microsoft.com/privacy"
  - "https://privacy.apple.com/"
  - "https://takeout.google.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Account privacy and tracking review

**Goal:** in about an hour, reduce what the big platforms collect and keep, stop
cross-app ad tracking and needless location sharing, and limit how far your details
spread — then repeat briefly on a schedule. Menu paths change often; where a label
doesn't match, search the settings for the key word.

## 1. Google
- **myactivity.google.com** › Web & App Activity and YouTube History › **Auto-delete**
  › 3 months (options are 3, 18 or 36 months). Turn activity off entirely if you
  don't value the personalisation.
- Timeline (location history) is now stored on the device on most phones; check
  it is off or on auto-delete if you don't use it.
- **myadcenter.google.com**: turn off personalised ads or prune topics.
- Run **Privacy Checkup** (myaccount.google.com › Data & privacy).
- "Results about you" lets you request removal of your phone/address from Search
  results (availability varies by country).

## 2. Apple
- Settings › Privacy & Security › **Tracking** › turn off "Allow Apps to Request to
  Track" — apps are then refused without asking (App Tracking Transparency).
- Privacy & Security › **Location Services**: set each app to *While Using* or
  *Never*, and switch **Precise Location** off for apps that only need your town.
  Check System Services › Significant Locations.
- **Mail Privacy Protection**: Settings › Apps › Mail › Privacy Protection › Protect
  Mail Activity (older iOS: Settings › Mail) — blocks tracking pixels and hides your IP.
- Settings › Privacy & Security › Apple Advertising › Personalised Ads off.

## 3. Microsoft
- **account.microsoft.com/privacy**: clear browsing, search, location and Copilot or
  assistant history you don't want kept.
- Windows: Settings › Privacy & security › General (turn off advertising ID, app
  launch tracking), Diagnostics & feedback (Required only; Tailored experiences off),
  and review Location.

## 4. Meta (Facebook, Instagram)
- Accounts Center › Your information and permissions › **Your activity off Meta
  technologies** (formerly Off-Facebook Activity) › clear previous activity and
  **disconnect future activity**.
- Accounts Center › Ad preferences: review ad topics and partner data.
- Facebook Settings › Audience and visibility: default post audience to Friends,
  **Limit past posts**, and restrict who can look you up by email/phone.
- Run Privacy Checkup on each Meta app.

## 5. Phone-wide
- **Advertising ID**: Android Settings › Privacy (or Security & privacy) › Ads ›
  **Delete advertising ID** (Android 12+). iOS has no reset; ATT covers it.
- **Location**: grant "Only while using the app" and **Approximate** location wherever
  offered; deny background location unless it's a navigation or family-safety app.
- Review Bluetooth/nearby devices and contacts permissions — common data grabs.

## 6. Data brokers and people-search sites
Search your name plus city; for each people-search result, use the site's own
opt-out page (expect email confirmation, and re-listings months later). Paid removal
services automate this. In California, the state's Delete Act platform (DROP) lets
residents send one deletion request to all registered brokers — I'm not fully sure
of its current rollout status; check the California privacy agency's site. EU/UK
residents can send erasure requests under GDPR.

## 7. Email aliases
Use a unique forwarding alias per site — **SimpleLogin**, Apple **Hide My Email**
(iCloud+), **Firefox Relay**, DuckDuckGo Email Protection or addy.io — so leaks are
traceable, spam can be cut by disabling one alias, and breach lists can't link your
accounts. Keep the alias service's account protected with MFA: it is now a recovery path.

## 8. Download what they hold
Google Takeout, privacy.apple.com, Meta "Download your information", Microsoft privacy
dashboard. Under GDPR (EU/UK) a subject access request must be answered within one
month; under CCPA/CPRA (California) generally 45 days. Other regions vary.

## Gotchas
- Turning off "personalised ads" changes targeting, not necessarily collection.
- Deleting history can degrade recommendations and some assistant features — expected.
- Major OS or app updates sometimes add new toggles defaulted on; re-check after them.

## Cadence
Quarterly 15-minute pass over sections 1–5; data-broker search every six months;
a full review yearly or after a new phone.

## Verify
- [ ] Google auto-delete set; ad personalisation reviewed.
- [ ] iOS "Allow Apps to Request to Track" off / Android ad ID deleted.
- [ ] No app has background or precise location without a reason.
- [ ] Meta off-platform activity disconnected; default audience not Public.
- [ ] New sign-ups use an email alias.
- [ ] Next review date is in your calendar.
