---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.webmail-and-cloud-mailbox-artefacts
name: webmail-and-cloud-mailbox-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [webmail-forensics, email-forensics, browser-forensics, m365, gmail, dfir]
level: practitioner
status: draft
description: "Find evidence of webmail and cloud mailbox use on endpoints and in provider logs: browser history and cache, downloaded attachments, and server-side audit data."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://learn.microsoft.com/en-us/purview/audit-log-activities", "https://support.google.com/a/answer/4579579"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Webmail and cloud mailbox artefacts

**Goal:** show which webmail accounts a user accessed, what they did (read, send, attach),
and get message content from the provider when lawful.

## Endpoint artefacts
- Browser history: `mail.google.com/mail/u/0/#inbox/<id>`, `outlook.live.com`,
  `outlook.office.com`, ProtonMail; URL fragments reveal folders and message IDs.
- Browser cache: cached message views, inline images, attachment previews (Chromium
  `Cache_Data`, Firefox `cache2`); parse with ChromeCacheView or Hindsight.
- Downloads with Zone.Identifier `HostUrl` from `mail-attachment.googleusercontent.com`,
  `attachment.outlook.live.net`.
- Uploads: OpenSavePidlMRU in NTUSER.DAT (files picked to attach), proxy POST sizes.
- Session cookies (which accounts were logged in).

## Provider side (corporate)
- M365: Unified Audit Log `MailItemsAccessed`, `Send`, `MailboxLogin`; OWA client info
  strings; sign-in logs per app.
- Google Workspace: Gmail log events (Admin console reporting) and Gmail log search
  (BigQuery export) for message delivery, opens via client types.

## Personal accounts
Content requires the user's consent or legal process to the provider (subpoena/warrant,
preservation request first). Endpoint residue is often all you have.

## Gotchas
- Webmail in private windows leaves little on disk; rely on network logs and memory.
- Mobile apps for webmail sync locally (Gmail app DB on Android) rather than browser caches.

## Verify
Each claimed webmail action has a browser/cache artefact and, where possible, a network or
provider log entry at the same time.
