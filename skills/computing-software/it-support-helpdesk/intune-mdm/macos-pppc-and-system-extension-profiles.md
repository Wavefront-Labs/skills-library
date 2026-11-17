---
id: computing-software.it-support-helpdesk.intune-mdm.macos-pppc-and-system-extension-profiles
name: macos-pppc-and-system-extension-profiles
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, macos-management, pppc-profile, tcc, privacy-preferences-policy-control, full-disk-access, system-extensions, kernel-extensions, managed-login-items, code-requirement]
level: advanced
status: draft
description: "Pre-approve macOS privacy and extension prompts via MDM: PPPC (TCC) profiles for Full Disk Access and more, code requirements, system extension and login item approval."
sources:
  - "https://support.apple.com/guide/deployment/welcome/web"
  - "https://developer.apple.com/documentation/devicemanagement/systemextensions"
  - "https://developer.apple.com/documentation/devicemanagement/privacypreferencespolicycontrol"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macos-pppc-and-system-extension-profiles

Goal: security agents, remote support tools and backup clients work on day
one, without users clicking "Allow" in System Settings (they can't for
Full Disk Access anyway without admin rights).

## What needs what
| Need | Payload |
|---|---|
| EDR/AV/backup reading all files | PPPC: `SystemPolicyAllFiles` (Full Disk Access) |
| Remote support control | PPPC: `Accessibility` (allow); `ScreenCapture` can only be set to "allow standard user to approve", not silently allowed |
| Automation (Apple Events) between apps | PPPC: `AppleEvents` with receiver |
| Network/endpoint security extensions | **System Extensions** payload: team ID + bundle IDs + extension types |
| Legacy kexts (avoid) | Kernel Extensions payload (Apple silicon also needs reduced security) |
| Background items (launch agents/daemons) | **Managed Login Items** / Service Management payload (macOS 13+) — stops "background item added" prompts |
| Content filter / VPN | their own payloads (Web Content Filter, VPN) |

## PPPC profile entry
Identifier (bundle ID or binary path), **Identifier Type**, **Code
Requirement** (exact), service, Allowed. Get the code requirement:
```bash
codesign -dr - /Applications/Vendor.app 2>&1 | sed -n 's/^designated => //p'
```
Vendors usually publish a ready-made PPPC/system extension profile — use
theirs. Jamf has a PPPC Utility app; Intune uses custom .mobileconfig or the
settings catalog (Privacy Preferences).

## Rules
- Must be delivered by **user-approved/ADE MDM** — profiles installed
  manually don't grant TCC.
- Deliver **before** the app installs (scope profile first, then package)
  to avoid prompts and half-working agents.
- Wrong code requirement = silently ignored.

## Troubleshooting
```bash
sudo profiles show -type configuration | grep -A3 -i tcc
systemextensionsctl list            # [activated enabled] expected
log show --predicate 'subsystem == "com.apple.TCC"' --last 10m
```
`tccutil reset All <bundleID>` clears user decisions for retesting.

## Verify
Agent's console shows Full Disk Access granted; `systemextensionsctl list`
shows extensions activated enabled; no privacy prompts on a fresh test Mac.
