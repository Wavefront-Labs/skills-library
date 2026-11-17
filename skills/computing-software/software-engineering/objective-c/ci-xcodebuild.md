---
id: computing-software.software-engineering.objective-c.ci-xcodebuild
name: ci-xcodebuild
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-ops, ci-xcodebuild]
level: practitioner
status: draft
description: "Build and test Objective-C projects in CI on macOS runners using xcodebuild, caching, simulators and result bundles."
sources:
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CI with xcodebuild
**Goal:** repeatable builds on hosted macOS runners.

```yaml
# .github/workflows/ci.yml (example)
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.4.app     # version must exist on the runner image
      - name: Build and test
        run: |
          set -o pipefail
          xcodebuild test -workspace App.xcworkspace -scheme App \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            -resultBundlePath build/R.xcresult CODE_SIGNING_ALLOWED=NO | xcpretty
      - uses: actions/upload-artifact@v4
        with: { name: results, path: build/R.xcresult }
```
- Pin the Xcode version and simulator device explicitly; runner images change.
- Cache Pods/SwiftPM (`~/Library/Caches/org.swift.swiftpm`, `Pods/`) keyed on lock files.
- Run lint and analyzer jobs separately: `clang-format --dry-run --Werror`, `xcodebuild analyze`.
- Upload `.xcresult` bundles for failure diagnosis.
- Keep signing secrets in CI secret storage; import certificates into a temporary keychain.
- Alternatives: Xcode Cloud, fastlane lanes, Bitrise, Jenkins on Mac hardware.

## Gotchas
- macOS runners are slower and costlier than Linux; run Linux GNUstep builds for portable code.
- Simulators need a boot wait or `xcrun simctl bootstatus`.

## Self-check
Run the workflow on a branch and confirm the test results artifact is uploaded.
