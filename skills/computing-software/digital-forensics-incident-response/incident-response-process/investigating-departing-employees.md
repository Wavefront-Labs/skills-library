---
id: computing-software.digital-forensics-incident-response.incident-response-process.investigating-departing-employees
name: investigating-departing-employees
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [departing-employee, insider-threat, data-exfiltration, hr-investigation, dfir]
level: practitioner
status: draft
description: "Investigate data taking by departing employees: legal basis, preservation, the 30-90 day lookback across USB, cloud, email and print, and reporting to HR/legal."
sources: ["https://insights.sei.cmu.edu/library/common-sense-guide-to-mitigating-insider-threats-seventh-edition/", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Investigating departing employees

**Goal:** determine whether a leaver (often joining a competitor) took confidential data, with
evidence that will stand up in civil litigation.

## Before collecting
- Instruction from legal/HR with the scope (person, systems, period); confirm the acceptable-use
  policy and local privacy law allow monitoring and review.
- Preserve immediately at notice of resignation, not after they leave: laptops get reimaged by IT
  on return. Place a hold on mailbox, OneDrive, and the device.

## Lookback window
CERT research shows most IP theft happens within 30 days of departure; review 90 days before
notice through the last day.

## What to examine
- **USB / removable media:** USBSTOR, MountPoints2, partition diagnostic log, LNK files and
  jump lists pointing to removable volumes, shellbags of removable drive-letter paths.
- **Cloud sync and upload:** personal Google Drive/Dropbox clients, browser uploads (proxy/CASB
  logs), OneDrive sharing to personal accounts, mass downloads in SharePoint audit logs (`FileDownloaded`, `FileSyncDownloadedFull`).
- **Email:** sent to personal addresses with attachments; auto-forward rules.
- **Printing:** print server logs (event 307) and printer job logs.
- **Volume anomalies:** UAL/CASB download counts vs the user's baseline; archive creation (7z/zip) before departure.
- **Anti-forensics:** wiping tools, browser history clearing, factory resets shortly before return.

## Reporting
Neutral factual report: what was accessed/copied, when, to where, with evidence references;
avoid conclusions on intent. Legal may use it for a demand letter or injunction.

## Gotchas
- Personal devices: no access without consent or court order.
- Activity part of normal duties (copying files to work USB for a client) needs business context from the manager.

## Verify
Every exfiltration claim in the report cites at least two corroborating artefacts.
