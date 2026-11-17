---
id: computing-software.it-support-helpdesk.apple-device-management.pppc-payload
name: pppc-payload
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, pppc-tcc, pppc-payload, pppc, privacy-payload]
level: practitioner
status: docs-checked
description: "Build Privacy Preferences Policy Control payloads for macOS: services, identifier and code requirement, Allowed versus Authorization, and which services a profile can only deny."
sources:
  - "https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.TCC.configuration-profile-policy.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pppc-payload

Goal: pre-approve or deny privacy permissions on managed Macs.
- Payload `com.apple.TCC.configuration-profile-policy` (macOS 10.14 and later): device channel only, forbidden with User Enrolment, multiple payloads allowed, must be installed by a device management service and be user-approved. Apple's page states supervision is required to apply it through a device management service and that, with several payloads, the more restrictive settings win.
- The `Services` dictionary is keyed by service, for example `SystemPolicyAllFiles` (full disk access), `SystemPolicySysAdminFiles`, `Accessibility`, `AppleEvents`, `PostEvent`, `ListenEvent`, `ScreenCapture`, `Camera`, `Microphone`, `AddressBook`, `Calendar`, `Reminders`, `Photos`, `MediaLibrary`, `SystemPolicyDesktopFolder`, `SystemPolicyDocumentsFolder`, `SystemPolicyDownloadsFolder`, `SystemPolicyNetworkVolumes`, `SystemPolicyRemovableVolumes`. Each holds an array of entries.
- Entry keys: `Identifier` (case-sensitive bundle ID or install path), `IdentifierType` (`bundleID` or `path`; app bundles by bundle ID, nonbundled binaries by path), `CodeRequirement` (required), optional `StaticCode` (default false), and either `Allowed` (boolean) or `Authorization` (macOS 11 and later: `Allow`, `Deny`, `AllowStandardUserToSetSystemService`, the last valid only for `ListenEvent` and `ScreenCapture`), but not both. `Comment` is not used. `AppleEvents` entries also need `AEReceiverIdentifier`, `AEReceiverIdentifierType` and `AEReceiverCodeRequirement`.
- Get the requirement with `codesign -dr - /path/to/Application.app` (apps) or `codesign -dr - /path/to/mybinary`; include everything after `designated =>`. The YAML gives the form `codesign -display -r -`.
- A profile can only deny, never grant: `Camera`, `Microphone`, `ListenEvent` and `ScreenCapture`. `Camera`, `Microphone`, `Accessibility` and `SpeechRecognition` are deprecated in macOS 27, with `Privacy` in the `com.apple.configuration.app.settings` declaration as the replacement.
- With `Allowed` the user is not prompted and cannot change the value.
Gotcha: helper tools inside an app bundle inherit the app's permissions, while nonbundled binaries need their own path entry; keep the `CodeRequirement` in step with the vendor's signing.
Verify: if prompts still appear after deployment, run `log stream --debug --predicate 'subsystem == "com.apple.TCC" AND eventMessage BEGINSWITH "AttributionChain"'` to find the responsible app or binary.

## Checked

Date: 2026-11-07. Read in full: the Apple Platform Deployment "Privacy Preferences Policy Control device management payload settings" page (supported methods, general settings table, custom payload requirements, the log stream command) and apple/device-management `com.apple.TCC.configuration-profile-policy.yaml` lines 1 to 260 (services after `SystemPolicyDesktopFolder` were not read). Removed: PPPC Utility, the Settings > Privacy Verify, "tccutil is not needed", the "one profile per vendor" advice and the claim that Full Disk Access/Accessibility are "user prompt only".
Method: documentation only; no commands were run.
