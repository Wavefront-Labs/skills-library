---
id: computing-software.digital-forensics-incident-response.evidence-handling.preserving-workspace-data-with-google-vault
name: preserving-workspace-data-with-google-vault
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [google-vault, legal-hold, cloud-evidence, google-workspace-audit, dfir]
level: practitioner
status: docs-checked
description: "Use Google Vault for Workspace investigations: licence needs, holds, search, exports with metadata and MD5 checksum files, the 15-day export window and audit."
sources: ["https://support.google.com/vault/answer/2462365", "https://support.google.com/vault/answer/6099459", "https://developers.google.com/vault"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preserving Workspace data with Google Vault

**Goal:** preserve and export Workspace content for an investigation or litigation without relying on the user's account.

## What Vault covers
Vault is an information governance and eDiscovery tool for Google Workspace: retain, hold, search and export. The overview lists Gmail, Drive files, Calendar events, Chat messages (when conversation history is on), Meet recordings and associated logs, Groups messages, Voice items (Voice add-on only), Sites and Gemini conversations. Check the supported data types page for exact coverage and document any gap.

## Licences
Both the users whose data is searched or held and the admins using Vault need a Workspace licence that includes Vault (since 1 November 2025 admins must have one to keep using it). Only users with a Vault licence are covered. Deleting a user or a required licence may irreversibly purge their data, so do not remove either before preserving.

## Holds
- Holds preserve data indefinitely. Place them on accounts, organizational units or groups; for Gmail and chat messages you can limit a hold to matching messages.
- Data on hold remains available to Vault even if users delete it and empty their trash. Retention rules are separate: Vault does not retain anything until rules are set, and data not on hold is subject to standard deletion when a rule expires.

## Search and export
- Search by user account, organizational unit, date or keyword; most services support Boolean operators. Preview messages, attachments and files.
- An export contains a copy of all matching data, the metadata linking it to individual users, and corroborating information to prove it matches the data on Google's servers.
- Exports include a file-checksums file listing MD5 hashes of all files in the export, plus metadata files (XML or CSV, depending on service) and count and error reports. Mail can be exported as mbox or PST; PST contents cannot be correlated with the XML metadata. For Drive, the metadata has a per-file MD5 `Hash`; `SourceHash` (Docs, Sheets, Slides only) can verify an exact copy of the source.
- An export is available for 15 days, then deleted. Download and hash it promptly.
- Verify downloaded files against the checksums file, and also hash them yourself for your custody record.

## API
The Vault API supports eDiscovery: manage matters, place holds, and start and download exports. See its reference for methods.

## Audit
Vault keeps a complete audit log of activity in Vault (creating or editing a retention rule, running a search, exporting data); it cannot be edited. Include it in custody documentation.

## Verify
Hold is active for each custodian; exported file hashes match the checksums file; the audit log shows who exported.

## Checked
Confirmed against the Vault overview (coverage, licences, holds, retention, export contents, 15-day window, audit log), the export contents page (checksums file, MD5 hash, SourceHash, mbox/PST, metadata files) and the Vault API landing page (matters, holds, exports). Removed unconfirmed content: Admin console menu paths, search operator syntax, matter-creation steps, API method names, shared drive scoping, Drive version export, and the Calendar and third-party coverage gaps.

Method: docs-only read of cited pages, 2026-11-09
