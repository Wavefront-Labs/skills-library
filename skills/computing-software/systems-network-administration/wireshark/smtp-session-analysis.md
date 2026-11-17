---
id: computing-software.systems-network-administration.wireshark.smtp-session-analysis
name: smtp-session-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, smtp-analysis, smtp, starttls, email, protocol-analysis]
level: practitioner
status: verified
description: "Analyse SMTP sessions in Wireshark: EHLO capabilities, STARTTLS, AUTH, reply codes, DATA transfer and diagnosing rejections and delivery delays."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321
  - https://www.rfc-editor.org/rfc/rfc3207
  - https://www.wireshark.org/docs/dfref/s/smtp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMTP analysis

## Filters
```
smtp
smtp.req.command == "EHLO"             # case-sensitive: smtplib sends lowercase, use upper(smtp.req.command) == "EHLO"
smtp.response.code >= 400
smtp.req.command == "STARTTLS"
smtp.req.command == "AUTH"
imf                                    # message content (cleartext only)
```
Ports: 25 (MTA relay), 587 (submission, STARTTLS), 465 (implicit TLS submission).

## Session flow
`220` banner, `EHLO` -> `250-` capability list (SIZE, STARTTLS, AUTH, PIPELINING, 8BITMIME),
`STARTTLS` -> `220`, then TLS, new EHLO, `MAIL FROM`, `RCPT TO`, `DATA` -> `354`, message, `.` ->
`250 queued as ...`, `QUIT`.

## Reading failures
| Reply | Typical meaning |
|-------|-----------------|
| 421 | service not available, closing the channel (RFC 5321); often a connection limit at the banner |
| 450/451 | temporary (450 mailbox unavailable, 451 error in processing); greylisting and DNS failures commonly land here |
| 452 | insufficient system storage (too many recipients is also reported as 452) |
| 530/535 | authentication required (5.7.0) / credentials invalid (5.7.8), RFC 4954 |
| 550 5.7.1 | policy rejection: SPF/DMARC/relay denied/blocklisted |
| 552 | exceeded storage allocation (size limit) |
| 554 | transaction failed, often at banner for blocklisted IPs |
Enhanced status codes appear in the text: 5.7.23 SPF validation failed, 5.7.25 reverse DNS validation failed, 5.7.26 multiple authentication checks failed (IANA registry); a DMARC reject may use any of these or a plain 5.7.1.

## Delays
- Long gap before the 220 banner: server doing reverse DNS/RBL lookups (tarpitting).
- Gaps after `.`: content scanning.
Use `frame.time_delta_displayed` with the filter `smtp` per stream.

## STARTTLS problems
- No STARTTLS in the EHLO response from a server that supports it: something on the path altered the reply; RFC 3207
  section 6 describes deleting the `250 STARTTLS` line as a man-in-the-middle attack. Compare captures on both sides of any
  SMTP-inspecting middlebox.
- TLS alert after STARTTLS: certificate/version mismatch.

## Verify
- [ ] A test send shows 250 after DATA completion and the expected TLS/AUTH steps.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 over a loopback capture of Python `smtplib` against a minimal SMTP server on port 2525 (decoded with `-d tcp.port==2525,smtp`; 550 5.7.1 on one RCPT, 250 queued): `smtp.response.code >= 400` and `imf` matched, `smtp.req.command == "STARTTLS"`/`"AUTH"` matched nothing (none sent), and `smtp.req.command == "EHLO"` did NOT match because smtplib sends lowercase `ehlo` (the field is case-preserving); `upper(smtp.req.command) == "EHLO"` matched. `smtp.req.parameter` carried the EHLO name.
- Reply meanings checked in RFC 5321 (421, 450, 451, 452, 550, 552, 554: https://www.rfc-editor.org/rfc/rfc5321.txt) and RFC 4954 (530 5.7.0, 535 5.7.8); enhanced codes 5.7.1, 5.7.23, 5.7.24, 5.7.25, 5.7.26 in the IANA registry https://www.iana.org/assignments/smtp-enhanced-status-codes/ (5.7.26 is "Multiple authentication checks failed", not DMARC specifically; the old text was corrected); RFC 3207 section 6 on STARTTLS stripping. The Cisco `XXXXXXXA` claim could not be confirmed and was removed.
- Not captured here: a real STARTTLS upgrade and AUTH exchange; the skill describes them from RFC 3207/4954 only.
