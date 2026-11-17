---
id: computing-software.it-support-helpdesk.apple-device-management.kernel-extension-approval
name: kernel-extension-approval
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, kernel-extension, kernel-extension-approval, kext, legacy]
level: practitioner
status: docs-checked
description: "Pre-approve legacy macOS kernel extensions with the com.apple.syspolicy.kernel-extension-policy payload, and know its keys, defaults and enrolment limits."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.syspolicy.kernel-extension-policy.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kernel-extension-approval

Goal: keep legacy kexts working only while required.
- Payload `com.apple.syspolicy.kernel-extension-policy` (macOS 10.13.2 and later): device channel only, not allowed with User Enrolment, must be user-approved, multiple instances allowed.
- `AllowedTeamIdentifiers`: team IDs whose validly signed kernel extensions can load. `AllowedKernelExtensions`: dictionary mapping a team identifier to an array of bundle identifiers that the system always allows to load.
- `AllowUserOverrides` (default false): true lets users approve additional extensions that profiles do not explicitly allow. `AllowNonAdminUserApprovals` (macOS 11 and later, default false): true lets non-administrative users approve extensions in the Security & Privacy preferences.
- The payload's own description: it enables team identifiers or specific kernel extensions to load without user approval and can block users from approving others.
Practice: inventory which Macs still need a kext, record the vendor's plan to move to a system extension (see system-extension-approval), and keep the allowlist as small as possible.
Verify: the profile shows as installed and the listed extension loads without a user approval step.

## Checked

Date: 2026-11-07. Read in full: apple/device-management `com.apple.syspolicy.kernel-extension-policy.yaml` (all keys, defaults, OS minimum, enrolment and channel limits). Removed: every Apple silicon / reduced security claim, `kmutil showloaded`, `bputil -d`, the Extension Attribute inventory idea and the "MDM can only allow when supervised" claim, none of which the page states; the previously cited Apple guide URL redirected to the guide welcome page and the developer.apple.com page is unreadable.
Method: documentation only; no commands were run.
