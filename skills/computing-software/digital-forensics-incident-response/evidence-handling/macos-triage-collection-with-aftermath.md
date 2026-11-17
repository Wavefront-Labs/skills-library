---
id: computing-software.digital-forensics-incident-response.evidence-handling.macos-triage-collection-with-aftermath
name: macos-triage-collection-with-aftermath
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [aftermath, triage-collection, macos-forensics, live-response, dfir]
level: practitioner
status: draft
description: "Collect and analyse macOS triage data with Jamf's Aftermath: deployment via MDM, collection contents, deep mode, analysis mode and output handling."
sources: ["https://github.com/jamf/aftermath", "https://support.apple.com/guide/deployment/welcome/web"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS triage collection with Aftermath

**Goal:** Aftermath is an open-source macOS incident response collector (Swift, signed and
notarised builds) that gathers persistence, logs, browser and system artefacts, then builds a
timeline.

## Deploy
- Install the signed `.pkg` from the GitHub releases (installs to `/usr/local/bin/aftermath`).
- Grant **Full Disk Access** via an MDM PPPC profile for the binary, or many artefacts (TCC.db,
  Mail, Safari) will be missing.
- Push via MDM (Jamf policy script) or run from an IR shell with sudo.

## Collect
```bash
sudo aftermath                      # standard collection -> /tmp/Aftermath_<serial>.zip
sudo aftermath --deep               # adds file system walk with metadata for a timeline (slow)
sudo aftermath -o /Volumes/EVID     # output location
sudo aftermath --pretty             # colourised console
```
Collection includes: unified log excerpts, LaunchAgents/Daemons, login items, cron, shell history,
installed apps, browser histories (Safari, Chrome, Firefox, Edge), TCC databases,
quarantine events, network configuration, running processes, and system info.

## Analyse
```bash
aftermath --analyze /path/Aftermath_<serial>.zip   # parses and builds storyline.csv timeline
```
Review `storyline.csv` sorted by time around the alert, then pivot into raw artefacts.

## Handling
- Hash the zip on collection (`shasum -a 256`) and record the serial number and Aftermath version.
- Clean up with `aftermath --cleanup` to remove local output after upload.

## Gotchas
- No memory capture; macOS memory acquisition needs separate tooling and is heavily restricted.
- Unified logs are large; Aftermath collects targeted ranges - add a `log collect --last 3d` archive if needed.
- Running without FDA silently skips protected locations; check the collection log for permission errors.

## Verify
The archive contains TCC.db, browser histories and persistence plist folders, confirming FDA was effective.
