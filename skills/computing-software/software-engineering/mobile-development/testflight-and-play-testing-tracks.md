---
id: computing-software.software-engineering.mobile-development.testflight-and-play-testing-tracks
name: testflight-and-play-testing-tracks
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-release, testflight, play-testing-tracks, beta-testing, internal-testing, firebase-app-distribution]
level: practitioner
status: docs-checked
description: "Run mobile beta programs: TestFlight internal/external groups and first-build review, Play internal/closed/open tracks, promoting builds, and collecting feedback."
sources:
  - https://developer.apple.com/testflight/
  - https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview
  - https://support.google.com/googleplay/android-developer/answer/9845334
  - https://firebase.google.com/docs/app-distribution
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# TestFlight and Play testing tracks

**Goal:** every release candidate reaches testers quickly through the same pipeline that ships to production, and the binary that passed testing is the one promoted.

## 1. TestFlight
- Provide test information first: beta app description, what to test, and an email address for feedback.
- **Internal testers**: up to 100 App Store Connect users with access to your content.
- **External testers**: up to 10,000, by email invitation or public link (criteria on a public link can limit the number). The first build added to a group is sent to App Review; review is required only for the first build, and later builds may not need a full review. Testing starts once approved.
- A build can be tested for up to 90 days; you can expire it earlier. If you do not expire a build and it goes live, invited testers can still test it. Builds must include application identifiers in their provisioning profiles; check export compliance (encryption) requirements when uploading.
- Feedback: testers on TestFlight 2.3 or later on iOS, macOS and visionOS can send feedback from the TestFlight app or by screenshot inside the beta app; it appears in the TestFlight Feedback section of App Store Connect. App Store Connect also shows sessions and crashes per build. tvOS and older iOS send feedback to your email address.
- Upload to App Store Connect (see the fastlane skill for `upload_to_testflight`).

## 2. Google Play tracks
| Track | Audience | Notes |
|---|---|---|
| Internal testing | up to 100 testers by email list | Fastest; a new AAB is available within minutes; may skip standard policy and security reviews; can start before app setup is complete |
| Closed testing | email lists (up to 200 lists, 2,000 users each, 50 lists per track) or Google Groups; more than one closed track | Only your test group receives closed versions |
| Open testing | anyone; app visible on Google Play, link shareable | One open test at a time; tester count unlimited by default or capped (cap must be at least 1,000); users can send private feedback |
| Production | everyone | - |
Google recommends starting with an internal test, then a small closed group, and you must test before releasing to production. Developers with personal accounts created after 13 November 2023 must meet specific testing requirements before they can publish; check the Play Console testing requirements article. After first publishing a test, the link can take several hours to become available. A user opted in to the internal test must opt out before joining an open or closed test. Testers need a Google Account; paid apps must be purchased for open and closed tests but are free in internal tests.
Promote the same release through the tracks rather than rebuilding between stages.

## 3. Quick ad hoc distribution
Firebase App Distribution takes APK, AAB or IPA uploads (Firebase console, fastlane, Gradle or CLI), sends tester email invitations, supports in-app feedback, and integrates with Google Play internal app sharing and Crashlytics stability data. Use it for QA builds of feature branches; it does not replace TestFlight or the Play tracks before release.

## 4. Pipeline
```
merge to main -> CI builds signed release -> upload to TestFlight internal + Play internal
  -> QA sign-off -> external/closed group -> release candidate -> submit for review -> staged rollout
```
Tag the commit that produced the build; derive build numbers from CI.

## Gotchas
- Play changes (new tests and edits) can take several hours to reach testers.
- Feedback from Play test users does not affect the public rating.
- Debug-only code must be stripped from release-configured beta builds; testers should test release builds.

## Verify
- A merged change appears in TestFlight internal and the Play internal track automatically, and the build promoted to production has the same version/build number as the one QA approved.

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against the Apple TestFlight Overview, the Play Console "Set up an open, closed, or internal test" help page and the Firebase App Distribution overview. Removed unconfirmed claims: `xcrun altool` upload, `supply --track` command line, "no review" for TestFlight internal builds, open-track review, Play membership caching, and the TestFlight contact-email submission-block gotcha.
