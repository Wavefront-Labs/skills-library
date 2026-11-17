---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.featureusage-taskbar-interaction-keys
name: featureusage-taskbar-interaction-keys
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [featureusage, evidence-of-execution, ntuser, windows-registry, dfir]
level: practitioner
status: draft
description: "Read the NTUSER FeatureUsage keys (AppSwitched, AppLaunch, ShowJumpView, AppBadgeUpdated) to show a user interacted with an application via the taskbar."
sources: ["https://www.crowdstrike.com/blog/how-to-employ-featureusage-for-windows-10-taskbar-forensics/", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FeatureUsage taskbar interaction keys

**Goal:** Windows 10/11 counts how often a user switches to, launches, or opens jump lists for
taskbar applications. It supports "the user actively used program X" beyond mere execution.

## Location
`NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\`
| Subkey | Meaning |
|---|---|
| `AppSwitched` | Count of times the user left-clicked a taskbar app to switch to it (focus) |
| `AppLaunch` | Launches of applications **pinned** to the taskbar |
| `ShowJumpView` | Right-clicks to open the jump list |
| `AppBadgeUpdated` | Badge updates on taskbar icons (e.g. unread counts) - shows app was running |
| `TrayButtonClicked` | Clicks on built-in tray buttons (Start, Search, Task View, Clock) |

Value names are full application paths or AppUserModelIDs; data is a DWORD count.

## Analysis
- Use RECmd (Kroll batch includes FeatureUsage) or Registry Explorer.
- No per-entry timestamp: the subkey last-write time dates the latest update only.
- Presence of a path under `AppSwitched` = the program had a taskbar window that the user clicked
  to focus: strong evidence of interactive use (versus background execution by malware).

## Use cases
- Insider cases: user actively worked in a file-transfer client or encryption tool.
- Rebutting "malware did it" when the application shows many interactive switches.

## Gotchas
- Counts are cumulative and do not reset; no history of when increments happened.
- Applications run via RDP RemoteApp or in VMs do not appear.

## Verify
Corroborate with UserAssist, BAM, prefetch and jump lists for the same application.
