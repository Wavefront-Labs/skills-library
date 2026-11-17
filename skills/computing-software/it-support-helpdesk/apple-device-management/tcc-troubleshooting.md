---
id: computing-software.it-support-helpdesk.apple-device-management.tcc-troubleshooting
name: tcc-troubleshooting
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, pppc-tcc, tcc-troubleshooting, tcc, privacy-permissions]
level: practitioner
status: docs-checked
description: "Diagnose macOS privacy prompts that persist after a PPPC profile: find the responsible binary in the TCC log and check identifier, code requirement and Allow/Deny logic."
sources:
  - "https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.TCC.configuration-profile-policy.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tcc-troubleshooting

Goal: understand why an app still prompts for, or lacks, a privacy permission after a PPPC profile.
- Find the responsible process in real time: `log stream --debug --predicate 'subsystem == "com.apple.TCC" AND eventMessage BEGINSWITH "AttributionChain"'` (Apple's own suggestion when prompts continue after deploying a custom payload).
- Check the entry: `Identifier` is case-sensitive; `IdentifierType` must be `bundleID` for app bundles and `path` for nonbundled binaries; `CodeRequirement` must be everything after `designated =>` from `codesign -dr - /path/to/Application.app`.
- Check `Allowed` versus `Authorization`: an entry needs one, not both. With several payloads the most restrictive setting (deny) wins, so look for another profile that denies the same service.
- Camera, microphone, `ListenEvent` and `ScreenCapture` can only be denied by a profile, never granted, so a prompt there is expected; `AllowStandardUserToSetSystemService` lets a standard user set `ListenEvent` and `ScreenCapture` in Privacy preferences.
- Helper tools embedded in an app bundle inherit the app's permissions; a different helper binary outside it needs its own entry.
- The payload needs a device management service to install it (Device Enrolment or Automated Device Enrolment) and is not available on macOS User Enrolment.
Practice: collect the bundle ID, the installed profile list and the log extract before escalating to the vendor, because each device management service presents PPPC settings differently.
Verify: the `log stream` output names the process (attribution chain) that your `Identifier` and `CodeRequirement` must match.

## Checked

Date: 2026-11-07. Read in full: Apple's PPPC payload page (custom payload requirements table, the log stream command, vendor-implementation note) and the apple/device-management TCC YAML (lines 1 to 260: the Identity keys, deny-only services, Allowed/Authorization rule). Removed: `tccutil reset`, `log show --last 10m`, the user/system TCC database paths, the SIP statement and the "reproduce on a clean user account" advice, none of which the pages state.
Method: documentation only; no commands were run.
