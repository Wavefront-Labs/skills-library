---
id: computing-software.digital-forensics-incident-response.incident-response-process.proving-exfiltration-to-personal-cloud-storage
name: proving-exfiltration-to-personal-cloud-storage
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [cloud-upload-exfiltration, insider-threat, data-exfiltration, browser-forensics, casb, dfir]
level: advanced
status: draft
description: "Prove or rule out upload of company data to personal cloud storage or webmail: browser, sync client, proxy and CASB evidence, and file-to-upload correlation."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://attack.mitre.org/techniques/T1567/002/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proving exfiltration to personal cloud storage and webmail

**Goal:** show that specific company files were uploaded to a personal Google Drive,
Dropbox, OneDrive personal, WeTransfer or webmail account, by the user, at a time.

## Sources
| Source | What it gives |
|---|---|
| Proxy / SWG logs | Upload requests (POST/PUT, large request bytes) to storage domains, with user and time |
| CASB / Defender for Cloud Apps | App activity: "upload file" to unsanctioned app, file names sometimes |
| Browser history (Chromium `History` db) | Visits to upload pages, file picker use is not stored, but `downloads` table and visited URLs are |
| Sync clients | Dropbox `.dropbox` / `instance1` databases, Google Drive for desktop `metadata_sqlite_db`, OneDrive personal logs listing synced file names |
| Endpoint | EDR file read events by browser process right before upload; `RecentDocs`, jump lists for the browser showing file paths opened in the file picker |
| Mail | Personal webmail sends are only in proxy/browser; corporate mail with attachments to personal addresses in message trace |

## Method
1. Identify candidate time windows from proxy upload volume spikes per user.
2. In those windows, find which files the browser or sync client read (EDR, jump lists,
   OpenSaveMRU `OpenSavePidlMRU` in NTUSER.DAT shows files chosen in open/save dialogs).
3. Match file sizes to upload request sizes (approximate; TLS and encoding overhead).
4. Check for staging: archives created shortly before (zip/7z), renamed extensions.

## Gotchas
- TLS inspection off means proxy logs show only domain and bytes, not file names.
- Corporate OneDrive vs personal OneDrive share domains; check tenant/account in URLs or
  sync client config.
- Get legal sign-off before examining any personal account data.

## Verify
For each claimed exfiltrated file, cite at least two independent artefacts (e.g. OpenSaveMRU
entry and proxy upload of matching size within seconds).
