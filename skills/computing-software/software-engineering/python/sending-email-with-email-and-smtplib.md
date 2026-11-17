---
id: computing-software.software-engineering.python.sending-email-with-email-and-smtplib
name: sending-email-with-email-and-smtplib
category: computing-software
field: software-engineering
product: python
tags: [python, py-internet, email-smtplib, smtplib, emailmessage, starttls, mime, attachments, header-injection]
level: practitioner
status: docs-checked
description: "Build messages with email.message.EmailMessage (text, HTML alternative, attachments) and send them over SMTP with STARTTLS or SSL, without header injection or credential leaks."
sources: ["https://docs.python.org/3/library/email.message.html", "https://docs.python.org/3/library/smtplib.html", "https://docs.python.org/3/library/email.examples.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sending email with email and smtplib

```python
import smtplib, ssl, mimetypes
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

msg = EmailMessage()
msg["From"] = "Alerts <alerts@example.com>"
msg["To"] = "ops@example.com, dev@example.com"
msg["Subject"] = "Nightly report"
msg["Date"] = formatdate(localtime=True)
msg["Message-ID"] = make_msgid(domain="example.com")
msg.set_content("Plain text body")                         # always provide text
msg.add_alternative("<h1>Report</h1><p>OK</p>", subtype="html")

ctype, _ = mimetypes.guess_type("report.pdf")
maintype, subtype = (ctype or "application/octet-stream").split("/")
with open("report.pdf", "rb") as f:
    msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename="report.pdf")

ctx = ssl.create_default_context()
with smtplib.SMTP("smtp.example.com", 587, timeout=20) as s:   # submission port + STARTTLS
    s.starttls(context=ctx)
    s.login(user, password)                 # read from env/secret store, never hard-coded
    s.send_message(msg)
# Implicit TLS: smtplib.SMTP_SSL("smtp.example.com", 465, context=ctx)
```

## Rules
- Use the `EmailMessage` API (its default policy follows the email RFCs, serialising with `\n` line endings), not hand-assembled MIME parts.
- `add_alternative()` adds a multipart/alternative part and `add_attachment()` a multipart/mixed part with `Content-Disposition: attachment`.
- `SMTP_SSL` is for connections where TLS is required from the start; otherwise use `SMTP.starttls(context=...)`.

## Gotchas
- Never put unvalidated user input with newlines into headers.
- `send_message` takes recipients from the To, Cc and Bcc headers when `to_addrs` is None, and does not transmit any Bcc header; `sendmail` leaves headers untouched and uses the envelope you pass.
- Set a `timeout` (seconds) on `SMTP`/`SMTP_SSL`; without one the global default applies, and a value of zero raises `ValueError` (3.9+).

## Verify
- [ ] Send to a local capture server and open the raw message: boundary parts, `Content-Type`, attachment filename correct.
- [ ] Credentials come from the environment or a secret store.

## Checked

2026-11-08. Confirmed on the email.message and smtplib pages: `EmailMessage(policy=default)` and its line-ending note, `set_content()`, `add_alternative()` (multipart/alternative), `add_attachment()` (multipart/mixed, attachment disposition), `SMTP(host, port, local_hostname, timeout, source_address)`, `SMTP_SSL` purpose, `starttls(*, context=None)`, `send_message` recipient extraction from To/Cc/Bcc and Bcc not transmitted, `sendmail` envelope behaviour, the timeout `ValueError` for zero (3.9). Removed: the claim that `EmailMessage` raises `ValueError` for newline headers, port 25/587/465 advice, deliverability remark, removal of `smtpd` in 3.12, the dev-server suggestions and the wrong advice to pass `to_addrs` for Bcc.

Method: docs-only read of cited pages, 2026-11-08
