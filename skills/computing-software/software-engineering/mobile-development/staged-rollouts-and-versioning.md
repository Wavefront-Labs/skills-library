---
id: computing-software.software-engineering.mobile-development.staged-rollouts-and-versioning
name: staged-rollouts-and-versioning
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-release, staged-rollout, phased-release, versioning, version-code, build-numbers, forced-update, release-train]
level: practitioner
status: draft
description: "Ship mobile releases safely: Play staged rollouts and halts, App Store phased release, version and build numbering, minimum-version enforcement and release trains."
sources:
  - https://support.google.com/googleplay/android-developer/answer/6346149
  - https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases
  - https://developer.android.com/guide/playcore/in-app-updates
  - https://semver.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Staged and phased rollouts and versioning

**Goal:** a bad release reaches a small percentage of users and is stopped quickly, because mobile releases cannot be rolled back.

## 1. Why mobile is different
Users keep old versions for months; you cannot pull a binary back from devices. Mitigations: gradual rollout, server-side feature flags (kill switches), backward-compatible APIs, and minimum-version enforcement.

## 2. Google Play staged rollout
- Release to production with a percentage (1%, 5%, 20%, 50%, 100%), increase manually or via API (`fastlane supply --rollout 0.05`).
- **Halt** a rollout from Play Console if crash rate spikes; users who got it keep it. Fix by releasing a higher `versionCode` (you cannot re-release a lower version to users who updated).
- Watch Android vitals (crash rate, ANR rate) per version; Play's bad-behaviour thresholds (1.09% user-perceived crash rate, 0.47% ANR) affect store visibility.

## 3. App Store phased release
- Automatic 7-day schedule for **automatic updates**: 1%, 2%, 5%, 10%, 20%, 50%, 100%. Users can still manually update from the store at any time.
- Pause for up to 30 days total; resume or release to all.
- A bad build cannot be removed for users who updated: submit a fix (expedited review if critical), and use remote config to disable the broken feature now.

## 4. Version and build numbers
- Marketing version: `MAJOR.MINOR.PATCH` (iOS `CFBundleShortVersionString`, Android `versionName`).
- Build number: monotonic integer from CI (iOS `CFBundleVersion` per version; Android `versionCode` globally increasing; common scheme `major*1_000_000 + minor*10_000 + patch*100 + build`, or simply the CI build number).
- Tag the release commit `v4.12.0`; changelog/release notes from commits.
- Limits and tooling: Play rejects an upload whose `versionCode` is not higher than every previously uploaded one (any track) and caps it at 2100000000; App Store Connect requires `CFBundleVersion` to increase within a marketing version. Set both from CI (`agvtool new-version -all $BUILD` or fastlane `increment_build_number`; Gradle `versionCode = System.getenv("BUILD_NUMBER").toInt()`), never by hand.

## 5. Minimum-version enforcement
- Backend returns `minSupportedVersion` (per platform) in a config endpoint; app shows a blocking "please update" screen below it, and a soft prompt below `recommendedVersion`.
- Android in-app updates API: immediate (blocking) or flexible (background download) flows via Play.
- APIs must support at least N previous app versions; version your endpoints and never break old clients without enforcing an update first.

## 6. Release trains
Fixed cadence (e.g. weekly or biweekly): branch cut, stabilisation on beta tracks, submit, phased rollout. Features miss the train if not ready (behind flags) rather than delaying it.

## Gotchas
- Shipping a new required API field and an app version that depends on it the same day breaks old clients still on the store cache; deploy backend first.
- Phased release only affects automatic updates; new installs always get the latest version.
- Hotfix numbering: keep build numbers increasing across branches to avoid upload rejections.

## Verify
- Dashboards show crash-free rate per version during rollout, a documented halt/pause runbook exists, and the minimum-version gate is tested by pointing a dev build at a config with a higher minimum.
