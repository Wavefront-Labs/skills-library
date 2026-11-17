---
id: computing-software.email-administration.mail-server-administration.header-anatomy-reading
name: header-anatomy-reading
category: computing-software
field: email-administration
product: mail-server-administration
tags: [header-anatomy-reading, received-headers, message-id, authentication-results, header-analysis]
level: practitioner
status: draft
description: "Read a message's Received chain, Message-ID and Authentication-Results top to bottom to locate delay or forgery."
sources:
  - https://www.rfc-editor.org/rfc/rfc5322
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Header anatomy reading

**Goal:** trace a message hop by hop.
## Steps
1. Read `Received:` lines bottom to top; each hop prepends one. Only your own servers' lines are trustworthy; lines below them can be forged.
2. Compute per-hop delay from the timestamps (watch time zones).
3. Check `Authentication-Results:` added by your own receiving MTA for spf/dkim/dmarc results.
4. Check `Message-ID:` domain and `Date:` for sanity.
## Failure modes
- Trusting an `Authentication-Results` header that arrived from outside rather than the one your server added.
- A large delay at one hop usually means greylisting, a deferral queue or throttling there.
## Verify
- Your own server's Received line carries the queue id; find the same id in the mail log.
- Per-hop delays add up to the end-to-end delay you observed.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
