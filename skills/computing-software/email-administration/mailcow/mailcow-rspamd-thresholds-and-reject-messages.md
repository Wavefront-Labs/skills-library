---
id: computing-software.email-administration.mailcow.mailcow-rspamd-thresholds-and-reject-messages
name: mailcow-rspamd-thresholds-and-reject-messages
category: computing-software
field: email-administration
product: mailcow
tags: [spam-thresholds, actions-conf, reject-message, discard-on-reject, prefilter-reject, multimap, greylisting]
level: advanced
status: docs-checked
description: "Set server-wide spam score thresholds, custom reject text, silent discard and greylisting off in mailcow's Rspamd configuration files."
sources: ["https://docs.mailcow.email/manual-guides/Rspamd/u-e-rspamd-tweaks/", "https://docs.mailcow.email/manual-guides/Rspamd/u_e-rspamd-disable-greylisting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rspamd thresholds, reject text and greylisting

Server-wide thresholds go in `data/conf/rspamd/local.d/actions.conf`, for example `reject = 15;`, `add_header = 8;` and `greylist = 7;`. Restart rspamd-mailcow. Existing per-user settings are not overwritten; the docs describe a reset procedure that sources `mailcow.conf`.

Custom reject message: create `data/conf/rspamd/override.d/worker-proxy.custom.inc` with `reject_message = "My custom reject message";`. This does not affect prefilter reject actions. For those, find the symbol with `grep -R "SYMBOL" data/conf/rspamd/` and add a `message = "..."` line to the multimap entry, such as the `GLOBAL_RCPT_BL` block that sets `type = "rcpt"`, `prefilter = true` and `action = "reject"`.

Silent drop: put `discard_on_reject = true;` in the same `worker-proxy.custom.inc`.

Greylisting only applies to messages that already have a higher Rspamd score (soft rejected). The docs do not recommend disabling it, but it can be turned off server-wide by adding `enabled = false;` to `data/conf/rspamd/local.d/greylist.conf` and restarting rspamd-mailcow.

## Checked

2026-11-09. Confirmed on the Rspamd tweaks and disable-greylisting pages: actions.conf thresholds, existing user settings not overwritten, the filterconf reset, worker-proxy.custom.inc reject_message and discard_on_reject, the GLOBAL_RCPT_BL multimap message, and greylist.conf enabled = false. No changes needed.

Method: docs-checked 2026-11-09 against the full Rspamd tweaks and disable-greylisting pages (raw markdown in mailcow-dockerized-docs).
