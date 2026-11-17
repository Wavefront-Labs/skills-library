---
id: computing-software.it-support-helpdesk.apple-device-management.system-extension-approval
name: system-extension-approval
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, system-extension, system-extension-approval, endpoint-security, network-extension]
level: practitioner
status: docs-checked
description: "Pre-approve macOS system extensions with the com.apple.system-extension-policy payload: team and bundle identifiers, extension types, removal rules and profile combining."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.system-extension-policy.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# system-extension-approval

Goal: let approved security agents and drivers load without a user prompt.
- Payload `com.apple.system-extension-policy` (macOS 10.15 and later): device channel only, not allowed with User Enrolment, and the page says the payload must be user-approved.
- `AllowedTeamIdentifiers`: team IDs whose validly signed system extensions may load. `AllowedSystemExtensions`: a dictionary mapping a team identifier to an array of bundle identifiers. The same team identifier in both is an error.
- `AllowedSystemExtensionTypes` maps a team identifier to the types it may install: `DriverExtension`, `NetworkExtension`, `EndpointSecurityExtension`. With no entry for a team, all types are allowed.
- `AllowUserOverrides` (default true): false stops users approving extensions that profiles do not explicitly allow.
- Removal: `RemovableSystemExtensions` (macOS 12 and later) lets an app deactivate the listed extensions through `OSSystemExtensionDeactivationRequest` without admin authorisation. `NonRemovableSystemExtensions` and `NonRemovableFromUISystemExtensions` (macOS 15 and later) prevent disabling or uninstalling, the second only from System Settings or Finder; the same mapping cannot appear in both Removable and NonRemovable.
- Activating an allowed extension with the `OSSystemExtensionActivationRequest` API avoids the administrator prompt.
- From macOS 11.3, installing the payload completes activation of an allowed extension that is pending, and removing it deactivates an allowed active extension.
- With several profiles, `AllowUserOverrides` is false if any profile sets false; all other values combine.
Practice: take team identifier and bundle IDs from the vendor, scope the profile to Macs that run the agent, and re-check after vendor releases because the allowlist is by bundle ID.
Verify: the profile shows as installed and the vendor app activates its extension without an approval prompt.

## Checked

Date: 2026-11-07. Read in full: apple/device-management `com.apple.system-extension-policy.yaml` (all keys, OS minimums, combining notes, the 11.3 activation behaviour). Removed: pairing with PPPC and content filter payloads, `systemextensionsctl list` (command not on the page), the "approval must reach the Mac before the app installs" gotcha and the activated-enabled Verify.
Method: documentation only; no commands were run.
