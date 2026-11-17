---
id: computing-software.software-engineering.objective-c.fastlane-lanes
name: fastlane-lanes
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-ops, fastlane-lanes]
level: practitioner
status: draft
description: "Automate test, build and distribution with fastlane lanes using run_tests, build_app, match and upload_to_testflight."
sources:
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# fastlane
**Goal:** scripted iOS/macOS release steps.

```ruby
# fastlane/Fastfile
default_platform(:ios)
platform :ios do
  lane :test do
    run_tests(scheme: "App", devices: ["iPhone 15"])      # alias: scan
  end
  lane :beta do
    match(type: "appstore", readonly: true)
    increment_build_number(xcodeproj: "App.xcodeproj")
    build_app(scheme: "App")                               # alias: gym
    upload_to_testflight                                   # alias: pilot
  end
end
```
- Run: `bundle exec fastlane test`, `bundle exec fastlane beta`; pin versions with a `Gemfile`.
- `match` syncs certificates and profiles via a private git repo or cloud storage.
- Authentication for App Store Connect uses an API key (`app_store_connect_api_key`) preferred over passwords.
- Environment-specific values live in `.env` files (not committed with secrets) or CI secrets.
- `fastlane init` scaffolds the folder; `fastlane lanes` lists lanes.

## Gotchas
- Action names and options change between fastlane releases; check `fastlane action <name>`.
- Interactive prompts hang CI; set `FASTLANE_SKIP_UPDATE_CHECK=1` and avoid two-factor flows via API keys.

## Self-check
Run `bundle exec fastlane lanes` to list lanes, then run the test lane locally.
