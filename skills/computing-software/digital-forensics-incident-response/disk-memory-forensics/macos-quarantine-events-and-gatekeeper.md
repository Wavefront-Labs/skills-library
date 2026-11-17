---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-quarantine-events-and-gatekeeper
name: macos-quarantine-events-and-gatekeeper
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [quarantine-events, macos-forensics, download-provenance, gatekeeper, dfir]
level: practitioner
status: draft
description: "Trace macOS download provenance with QuarantineEventsV2, com.apple.quarantine xattrs and kMDItemWhereFroms, plus Gatekeeper/XProtect logs for executed payloads."
sources: ["https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web", "https://www.sans.org/white-papers/", "https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS quarantine events and Gatekeeper

**Goal:** prove where a file on a Mac came from, when, and through which application, and
whether Gatekeeper checked or blocked it when opened.

## QuarantineEventsV2
`~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2` (SQLite), table `LSQuarantineEvent`:
| Column | Meaning |
|---|---|
| `LSQuarantineEventIdentifier` | UUID - matches the xattr on the file |
| `LSQuarantineTimeStamp` | Mac absolute time (seconds since 2001-01-01) |
| `LSQuarantineAgentBundleIdentifier` / `AgentName` | Downloading app (Safari, Chrome, Mail, Messages, AirDrop) |
| `LSQuarantineDataURLString` | URL of the file |
| `LSQuarantineOriginURLString` | Page/origin that referred it |
| `LSQuarantineSenderName/Address` | For Mail/Messages/AirDrop |
```sql
SELECT datetime(LSQuarantineTimeStamp + 978307200,'unixepoch') t, LSQuarantineAgentName, LSQuarantineDataURLString, LSQuarantineOriginURLString
FROM LSQuarantineEvent ORDER BY LSQuarantineTimeStamp;
```

## Extended attributes on the file
```bash
xattr -l file.dmg
# com.apple.quarantine: 0083;6712a3f1;Safari;<UUID>   (flags;hex unix time;agent;event UUID)
mdls -name kMDItemWhereFroms file.dmg               # download URL and referrer (Spotlight metadata)
```
Flags: `0081`/`0083` etc. bit 0x40 set means the user approved opening (Gatekeeper passed / user overrode).

## Gatekeeper and XProtect evidence
- Unified logs: `log show --predicate 'process == "syspolicyd" OR process == "XProtect"' --last 7d` - assessment results, notarization checks, user overrides ("Open Anyway").
- `/var/db/SystemPolicyConfiguration/ExecPolicy` (SQLite) records executed/assessed binaries on recent macOS versions.
- XProtect Remediator logs in unified logs (`com.apple.XProtectFramework`).

## Gotchas
- Files fetched with `curl`, unzipped by some tools, or copied from network shares lack quarantine xattrs - commonly abused to bypass Gatekeeper.
- Users can clear QuarantineEventsV2; the xattr on the file may survive (and vice versa).

## Verify
For each payload, xattr UUID matches a QuarantineEventsV2 row, and Gatekeeper logs show what happened at first open.
