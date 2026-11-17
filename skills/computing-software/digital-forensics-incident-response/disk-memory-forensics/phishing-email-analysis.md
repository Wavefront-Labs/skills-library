---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.phishing-email-analysis
name: phishing-email-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [phishing-analysis, email-forensics, maldoc, url-analysis, email-header-analysis, dfir]
level: practitioner
status: draft
description: "Analyse a reported phishing email end to end: headers, links and redirects, attachments, credential-harvest pages, safe detonation and IOC extraction for blocking."
sources: ["https://github.com/decalage2/oletools", "https://urlscan.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phishing email analysis

**Goal:** decide quickly whether a reported email is malicious, what it does, and produce
IOCs and actions (block, purge, reset).

## Steps
1. **Get the original** as `.eml`/`.msg` with full headers (not a forward, which loses
   them). Hash it.
2. **Headers**: sender, Reply-To, Return-Path, authentication results, originating IP.
3. **Links**: extract all URLs (including from HTML and attachments): `emldump.py`,
   `msgconvert`, or `grep -oE 'https?://[^"> ]+'`. Decode safe-link wrappers
   (`safelinks.protection.outlook.com/?url=`). Check reputation (VirusTotal, urlscan.io
   private scan), follow redirects in a sandboxed browser or `curl -sIL` from an isolated
   host, capture the landing page (credential harvesting kits mimic M365/Okta).
4. **Attachments**: hash, type by magic (`file`), never open on the analysis host.
   Office: `olevba`, `oleid`; PDF: `pdfid`, `pdf-parser`; archives/ISO/LNK: list contents;
   HTML attachments: look for HTML smuggling (base64 blobs, `msSaveOrOpenBlob`). Detonate in
   a sandbox if needed.
5. **Infrastructure**: domains' registration age, hosting, certificate transparency;
   pivot for related campaigns.
6. **Scope**: message trace for same sender/subject/URL; who clicked (proxy, Safe Links
   click logs); who entered credentials (sign-ins from kit infrastructure).

## Outputs
Verdict, IOCs (sender, domains, URLs, hashes, IPs), actions: purge, block sender/URL,
reset credentials of submitters, user notification.

## Gotchas
- Credential pages may geofence or show benign content to scanners; use residential egress
  or user agent of the target where policy allows.
- Do not visit links from your corporate network or logged-in browser.

## Verify
Purge search returns zero items afterwards and no further clicks appear in proxy/Safe Links
logs after blocking.
