---
id: computing-software.email-administration.mail-server-administration.mail-monitoring-checks
name: mail-monitoring-checks
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mail-monitoring-checks, mail-monitoring, monitoring, nagios-check, certificate-expiry, smtp-probe]
level: practitioner
status: draft
description: "Monitor a mail server: SMTP/IMAP port checks, certificate expiry, queue size, blocklist status and DNS record drift."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mail monitoring checks

**Goal:** know before users complain.
## Checks
- Ports 25, 587, 993 respond with a banner; TLS cert expiry above 14 days.
- Synthetic test: send a message to a probe mailbox and fetch it by IMAP, measure latency.
- DNS: MX, SPF, DKIM, DMARC records unchanged (diff against a stored copy).
- Daily blocklist status of outbound IPs.
## Steps
1. Run probes from outside your network.
2. Alert via email to a different system (not the one you monitor).
## Failure modes
- Monitoring emails sent through the same broken server.
## Verify
- Stopping Postfix in staging triggers the alert within your set interval.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
