---
id: computing-software.email-administration.mailcow.mailcow-clamav-signature-whitelist
name: mailcow-clamav-signature-whitelist
category: computing-software
field: email-administration
product: mailcow
tags: [clamav, signature-whitelist, whitelist-ign2, virus-found, false-positive, clamd-mailcow]
level: advanced
status: docs-checked
description: "Allow a legitimate attachment type that ClamAV flags by adding its signature to whitelist.ign2 and clearing cached results."
sources: ["https://docs.mailcow.email/manual-guides/ClamAV/u_e-clamav-whitelist/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Whitelisting ClamAV signatures in mailcow

When clean mail is blocked, Rspamd flags it with `VIRUS_FOUND`. A typical case is interactive PDF forms, whose embedded JavaScript is reported as `PUA.Pdf.Trojan.EmbeddedJavaScript-1`. Read the `clamd-mailcow` container log to find the exact signature name; a line ends with `... FOUND`.

To allow that signature, append its name to `data/conf/clamav/whitelist.ign2`, for example `echo 'PUA.Pdf.Trojan.EmbeddedJavaScript-1' >> data/conf/clamav/whitelist.ign2`. Restart `clamd-mailcow` from the UI or with `docker compose restart clamd-mailcow`. Then clean cached ClamAV results from Redis, using the commands in the docs, which source `mailcow.conf` for the Redis password.

Whitelisting a signature disables detection of that signature for all mail, so use it only for names you have verified.

## Checked

2026-11-09. Confirmed on the ClamAV whitelist page: VIRUS_FOUND, the interactive PDF example and signature name, FOUND log check, whitelist.ign2 append, clamd restart and the rs_cl* Redis cleanup. Removed the unconfirmed SKIP_CLAMD sentence.

Method: docs-checked 2026-11-09 against the full ClamAV whitelist page (u_e-clamav-whitelist.en.md in mailcow-dockerized-docs).
