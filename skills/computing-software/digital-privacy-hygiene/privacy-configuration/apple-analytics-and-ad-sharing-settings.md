---
id: computing-software.digital-privacy-hygiene.privacy-configuration.apple-analytics-and-ad-sharing-settings
name: apple-analytics-and-ad-sharing-settings
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, apple-analytics-sharing, apple, ios, macos, personalized-ads, siri, analytics]
level: intro
status: docs-checked
description: "Turn off optional data sharing on iPhone and Mac: device analytics, Apple personalised ads, Improve Siri recordings and Safari ad measurement, using Apple's own pages."
sources:
  - "https://www.apple.com/legal/privacy/data/en/device-analytics/"
  - "https://www.apple.com/legal/privacy/data/en/apple-advertising/"
  - "https://www.apple.com/legal/privacy/data/en/ask-siri-dictation/"
  - "https://support.apple.com/en-us/102420"
  - "https://ssd.eff.org/module/how-to-get-to-know-iphone-privacy-and-security-settings"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apple analytics and ad sharing settings

**Goal:** stop the optional diagnostics and advertising data Apple devices send. Paths follow Apple's pages and the
EFF guide (written for iOS 26); labels vary by OS version.

## iPhone / iPad
- **Device analytics:** Settings > Privacy & Security > **Analytics & Improvements** > turn off **Share iPhone
  Analytics** (**Share iPhone & Watch Analytics** if a Watch is paired). **Analytics Data** on the same screen shows
  what is collected. Apple says the data does not identify you personally, and that with Location Services on, device
  location may also be sent for performance analysis.
- **Analytics location:** Settings > Privacy & Security > Location Services > System Services > turn off **iPhone
  Analytics**.
- **Siri recordings:** same Analytics & Improvements screen > turn off **Improve Siri & Dictation** (or **Improve
  Siri & Apple Intelligence**). Audio is not stored by Apple unless you opt in.
- **Apple personalised ads:** Settings > Privacy & Security > **Apple Advertising** > Personalized Ads off. This
  covers App Store, Apple News and Stocks; Apple Maps shows contextual ads only. Apple notes it may not reduce the
  number of ads. **View Ad Targeting Information** on the same screen shows your segments.
- **Siri on-device history:** Settings > Siri > Turn Off Siri deletes the stored Siri and Dictation transcripts on
  the device; Settings > Siri > Excluded Apps stops Siri using an app's information.
- **Safari ad measurement:** Settings > Apps > Safari > Advanced > turn off **Privacy Preserving Ad Measurement**
  (EFF).

## Mac
System Settings > Privacy & Security > **Apple Advertising** > deselect Personalized Ads; **View Ad Targeting
Information** is in the same place. Location-based ads: turn off Location Services or the app permission for News or TV.

## Third-party tracking
Separate from the above: Settings > Privacy & Security > **Tracking** > Allow Apps to Request to Track off (iPhone,
iPad; Apple TV under Settings > General > Privacy & Security). Apps that ask are then treated as Ask App Not to Track.

## Gotchas
- Personalized Ads may be unavailable on minors' accounts, managed accounts, or where Apple does not serve ads.
- These toggles do not stop contextual ads or the data apps collect themselves.

## Verify
- [ ] Analytics and Improve Siri off, Personalized Ads off.

## Checked
Checked 2026-11-08 against the full text of Apple's "Device Analytics & Privacy", "Apple Advertising & Privacy" and
"Siri, Dictation & Privacy" pages, Apple Support 102420, and the EFF iPhone settings guide. Removed what none of
them state: Share iCloud Analytics, Health Records, Wheelchair Mode, Fitness+ and AssistiveTouch toggles, the claim
that analytics also go to app developers, "Share Mac Analytics" and the Mac and Apple TV analytics paths, "Watch
follows the iPhone toggle", and that updates re-enable sharing. The apple.com/legal/privacy page is a stub and the
iPhone guide link a contents page, so both were dropped from sources.
Method: documentation only; no commands were run.
