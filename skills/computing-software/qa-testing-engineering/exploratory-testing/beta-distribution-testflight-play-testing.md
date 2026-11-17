---
id: computing-software.qa-testing-engineering.exploratory-testing.beta-distribution-testflight-play-testing
name: beta-distribution-testflight-play-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [testflight, play-internal-testing, beta-testing, app-distribution, mobile-testing]
level: practitioner
status: draft
description: "Distribute mobile builds for testing with TestFlight and Google Play internal, closed and open testing tracks: setup, testers, feedback collection and promotion."
sources:
  - https://developer.apple.com/testflight/
  - https://support.google.com/googleplay/android-developer/answer/9845334
  - https://www.istqb.org/certifications/mobile-application-testing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Beta distribution (TestFlight, Play internal testing)

**Goal:** get the exact store-signed build into testers' hands quickly, collect feedback, and promote the tested build without rebuilding.

## Apple TestFlight
- Upload via Xcode Organizer, `xcrun altool`/Transporter or fastlane `pilot`.
- **Internal testers:** up to 100 App Store Connect users; builds available after processing, no review.
- **External testers:** up to 10,000 by email or public link; the first build of a version needs Beta App Review.
- Builds expire after 90 days. Testers send feedback with screenshots from the TestFlight app; read it in App Store Connect > TestFlight > Feedback, crashes appear too.
- Add "What to Test" notes per build so testers focus on changes.

## Google Play testing tracks
- **Internal testing:** up to 100 testers, available within minutes, good for QA every build.
- **Closed testing:** email lists or Google Groups; new personal developer accounts must run a closed test with a minimum number of testers for a period before production access.
- **Open testing:** anyone can join from the store listing.
- Upload with Play Console, fastlane `supply`, or the Play Developer API; promote a release from internal to closed to production without re-uploading.
- **Internal app sharing** for quick ad hoc builds to testers (different signing considerations).

## Practice
- Test the store-distributed build, not only debug builds: signing, ProGuard/R8, entitlements and in-app purchase config differ.
- Use CI (fastlane lanes, Xcode Cloud, Bitrise) to publish each merge to internal tracks with build number and changelog.
- Track which build each tester used in bug reports.

## Verify
Every release candidate is installed by QA from TestFlight/Play internal, feedback is collected in one place, and the production release is a promotion of that same build.
