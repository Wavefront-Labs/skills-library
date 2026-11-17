---
id: computing-software.email-administration.dovecot.login-proxy-failure-states-reading
name: login-proxy-failure-states-reading
category: computing-software
field: email-administration
product: dovecot
tags: [login-proxy, proxy-state, timed-out, imap-states, pop3-xclient, submission-ehlo]
level: advanced
status: docs-checked
description: "Decode proxy log messages such as timed out in state=login/banner to see which command was sent and which reply was last received."
sources:
  - https://doc.dovecot.org/main/core/admin/login_proxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Login-process proxying covers IMAP, POP3, submission and ManageSieve. LMTP and doveadm do their own proxying but stay mostly compatible. When a proxy login fails, the error shows the connection state at disconnect or timeout.

IMAP state is `sent/received`. A message like `timed out in state=login/banner` means the timeout came while waiting for the LOGIN reply (the banner was the last thing received). `capability+login/banner` means CAPABILITY and LOGIN were pipelined and only the banner arrived.

IMAP sent states: `id` (session ID and original client IP/port), `starttls`, `capability` (only if the backend does not send it), `login`, `authenticate` (when LOGIN is not usable, such as master user login or non-cleartext mechanisms), and `auth-continue` (SASL continuation). Received states: `none`, `banner` ("* OK Dovecot ready"), `id`, `starttls`, `capability` (command replies received), `auth-continue` (a + reply), and `login` (LOGIN or AUTHENTICATE reply received).

POP3 states: `banner` (nothing received, banner not yet seen), `starttls` (STLS sent), `xclient`, `login1` (USER sent), `login2` (PASS or AUTH sent).

Submission states: `banner`, `ehlo` (EHLO sent), `starttls`, `tls-ehlo` (EHLO after STLS sent), `xclient`, `authenticate` (AUTH sent).

ManageSieve states: `none`, `tls-start` (STARTTLS sent), `tls-ready` (accepted; handshake starting), `xclient`, `auth`.

Reading it: the sent side names the command the proxy was waiting on, and the received side is the last reply it got. For POP3, submission and ManageSieve the banner/none state means nothing has been received from the backend yet. The page lists states only; it gives no causes, so look at the backend for the stage that stalled.

## Checked
2026-11-09. Read the whole Dovecot "Login Process Proxying" page (doc.dovecot.org/main/core/admin/login_proxy.html; the old main/admin/ URL is a script shell with no text, so the source was replaced). Confirmed all state names and descriptions for IMAP, POP3, submission and ManageSieve. Completed the IMAP state lists with the entries the page lists that the draft omitted; removed the unsupported cause diagnosis (unreachable backend, hanging authentication) and the advice about timeouts.

Method: documentation only; no commands were run.
