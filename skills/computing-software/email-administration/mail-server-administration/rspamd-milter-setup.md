---
id: computing-software.email-administration.mail-server-administration.rspamd-milter-setup
name: rspamd-milter-setup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [rspamd-milter-setup, rspamd, rspamd-milter, rspamc, rspamadm]
level: practitioner
status: draft
description: "Integrate Rspamd with Postfix as a milter and set up the controller password, DKIM signing module and logging."
sources:
  - https://rspamd.com/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rspamd milter setup

**Goal:** modern filtering through the milter protocol.
## Steps
1. `/etc/rspamd/local.d/worker-proxy.inc`: `milter = yes; timeout = 120s; upstream "local" { default = yes; self_scan = yes; }` with `bind_socket = "localhost:11332"`.
2. Postfix `smtpd_milters = inet:localhost:11332`, `milter_default_action = accept`, `milter_mail_macros = i {mail_addr} {client_addr} {client_name} {auth_authen}`.
3. Controller password: `rspamadm pw`, put hash in `worker-controller.inc`.
4. Check config: `rspamadm configtest`.
## Failure modes
- Editing files in `/etc/rspamd` instead of `local.d`/`override.d`: package upgrades overwrite.
## Verify
- `rspamc stat`; headers like `X-Rspamd-Result` or the web UI show scores.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
