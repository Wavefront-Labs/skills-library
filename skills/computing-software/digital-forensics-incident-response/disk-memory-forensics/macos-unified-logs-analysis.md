---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-unified-logs-analysis
name: macos-unified-logs-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [unified-logs, macos-forensics, log-show, logarchive, tracev3, dfir]
level: advanced
status: draft
description: "Analyse macOS Unified Logs: collecting logarchives, log show predicates, key subsystems for logins, process execution, TCC and remote access, and offline parsers."
sources: ["https://developer.apple.com/documentation/os/logging", "https://github.com/mandiant/macos-UnifiedLogs", "https://www.sans.org/cyber-security-courses/mac-and-ios-forensic-analysis-and-incident-response/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS Unified Logs analysis

**Goal:** extract user, process and security events from the macOS Unified Logging system.

## Storage and collection
Logs live in `/private/var/db/diagnostics/` (`Persist`, `Special`, `Signpost`,
`HighVolume`, `timesync`) as `.tracev3` files plus `/private/var/db/uuidtext/` (format
strings). Both are needed.
```bash
sudo log collect --output /Volumes/EVID/host.logarchive --last 7d   # live
# from an image: copy diagnostics + uuidtext into a .logarchive structure
```

## Querying (on a Mac)
```bash
log show --archive host.logarchive --style ndjson --start "2026-09-01 00:00:00" > all.ndjson
log show --archive host.logarchive --predicate 'process == "sshd"' --info
log show --archive host.logarchive --predicate 'subsystem == "com.apple.TCC"' --debug
log show --archive host.logarchive --predicate 'eventMessage CONTAINS[c] "screensharingd"'
```
Useful areas: `loginwindow`/`opendirectoryd` (logins, auth failures), `sudo`,
`sshd`, `screensharingd` (VNC/ARD), `com.apple.xprotect`/`syspolicyd` (Gatekeeper,
notarization, XProtect detections), `com.apple.TCC` (privacy permission grants),
`com.apple.launchd` (job loads, persistence), `kernel` (USB, network).

## Offline parsing (no Mac needed)
Mandiant `unifiedlog_parser` (Rust, macos-UnifiedLogs) outputs CSV/JSON from a logarchive or
raw diagnostics folders; also Plaso `unified_logging` parser in recent versions.

## Gotchas
- Retention is short (days to a few weeks) and volume high; collect early.
- Many messages are `<private>` redacted unless a logging profile was installed beforehand.
- Times are recorded with boot-relative continuous time and converted via `timesync`; keep
  those files.

## Verify
Cross-check key events (logins, process launches) with other artefacts (KnowledgeC, FSEvents,
`/var/log/` legacy logs) and confirm timestamps convert consistently in two tools.
