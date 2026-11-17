---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.parsing-eml-msg-and-mbox-files
name: parsing-eml-msg-and-mbox-files
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [eml-msg, email-forensics, email-header-analysis, phishing-analysis, dfir]
level: practitioner
status: draft
description: "Parse EML, Outlook MSG and mbox evidence safely: MIME structure, extracting attachments and hashes, MSG properties, and preserving original bytes."
sources: ["https://datatracker.ietf.org/doc/html/rfc5322", "https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxmsg/", "https://github.com/TeamMsgExtractor/msg-extractor"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parsing EML, MSG and mbox files

**Goal:** examine individual email messages from user reports, exports or images without
executing content and without altering the original.

## Formats
| Format | What it is | Tools |
|---|---|---|
| EML | Raw RFC 5322 message with MIME parts | Any text editor, Python `email`, `emldump.py`, `ripmime` |
| MSG | Outlook OLE compound file with MAPI properties (MS-OXMSG) | `extract_msg`, `olefile`, `oledump.py` |
| mbox | Many RFC 5322 messages concatenated, separated by `From ` lines | `mailbox` module, Thunderbird (read-only copy) |

## Workflow
```bash
sha256sum message.eml                 # hash original first, work on a copy
python3 - <<'EOF'
import email, hashlib, email.policy
m = email.message_from_bytes(open("message.eml","rb").read(), policy=email.policy.default)
print(m["From"], m["Subject"], m["Date"], m["Message-ID"])
for part in m.walk():
    fn = part.get_filename()
    if fn:
        data = part.get_payload(decode=True)
        print(fn, part.get_content_type(), hashlib.sha256(data).hexdigest())
EOF
extract_msg --out out/ message.msg     # dumps body, headers, attachments from MSG
```
- MSG: transport headers are in property `PR_TRANSPORT_MESSAGE_HEADERS` (0x007D); without it
  (internal Exchange mail) rely on MAPI properties (`PR_CLIENT_SUBMIT_TIME`, sender SMTP address).
- mbox: count messages and verify none were skipped on parse (malformed `From ` lines split messages).

## Safety
- Never open attachments on the analysis host; hash and send to the malware lab or sandbox.
- HTML bodies may contain tracking pixels; render only offline.
- Defang URLs in notes (`hxxps://`).

## Gotchas
- Forwarded "as attachment" messages contain the original as `message/rfc822`; analyse the inner message headers, not the forwarder's.
- Users who forward phishing inline destroy original headers; ask for the original via the report button / message trace.

## Verify
Attachment hashes, headers and body are recorded from the original bytes, with the original hash in the evidence register.
