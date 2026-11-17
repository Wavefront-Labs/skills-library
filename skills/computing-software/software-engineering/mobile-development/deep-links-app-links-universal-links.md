---
id: computing-software.software-engineering.mobile-development.deep-links-app-links-universal-links
name: deep-links-app-links-universal-links
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, app-lifecycle, deep-links, universal-links, app-links, assetlinks-json, apple-app-site-association, intent-filters, deferred-deep-links, android, ios]
level: practitioner
status: docs-checked
description: "Set up verified Android deep links: App Links vs deep links, Digital Asset Links verification, adb testing, user approval, update latency."
sources: ["https://developer.android.com/training/app-links", "https://developer.android.com/training/app-links/verify-applinks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deep links: Android App Links

**Goal:** a link to your website opens the right screen in the app when installed, without a disambiguation dialog.

## Deep links vs App Links
- Deep links use the intents system to route custom URIs and standard web schemes to your app. They are available on
  all Android versions but are subject to the system disambiguation dialog.
- Android App Links verify deep links to your own website by establishing a trusted association between app and site.
  Once verified, links open your app immediately. Supported on Android 6 and later on devices with Google services.
- Android 15 adds Dynamic App Links, which refine link behaviour without releasing a new app version.

## Auto verification
The system inspects intent filters that contain the action `android.intent.action.VIEW`, the categories
`android.intent.category.BROWSABLE` and `android.intent.category.DEFAULT`, and a data scheme of `http` or `https`. For each
unique host it fetches `https://hostname/.well-known/assetlinks.json` (Digital Asset Links). On Android 11 (API level
30) and lower the app becomes default handler only if a matching file is found for all hosts in the manifest.
Install the app and wait at least 20 seconds for the asynchronous verification.

## Manual verification (Android 12 and later)
The device must be online. Apps targeting Android 12 or higher use the updated process automatically; otherwise run
`adb shell am compat enable 175408749 PACKAGE_NAME`.
```
adb shell pm set-app-links --package PACKAGE_NAME 0 all     # reset state
adb shell pm verify-app-links --re-verify PACKAGE_NAME      # start verification
adb shell pm get-app-links PACKAGE_NAME                     # review results
```
Wait a few minutes before reviewing. A domain passes when its state is `verified`. Other states: `none` (not finished
or nothing recorded), `approved`, `denied`, `migrated`, `restored`, `legacy_failure`, `system_configured`, and error
codes of 1024 or greater (device-specific verifier errors; check the connection and retry).

## Asking the user to associate the app
Only one app at a time can be associated with a domain on a device. Check approval at runtime with
`DomainVerificationManager.getDomainVerificationUserState()` (states `DOMAIN_STATE_VERIFIED`, `DOMAIN_STATE_SELECTED`,
`DOMAIN_STATE_NONE`), or in testing with `adb shell pm get-app-links --user cur PACKAGE_NAME`. Explain why first,
then launch `Settings.ACTION_APP_OPEN_BY_DEFAULT_SETTINGS` with a `package:` URI to open the Open by default screen
where the user turns on Open supported links and selects domains. Third-party link-opening apps that cannot verify a
domain must tell users to associate it manually, and may offer a trampoline to the first-party app (this needs package
visibility into those apps).

## assetlinks.json update latency
- Android 15 (API level 35) and higher: periodic background re-verification; changes can take up to seven days to reach
  all devices.
- Android 14 (API level 34) and lower: no periodic re-verification; updates are normally picked up on app install or
  update.
- To test an update, reinstall the app; server-side caches can still delay delivery for a few hours.

## Verify
- [ ] `pm get-app-links` shows `verified` for every host.

## Checked
2026-11-08. Confirmed against the Android Developers pages App Links overview and Verify Android App Links (current URL `training/app-links/verify-applinks`): link types, Android 15 note, auto-verification rules, manual verification commands, state list, DomainVerificationManager and settings intent, update latency. Removed: iOS Universal Links content (Apple pages not readable), manifest `autoVerify` snippet and assetlinks.json contents (including signing-key advice) and content-type rules (not on the pages read), `am start` test, routing and safety advice, custom-scheme and deferred-link claims, the Firebase Dynamic Links shutdown date.
Method: documentation only; no commands were run.
