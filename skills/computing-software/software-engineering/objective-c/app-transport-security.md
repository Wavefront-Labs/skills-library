---
id: computing-software.software-engineering.objective-c.app-transport-security
name: app-transport-security
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-io, app-transport-security]
level: practitioner
status: draft
description: "Understand ATS defaults requiring HTTPS and modern TLS, and configure exceptions narrowly through Info.plist."
sources:
  - https://developer.apple.com/documentation/foundation
  - https://developer.apple.com/documentation/security
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# App Transport Security
**Goal:** keep network traffic encrypted by default.

- On iOS/macOS apps, ATS blocks cleartext HTTP and requires TLS 1.2 or later with forward-secret cipher suites for connections made through URL loading APIs (NSURLSession and related).
- Exceptions go under `NSAppTransportSecurity` in Info.plist:
```xml
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSExceptionDomains</key>
  <dict><key>legacy.example.com</key>
    <dict><key>NSExceptionAllowsInsecureHTTPLoads</key><true/></dict></dict>
  </dict>
</dict>
```
- `NSAllowsArbitraryLoads` disables ATS globally; avoid it, and App Store review may require justification.
- `NSAllowsLocalNetworking` permits local network connections.
- ATS applies to URL loading; lower-level sockets (CFNetwork streams, BSD sockets, Network framework) are not subject to the same checks.
- Per-domain keys include `NSIncludesSubdomains`, `NSExceptionMinimumTLSVersion`, `NSExceptionRequiresForwardSecrecy`.

## Gotchas
- Plain HTTP localhost development should use a narrow domain exception rather than the global flag.
- Redirects to HTTP are also blocked.

## Self-check
Request an `http://` URL in a debug build and confirm an ATS error (-1022) appears.
