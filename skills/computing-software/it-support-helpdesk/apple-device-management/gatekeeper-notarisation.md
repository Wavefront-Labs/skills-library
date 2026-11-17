---
id: computing-software.it-support-helpdesk.apple-device-management.gatekeeper-notarisation
name: gatekeeper-notarisation
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, gatekeeper, gatekeeper-notarisation, notarisation]
level: practitioner
status: docs-checked
description: "Explain Gatekeeper policy, notarisation and Developer ID signing, set Gatekeeper with the System Policy Control payload and diagnose blocked app launches on managed Macs."
sources:
  - "https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web"
  - "https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution"
  - "https://developer.apple.com/documentation/security/customizing-the-notarization-workflow"
  - "https://developer.apple.com/documentation/security/resolving-common-notarization-issues"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.systempolicy.control.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gatekeeper-notarisation

Goal: understand why a downloaded app is blocked on a Mac and what policy you control.
- Gatekeeper checks that downloaded software comes from an identified developer, is notarised by Apple and has not been altered. By default it allows software signed by the App Store, or by a registered developer and notarised. Organisations can allow only App Store software; users can override Gatekeeper unless device management restricts it.
- Set policy with the System Policy Control payload `com.apple.systempolicy.control` (macOS 10.8 or later, device channel, not allowed for User Enrolment). `EnableAssessment` true enables Gatekeeper, false disables it. `AllowIdentifiedDevelopers` true allows "Mac App Store and identified developers", false allows the Mac App Store only; it has no effect unless `EnableAssessment` is true. `EnableXProtectMalwareUpload` (macOS 15.0 or later) set to false stops the prompt to upload blocked malware to Apple.
- Inspect a blocked app: `codesign -dvv /path/to/App.app` shows signing details (a `Timestamp` value means a secure timestamp; `Signed Time` instead means none). `codesign -vvv --deep --strict /path/to/App.app` verifies the signature to the strictness notarisation needs. `spctl -vvv --assess --type exec /path/to/App.app` shows whether the app runs under the system policy now in effect.
- Notarisation: software distributed outside the Mac App Store is signed with a Developer ID certificate (not Mac Distribution, ad hoc or development certificates), uses the hardened runtime and a secure timestamp, and is uploaded to the Apple notary service, which returns a ticket. Gatekeeper finds the ticket online or attached to the software.
- Upload with `xcrun notarytool submit file.zip --keychain-profile "profile-name" --wait`; save credentials once with `xcrun notarytool store-credentials "profile-name"`; read a failure with `xcrun notarytool log <submission-id> --keychain-profile "profile-name" developer_log.json`. `altool` uploads have not been accepted since 1 November 2023.
- Attach the ticket with `xcrun stapler staple "App.app"` so Gatekeeper passes the check offline. You cannot staple a ZIP: staple each item, then rebuild the ZIP. Tickets exist for standalone binaries but cannot be stapled to them.
- Since macOS 10.14.5, software signed with a new Developer ID certificate and all new or updated kernel extensions must be notarised to run; since macOS 10.15, software built after 1 June 2019 and distributed with Developer ID must be notarised. Mac App Store software is exempt.
Practice: prefer a notarised build from the vendor. For internal apps, keep the signing certificate and notarytool credentials in a protected build pipeline, and staple tickets.
Gotcha: a Mac App Store only policy blocks identified-developer apps that would otherwise pass; check the payload before re-signing anything.
Verify: `spctl -vvv --assess --type exec /path/to/App.app` accepts the app under the policy you deployed.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Security "Gatekeeper and runtime protection in macOS" (sec5599; Gatekeeper behaviour, App Store only option); the apple/device-management YAML for `com.apple.systempolicy.control` (payload keys, OS minimums, channel); the three developer.apple.com notarisation articles (notarising before distribution, customising the workflow, resolving common issues), read as the JSON documentation data behind those pages because the HTML pages need JavaScript.
- Confirmed: all payload keys and OS minimums above; `codesign -dvv`, `codesign -vvv --deep --strict`, `spctl -vvv --assess --type exec`, `notarytool submit/store-credentials/log`, `stapler staple`, ZIP/standalone staple limits, altool cut-off and the 10.14.5 / 10.15 notarisation rules.
- Removed as unconfirmed or wrong: `stapler validate`, `spctl --status`, the claim that the payload is a restrictions payload (it is its own payload), reusing vendor Team IDs in PPPC profiles, and the quarantine-flag gotcha.
