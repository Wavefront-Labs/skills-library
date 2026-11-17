---
id: computing-software.software-engineering.mobile-development.mobile-ci-xcode-cloud-and-gradle-play-publisher
name: mobile-ci-xcode-cloud-and-gradle-play-publisher
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-ci, xcode-cloud, gradle-play-publisher, github-actions, macos-runners, code-signing, xcodebuild, android-ci]
level: practitioner
status: draft
description: "Set up mobile CI/CD: Android builds and Play uploads with Gradle Play Publisher, iOS builds on macOS runners or Xcode Cloud, signing secrets and caching."
sources: ["https://github.com/Triple-T/gradle-play-publisher", "https://developer.apple.com/documentation/xcode/xcode-cloud", "https://developer.android.com/studio/build/building-cmdline"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobile CI (Xcode Cloud / macOS runners / Gradle Play Publisher)

**Goal:** every merge builds, tests and (on release branches) uploads signed builds to TestFlight
and Play tracks with no manual steps on a developer laptop.

## Android pipeline (any Linux runner)
```yaml
jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: 17 }
      - uses: gradle/actions/setup-gradle@v4          # Gradle caching
      - run: ./gradlew lint testReleaseUnitTest bundleRelease
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
```
- Signing: decode the upload keystore from a base64 secret at build time; read passwords from env in
  `signingConfigs`. With **Play App Signing**, CI holds only the upload key (resettable in Play Console if lost or leaked).
- Instrumented tests: emulator via `reactivecircus/android-emulator-runner` (enable KVM on Linux
  runners) or Firebase Test Lab (`gcloud firebase test android run`).
- **Gradle Play Publisher** (`com.github.triplet.play`) uploads AABs, release notes and listing:
```kotlin
play {
    serviceAccountCredentials.set(file("play-service-account.json"))
    track.set("internal")                 // internal, alpha, beta, production or a custom track; defaults to internal
    defaultToAppBundles.set(true)
    releaseStatus.set(ReleaseStatus.COMPLETED)   // or DRAFT / HALTED / IN_PROGRESS (userFraction applies to IN_PROGRESS/HALTED)
}
```
  `./gradlew publishBundle` (all variants), `promoteArtifact --from-track internal --promote-track production --user-fraction .1`.
  Release notes in `src/main/play/release-notes/en-US/default.txt`. The service account needs
  release permissions in Play Console (API access).
- Version code from CI build number (monotonic).

## iOS pipeline: macOS runners
```yaml
  ios:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - run: sudo xcode-select -s /Applications/Xcode_16.4.app
      - run: |
          xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 16' \
            -resultBundlePath TestResults.xcresult | xcbeautify
      - run: bundle exec fastlane beta      # match + build_app + upload_to_testflight
```
- Pin the Xcode version explicitly; runner images change defaults.
- Apple-specific details below (fastlane match, API key flags, Xcode Cloud hours and `ci_scripts` names) were not checked against Apple's documentation.
- Signing: fastlane `match` (certificates/profiles in an encrypted git repo or cloud bucket,
  `readonly: true` in CI) or import a .p12 into a temporary keychain. Automatic signing with an App
  Store Connect API key (`-allowProvisioningUpdates -authenticationKeyPath ...`) also works.
- Upload with an **App Store Connect API key** (issuer id, key id, .p8) - no Apple ID 2FA prompts.
- Cache SwiftPM (`~/Library/Developer/Xcode/DerivedData/**/SourcePackages`) and CocoaPods; macOS
  runners are billed at a different rate from Linux (see the CI provider's pricing page), so keep Android/lint jobs on Linux.

## Xcode Cloud
- Apple-hosted CI configured in Xcode/App Store Connect: workflows with start conditions (branch,
  PR, tag), actions (build, test, analyze, archive) and post-actions (TestFlight internal/external,
  notifications).
- Signing is managed automatically (cloud-managed certificates); no secrets to handle.
- Custom scripts: `ci_scripts/ci_post_clone.sh` (install tools, e.g. `brew install swiftlint`),
  `ci_pre_xcodebuild.sh`, `ci_post_xcodebuild.sh`; environment variables like `CI_BUILD_NUMBER`,
  `CI_WORKFLOW`; secrets as secret environment variables.
- Check Apple's Xcode Cloud page for current included compute hours; it is limited for cross-platform or non-Apple steps (no Android).

## Other options
Bitrise, Codemagic (strong for Flutter/React Native), CircleCI macOS, GitLab with macOS runners,
EAS Build for Expo. Self-hosted Mac minis for heavy usage.

## Practices
- PR pipeline: lint, unit tests, a debug build; release pipeline: signed build, upload, tag.
- Archive dSYMs / R8 mapping files and upload to crash reporting in the same job.
- Keep secrets in the CI secret store; rotate when people leave; never commit keystores or .p8 keys.

## Checked
2026-11-01. Gradle Play Publisher settings and tasks confirmed against its README (track default, releaseStatus values, userFraction rule, release-notes path, defaultToAppBundles, publishBundle, promoteArtifact flags). Removed the 25 compute hours figure and the cost multiple. The iOS and Xcode Cloud sections were not checked, so the skill stays draft.
Method: documentation only; no commands were run.

## Verify
- [ ] A tag on main produces a TestFlight build and a Play internal release automatically.
- [ ] CI never prompts for Apple ID or 2FA (API key auth).
- [ ] Mapping files/dSYMs uploaded for every release build.
