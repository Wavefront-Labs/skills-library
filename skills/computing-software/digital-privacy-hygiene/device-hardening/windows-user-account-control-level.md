---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-user-account-control-level
name: windows-user-account-control-level
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, user-account-control, windows-security, standard-user]
level: practitioner
status: docs-checked
description: "Understand Windows User Account Control prompt behaviour for administrators and standard users, secure desktop, and the policy values that set them."
sources:
  - "https://learn.microsoft.com/windows/security/application-security/application-control/user-account-control/"
  - "https://learn.microsoft.com/windows/security/application-security/application-control/user-account-control/settings-and-configuration"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows User Account Control level

**Goal:** software can't get admin rights silently.

## What the policies set (Microsoft Learn, UAC settings and configuration)
- **Behavior of the elevation prompt for administrators in Admin Approval Mode** (registry value `ConsentPromptBehaviorAdmin`):
  0 Elevate without prompting, 1 Prompt for credentials on the secure desktop, 2 Prompt for consent on the secure desktop,
  3 Prompt for credentials, 4 Prompt for consent, 5 Prompt for consent for non-Windows binaries (default). Elevate
  without prompting is for the most constrained environments only.
- **Behavior of the elevation prompt for standard users** (`ConsentPromptBehaviorUser`): 0 automatically deny, 1 prompt for
  credentials on the secure desktop, 3 prompt for credentials (default).
- **Switch to the secure desktop when prompting for elevation** (`PromptOnSecureDesktop`): enabled by default; all
  requests then go to the secure desktop regardless of the prompt behaviour policies.
- **Allow UIAccess applications to prompt for elevation without using the secure desktop**: disabled by default.
- **Only elevate executables that are signed and validated**: enforces signature checks for apps requesting elevation.

## Best combo: standard account plus UAC
Do daily work as a standard user. A standard user's default prompt asks for credentials (an administrative user name and
password) instead of a Yes button, which defeats "just click Yes" tricks.

## Where to set it
Policy: Local Policies > Security Options (the policy names above begin "User Account Control:"). Hardening for
administrators: choose Prompt for credentials on the secure desktop. The Windows slider UI is not described on the fetched
pages; check Microsoft's page for your Windows version.

## Gotchas
- Some installers need elevation once; install, then go back to standard use.
- An unexpected prompt when you weren't installing anything: say No and investigate.

## Checked
2026-10-28. Confirmed on Microsoft Learn (UAC settings and configuration): policy names, options, defaults, registry values.
Removed (not on the fetched pages): the slider level table, Control Panel search path, publisher colour prompts, the
Administrator protection mode note.
Method: documentation only; no commands were run.
