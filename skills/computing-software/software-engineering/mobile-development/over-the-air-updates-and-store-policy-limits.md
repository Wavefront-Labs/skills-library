---
id: computing-software.software-engineering.mobile-development.over-the-air-updates-and-store-policy-limits
name: over-the-air-updates-and-store-policy-limits
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ota-updates, expo-updates, eas-update, codepush, shorebird, runtime-version, app-store-guidelines, hot-fixes]
level: advanced
status: docs-checked
description: "Ship over-the-air JS updates with Expo Update within Apple and Google Play rules: runtime versions, channels, rollouts and rollback, plus what Shorebird offers Flutter."
sources: ["https://docs.expo.dev/eas-update/introduction/", "https://docs.expo.dev/eas-update/runtime-versions/", "https://docs.shorebird.dev/", "https://developer.apple.com/app-store/review/guidelines/#software-requirements", "https://support.google.com/googleplay/android-developer/answer/9888379"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Over-the-air updates and store policy limits

**Goal:** fix bugs and tweak behaviour without a full store review, while staying inside the store
rules and never sending an update that is incompatible with the installed native code.

## What policy says
- **Apple App Review Guideline 2.5.2**: "Apps should be self-contained in their bundles, and may not
  read or write data outside the designated container area, nor may they download, install, or
  execute code which introduces or changes features or functionality of the app, including other
  apps." Educational apps for teaching or testing executable code may, in limited circumstances,
  download code if it is not used for other purposes and its source is viewable and editable by the
  user. Read the guideline itself; whether an interpreted-JavaScript update qualifies is not spelled
  out in this text, so treat anything that changes features as needing review.
- **Google Play** (the page checked is the Play policy on device and network abuse): "an app may
  not download executable code (such as dex, JAR, .so files) from a source other than Google Play".
  The restriction "does not apply to code that runs in a virtual machine or an interpreter where
  either provides indirect access to Android APIs (such as JavaScript in a webview or browser)".
  Interpreted code loaded at run time "must not allow potential violations of Google Play
  policies".
- **Expo's own guidance**: updates must follow the App Store and Play Store guidelines, "including
  the content of the updates and how you use them. This usually means changes to your app's
  behavior need to be reviewed."

## Expo Update: what OTA may carry
Expo Update enables an app to update "non-native pieces (such as JS, styling, and images)". The
docs' table recommends it for fixing JavaScript bugs, updating copy, translations, UI styling or
layouts, percentage rollouts, CI publishing and internal testing. A new app binary is required for
native code or native dependency changes, changes to app permissions (camera, location, and
others), Expo SDK version updates, and anything else that requires a new binary.

## Runtime versions: the compatibility contract
"Runtime versions are a property that guarantees compatibility between a build's native code and an
update." Updates are sent only to builds with compatible native code, so any native change needs a
new build and runtime version.
```json
{ "expo": { "runtimeVersion": { "policy": "fingerprint" } } }
```
- `appVersion` policy: the runtime version increments with the app version; if you forget to bump
  the app version after a native change you get a runtime version mismatch.
- `fingerprint` policy: increments whenever anything that may impact the native runtime changes;
  makes incompatible updates extremely unlikely at the cost of creating builds more often.
- A custom string (`"runtimeVersion": "1.0.0"`) gives full manual control; a platform-specific value
  (for example under `android`) takes precedence over the top-level one.
- If an update calls native code the build lacks, `expo-updates` "may detect an error and attempt
  to roll back to the previously working update".

## Expo Update workflow
```bash
npx expo install expo-updates
eas update:configure
eas update --channel production --message "Fix login button alignment"
```
- A new build is needed to include `expo-updates`; after that the publish command sends the bundle
  and assets "so users receive the new version on their next app launch". By default
  `expo-updates` checks for updates every time the app is loaded; a custom strategy uses the Updates
  API (`useUpdates()`, `checkForUpdateAsync()`, `fetchUpdateAsync()`) and app config.
- Rollback: republish a previous stable version on top of the problematic one, like a new commit.
- Rollouts publish an update to a small percentage of users; monitor the update's error rate on the
  Expo dashboard, cancel the rollout if errors are high, or roll back if fully rolled out.
- Preview: create a preview build with the same runtime version pointing at a different channel
  and test updates there before production, or use channel surfing for chosen users.
- The docs say existing React Native projects with `expo-updates` installed work too; pricing is
  per monthly active user, so see Expo's pricing page for current figures.
- Classic Updates (before December 2021) are deprecated and `expo publish` cannot publish new ones.

## Flutter: Shorebird
Shorebird "lets you push code updates to your Flutter app instantly, without waiting for app store
review". Its docs have a Code Push section and an "App store guidelines" page on how code push
works within the Play Store and App Store rules (not read for this skill); read it before relying on
it.

## Safety practices
- Staged rollout with error monitoring, and a known rollback path (republish).
- Test the incompatible-update recovery path, since automatic rollback is described as something
  `expo-updates` "may" attempt.
- Do not use OTA to change what App Review approved: Apple 2.5.2 and Expo's guidance both tie
  feature changes to review.

## Verify
- [ ] The runtime version policy changes when native code changes (`fingerprint`), or a manual bump
      is part of the release checklist.
- [ ] An update installs on a build with the matching runtime version and is not sent to others.
- [ ] Rollback was practised, and rollout error rates are watched on the dashboard.

## Checked
2026-11-08. Confirmed against the Expo Update introduction and Runtime versions pages, the Apple App
Review Guidelines (section 2.5.2), the Google Play executable-code policy text and the Shorebird
docs landing page. Removed because the pages do not state them: the earlier paraphrase of Apple's
rule (it claimed interpreted code is allowed and cited the Developer Program License Agreement),
`--rollout-percentage` and `update:rollback` flags and commands, channel-to-branch mapping,
update code signing, the CodePush retirement date, Shorebird commands, privacy and CI-embedding
advice.
Method: documentation only; no commands were run.
