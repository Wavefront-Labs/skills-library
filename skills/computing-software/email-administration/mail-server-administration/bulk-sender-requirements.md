---
id: computing-software.email-administration.mail-server-administration.bulk-sender-requirements
name: bulk-sender-requirements
category: computing-software
field: email-administration
product: mail-server-administration
tags: [bulk-sender-requirements, bulk-sender, google-yahoo-requirements, spam-rate]
level: practitioner
status: draft
description: "Meet the Google and Yahoo bulk sender requirements: SPF and DKIM, DMARC, PTR, TLS, low spam rate, one-click unsubscribe."
sources:
  - https://support.google.com/a/answer/81126
  - https://senders.yahooinc.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk sender requirements

**Goal:** a checklist for senders of high volume.
## Steps
1. Authenticate with SPF and DKIM, and publish DMARC (at least p=none) with alignment.
2. Valid forward and reverse DNS for sending IPs; TLS for transmission.
3. Keep spam complaint rate low (Google guidance cites staying under 0.1% and never reaching 0.3%; check the current page).
4. Marketing mail needs one-click unsubscribe (RFC 8058) and honouring within two days (provider guidance; confirm).
5. Format messages per RFC 5322.
## Failure modes
- Different providers' thresholds change; re-read their pages each year.
## Verify
- Postmaster Tools shows authenticated traffic and low spam rate.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
