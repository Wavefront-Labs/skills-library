---
id: computing-software.software-engineering.mobile-development.xcconfig-build-settings-and-environments
name: xcconfig-build-settings-and-environments
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, xcconfig, build-settings, build-configurations, schemes, environments, info-plist]
level: practitioner
status: draft
description: "Manage Xcode build settings with .xcconfig files: layered Debug/Release/Staging configurations, per-environment values in Info.plist, and inheritance gotchas."
sources: ["https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project", "https://developer.apple.com/documentation/xcode/build-settings-reference"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# xcconfig files for build settings and environments

Plain-text files that set build settings, diffable and mergeable, unlike the pbxproj.

## Layout
```
Config/Base.xcconfig
Config/Debug.xcconfig      // #include "Base.xcconfig"
Config/Staging.xcconfig
Config/Release.xcconfig
```
```
// Base.xcconfig
SWIFT_VERSION = 5.0
IPHONEOS_DEPLOYMENT_TARGET = 16.0

// Staging.xcconfig
#include "Base.xcconfig"
PRODUCT_BUNDLE_IDENTIFIER = com.example.app.staging
APP_API_HOST = api.staging.example.test
SWIFT_ACTIVE_COMPILATION_CONDITIONS = $(inherited) STAGING
```
Assign each file to a build configuration in Project > Info > Configurations (add a Staging configuration by duplicating Release).

## Use values in code
In Info.plist add `APIHost` = `$(APP_API_HOST)`, then read `Bundle.main.object(forInfoDictionaryKey: "APIHost")`.

## Gotchas
- A URL value containing `//` is read as a comment; write `https:/$()/host` to escape it.
- Always include `$(inherited)` when appending to list-type settings, otherwise you drop inherited values.
- A setting edited directly in the Xcode UI overrides the xcconfig for that target; delete the override (select the row, press Delete) to let the file win.
- CocoaPods generates its own xcconfigs; include them (`#include "Pods/Target Support Files/.../Pods-App.debug.xcconfig"`) or the build breaks.
- Never commit secrets in xcconfig; inject them in CI.

Verify: `xcodebuild -showBuildSettings -scheme App -configuration Staging | grep -E 'PRODUCT_BUNDLE_IDENTIFIER|APP_API_HOST'` prints the staging values.
