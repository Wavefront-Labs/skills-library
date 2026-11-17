---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-file-blocking-and-data-filtering
name: pan-os-file-blocking-and-data-filtering
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [file-blocking, pan-os, data-filtering, file-types, continue-page, data-loss-prevention]
level: practitioner
status: draft
description: "Block, alert or continue on risky file types with PAN-OS file blocking profiles, plus data filtering patterns for sensitive content."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/policy/file-blocking-profile"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: stop dangerous file types crossing zones and detect basic sensitive-data leakage.

```
configure
set profiles file-blocking FB-STD rules block-exec application any file-type [ exe dll msi ] direction both action block
set profiles file-blocking FB-STD rules continue-archive application any file-type [ zip rar ] direction download action continue
set profile-group PG-STANDARD file-blocking FB-STD
commit
```
`continue` shows a web page requiring the user to confirm, useful for archives; it works for web-browsing only and needs response pages enabled on the ingress interface management profile.

Data filtering (patterns such as credit-card or SSN formats, or custom regex) lives in a data-filtering profile with data objects; it requires a data-filtering password for log viewing of matches. For real DLP use Enterprise DLP (separate licence).

Gotchas
- File type is detected by magic bytes, not extension; renamed files are still caught.
- Encrypted or password-protected archives are opaque; block them by type if policy forbids them.
- `block` closes the connection with a response page for HTTP, but for other protocols the connection resets silently.

## Verify
```
show log data direction equal backward
```
Download a harmless test file of the blocked type in a lab; the data log entry should record the action and file name.
