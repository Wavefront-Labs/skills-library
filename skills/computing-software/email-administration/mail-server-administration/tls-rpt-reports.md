---
id: computing-software.email-administration.mail-server-administration.tls-rpt-reports
name: tls-rpt-reports
category: computing-software
field: email-administration
product: mail-server-administration
tags: [tls-rpt-reports, tls-rpt, smtp-tls-reporting, _smtp._tls]
level: advanced
status: docs-checked
description: "Receive SMTP TLS reports (TLS-RPT) by publishing _smtp._tls TXT and reading the JSON reports."
sources:
  - https://www.rfc-editor.org/rfc/rfc8461
  - https://www.rfc-editor.org/rfc/rfc8460
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tls rpt reports

**Goal:** learn which senders fail to deliver over TLS (RFC 8460).
## Steps
1. Publish `_smtp._tls.example.com. TXT "v=TLSRPTv1; rua=mailto:tlsrpt@example.com"`. If several TXT records are returned, those that do not begin with `v=TLSRPTv1;` are discarded.
2. Reports are JSON that SHOULD be gzip compressed (media type `application/tlsrpt+gzip`, otherwise `application/tlsrpt+json`). Look at `policies`, `summary` with `total-failure-session-count`, and `failure-details` entries whose `result-type` is a value such as `certificate-expired`.
3. Review the reports while MTA-STS is in `testing` mode, before moving it to `enforce` (RFC 8461 says testing-mode senders that implement TLSRPT send a report of policy failures).
## Failure modes
- Mailbox not receiving: check the rua address and your own filters.
## Verify
- `dig +short TXT _smtp._tls.example.com` returns the record.

## Checked

2026-11-09. Confirmed on RFC 8460: the _smtp._tls name and v=TLSRPTv1 record with rua mailto, discarding of non-matching TXT records, gzip compression and the tlsrpt+gzip and tlsrpt+json media types, the policies, summary, total-failure-session-count and failure-details fields, and the certificate-expired result type. Confirmed on RFC 8461 the testing mode reporting behaviour. Removed: the claim that the first report typically arrives within a day (not stated) and the boilerplate Postfix/Dovecot notes.

Method: documentation only; no commands were run.
