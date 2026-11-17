---
id: computing-software.software-engineering.objective-c.cocoapods-podspec
name: cocoapods-podspec
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-packaging, cocoapods-podspec]
level: practitioner
status: draft
description: "Write a podspec for an Objective-C library, lint it, and consume pods through a Podfile with pod install."
sources:
  - https://guides.cocoapods.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CocoaPods
**Goal:** publish and consume Objective-C libraries with CocoaPods.

```ruby
# ABCKit.podspec
Pod::Spec.new do |s|
  s.name = 'ABCKit'
  s.version = '1.0.0'
  s.summary = 'Short description'
  s.homepage = 'https://example.com/abckit'
  s.license = { :type => 'MIT', :file => 'LICENSE' }
  s.author = { 'Name' => 'dev@example.com' }
  s.source = { :git => 'https://example.com/abckit.git', :tag => s.version.to_s }
  s.ios.deployment_target = '13.0'
  s.source_files = 'Sources/**/*.{h,m}'
  s.public_header_files = 'Sources/Public/*.h'
  s.requires_arc = true
  s.frameworks = 'Foundation'
end
# Podfile
platform :ios, '13.0'
target 'App' do
  use_frameworks!
  pod 'ABCKit', '~> 1.0'
end
```
- Commands: `pod install` (use Podfile.lock), `pod update`, `pod lib lint ABCKit.podspec`, `pod trunk push` to publish.
- Open the generated `.xcworkspace`, not the project.
- Check in `Podfile.lock`; Pods directory is optional.
- `use_frameworks! :linkage => :static` selects static frameworks (verify option in the current Podfile docs).

## Gotchas
- Check CocoaPods' current maintenance and trunk status before adopting it for a new project (unconfirmed; SwiftPM is the default for new work).
- Mixing static libs and frameworks needs correct header paths.

## Self-check
Run `pod lib lint` and fix every warning.
