---
id: computing-software.software-engineering.objective-c.xcodebuild
name: xcodebuild
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-build, xcodebuild]
level: practitioner
status: draft
description: "Drive Xcode builds from the command line: list schemes, build, test on simulators, archive and export with xcodebuild."
sources:
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# xcodebuild
**Goal:** reproducible command-line builds.

```bash
xcodebuild -list -workspace App.xcworkspace
xcodebuild -workspace App.xcworkspace -scheme App -configuration Debug \
  -destination 'platform=iOS Simulator,name=iPhone 15' build
xcodebuild -workspace App.xcworkspace -scheme AppTests \
  -destination 'platform=iOS Simulator,name=iPhone 15' -resultBundlePath build/Tests.xcresult test
xcodebuild -scheme App -configuration Release archive -archivePath build/App.xcarchive
xcodebuild -exportArchive -archivePath build/App.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath build/out
xcodebuild -showBuildSettings -scheme App
```
- Use `-project X.xcodeproj` or `-workspace X.xcworkspace` (required with CocoaPods) plus `-scheme`.
- `-destination` selects device/simulator; list with `xcrun simctl list devices`. Simulator names must exist on the machine.
- `-derivedDataPath <dir>` isolates build output; `clean` removes products.
- `-enableCodeCoverage YES` for coverage; `-only-testing:Target/Class/method` to run a subset.
- Pipe through `xcpretty` for readable output if installed, and `set -o pipefail` so failures propagate.
- Code signing flags: `CODE_SIGN_IDENTITY=""`, `CODE_SIGNING_ALLOWED=NO` for unsigned simulator builds.

## Gotchas
- Scheme must be shared (checked into `xcshareddata`) to be visible on CI.
- Device names change with Xcode versions; query before hardcoding.

## Self-check
Run `xcodebuild -list` on a clean clone and confirm the scheme appears.
