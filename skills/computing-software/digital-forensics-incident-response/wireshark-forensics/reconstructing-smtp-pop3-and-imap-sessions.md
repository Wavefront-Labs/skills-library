---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.reconstructing-smtp-pop3-and-imap-sessions
name: reconstructing-smtp-pop3-and-imap-sessions
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [smtp-forensics, pop3, imap, email-protocols, export-objects-imf, wireshark, exfiltration, dfir]
level: practitioner
status: verified
description: "Reconstruct email sent and received over SMTP, POP3 and IMAP from pcaps: follow streams, export IMF objects, decode MIME and AUTH, and spot exfiltration."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html", "https://datatracker.ietf.org/doc/html/rfc5321", "https://datatracker.ietf.org/doc/html/rfc3501"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reconstructing SMTP, POP3 and IMAP sessions

**Goal:** recover whole messages and attachments from cleartext mail protocols in captures,
for phishing delivery, malware exfiltration over SMTP (a common route for info-stealers and
keyloggers), and insider leaks.

## Find the sessions
```
smtp || pop || imap
smtp.req.command == "AUTH" || smtp.req.command == "MAIL" || smtp.req.command == "RCPT"
smtp.data.fragment
tcp.port in {25, 465, 587, 110, 995, 143, 993}
```
Ports 465/993/995 are implicit TLS; 587/25/143/110 may upgrade with `STARTTLS` (after which
content is encrypted unless you have keys).

## Recover messages
- Follow > TCP Stream on an SMTP session: shows `EHLO`, `AUTH`, `MAIL FROM`, `RCPT TO`,
  `DATA` and the full RFC 5322 message.
- File > Export Objects > **IMF** saves each message as `.eml` (SMTP DATA and recognised
  messages); open in a mail client in the analysis VM or parse with Python's `email` package (`email.message_from_binary_file`; `python -m email` does not exist). Wireshark percent-encodes the subject in the file name (`/` becomes `%2f`).
- tshark: `tshark -r cap.pcapng -q --export-objects imf,mail_out`.
- POP3 `RETR` and IMAP `FETCH ... BODY[]` responses contain messages; IMF export covers many
  cases, otherwise save the stream as raw and cut out the message. In a test, the SMTP message exported whole (5723 bytes, attachment decoded intact) but the POP3 and IMAP messages came out as 1400-byte TCP-segment pieces, so use Follow Stream for those.

## Decode
- `AUTH LOGIN`: username and password base64 encoded on separate lines;
  `AUTH PLAIN`: base64 of `\0user\0password`. Decode: `echo <b64> | base64 -d`.
- Attachments: MIME parts with `Content-Transfer-Encoding: base64`; extract with
  the Python `email` package (`part.get_payload(decode=True)`); hash them.
- Info-stealer exfil mail usually puts host and user identifiers in the subject and lists harvested
  credentials in the body or attachments (screenshots, logs); the exact subject patterns are family
  specific, so take them from a current threat report for the family you suspect.

## Report items
Sender/recipient envelope (MAIL FROM/RCPT TO may differ from header From/To), server banner
and hostnames, client IP, authenticated account, timestamps, message hashes, attachment
hashes.

## Gotchas
- STARTTLS-protected sessions: only the pre-TLS commands are visible.
- Pipelining (`PIPELINING` extension) places several commands in one segment; read the stream,
  not single packets.
- Credentials seen in exfil traffic belong to victims: handle as sensitive data.

## Self-check
Each recovered message has a stream reference, envelope and header addresses, and attachment
hashes, and you stated whether parts of the session were encrypted.

## Checked
Run on Wireshark 4.4.1 against a synthetic capture (AUTH PLAIN on 587, AUTH LOGIN on 25, a multipart message with a
4000-byte base64 attachment over SMTP, POP3 RETR and IMAP FETCH): the filters matched (comma set required),
`smtp.data.fragment` fired on the multi-segment DATA, `--export-objects imf,<dir>` created the directory and wrote the
`.eml`, and Python `email` parsed it with the attachment intact. The AUTH PLAIN payload decodes to
NUL, user, NUL, password. Port roles (465 submissions, 587 submission, 993 imaps, 995 pop3s, 110, 143, 25) match the
IANA registry.
