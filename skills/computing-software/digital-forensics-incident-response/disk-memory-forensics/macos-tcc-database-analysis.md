---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-tcc-database-analysis
name: macos-tcc-database-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [tcc-database, macos-forensics, privacy-permissions, sqlite-forensics, dfir]
level: advanced
status: draft
description: "Analyse macOS TCC.db privacy permissions: user vs system databases, access table fields, auth values, timestamps, and spotting malware-granted or tampered permissions."
sources: ["https://support.apple.com/guide/security/controlling-app-access-to-files-secddd1d86a6/web", "https://www.rainforestqa.com/blog/macos-tcc-db-deep-dive", "https://attack.mitre.org/techniques/T1548/006/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS TCC database analysis

**Goal:** Transparency, Consent and Control (TCC) records which apps may use the camera, microphone,
screen recording, Full Disk Access, Accessibility and more. Malware needs these permissions; their
grants are evidence of capability and timing.

## Databases
- System: `/Library/Application Support/com.apple.TCC/TCC.db` (Full Disk Access, Accessibility, Screen Recording - system-wide services).
- Per user: `~/Library/Application Support/com.apple.TCC/TCC.db` (camera, microphone, contacts, documents folders...).
- Protected by SIP/TCC itself: collect from an image or with an FDA-enabled collector.

## access table (key columns)
| Column | Meaning |
|---|---|
| `service` | e.g. `kTCCServiceSystemPolicyAllFiles` (FDA), `kTCCServiceAccessibility`, `kTCCServiceScreenCapture`, `kTCCServiceMicrophone`, `kTCCServiceCamera`, `kTCCServiceAppleEvents` |
| `client` / `client_type` | Bundle ID (0) or absolute path (1) |
| `auth_value` | 0 denied, 1 unknown, 2 allowed, 3 limited |
| `auth_reason` | How it was set: 2 user consent, 3 user set (System Settings), 4 system set, 5 service policy, 6 MDM policy, ... |
| `csreq` | Code-signing requirement blob for the client |
| `last_modified` | Unix epoch of the grant |
| `indirect_object_identifier` | For AppleEvents: the target app |

```sql
SELECT service, client, client_type, auth_value, auth_reason, datetime(last_modified,'unixepoch') AS modified
FROM access ORDER BY last_modified DESC;
```

## What to look for
- Grants to unsigned binaries / path-based clients in `/tmp`, the shared users folder, hidden folders.
- Screen Recording, Accessibility, FDA grants around the infection time.
- `auth_reason` 4/5 unexpected for third-party clients (direct DB tampering when SIP was disabled or via exploits such as TCC bypass CVEs).
- Unified logs from `tccd` show prompts and decisions: `log show --predicate 'subsystem == "com.apple.TCC"'`.

## Gotchas
- MDM PPPC profiles grant permissions without DB rows in some cases (`/Library/Application Support/com.apple.TCC/MDMOverrides.plist`).
- Schema changes across macOS versions (columns added); check `PRAGMA table_info(access)`.

## Verify
Each sensitive grant is attributed to a legitimate app or flagged with its timestamp in the timeline.
