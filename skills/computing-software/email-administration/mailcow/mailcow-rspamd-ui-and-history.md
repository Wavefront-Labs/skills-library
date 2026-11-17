---
id: computing-software.email-administration.mailcow.mailcow-rspamd-ui-and-history
name: mailcow-rspamd-ui-and-history
category: computing-software
field: email-administration
product: mailcow
tags: [rspamd, rspamd-ui, rspamd-history, rspamc, ratelimit-keys, history-redis]
level: practitioner
status: docs-checked
description: "Open the Rspamd web UI in mailcow, increase its history length and wipe ratelimit keys from Redis."
sources: ["https://docs.mailcow.email/manual-guides/Rspamd/u_e-rspamd-general/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rspamd UI, history and ratelimit keys in mailcow

Rspamd handles antivirus integration, DKIM signing and spam filtering in mailcow. Its web UI is included but its password is random after installation, so first set your own: as administrator open the System Configuration tab (top left), then the Access Rspamd UI sub-tab, set the password, then browse to `https://${MAILCOW_HOSTNAME}/rspamd`.

Rspamd also offers command line tools (for example `rspamc` and `rspamadm`) inside the `rspamd-mailcow` container.

History: by default 1000 elements are kept, stored compressed. Edit `data/conf/rspamd/local.d/history_redis.conf` and change `nrows = 1000;`. The docs suggest trying 5000 or 10000 rather than a disproportionately high value and watching how the server copes. Restart rspamd-mailcow afterwards.

Ratelimit keys: to wipe all of them without the UI, run `redis-cli --scan --pattern RL* | xargs redis-cli unlink` inside the Redis container (UNLINK, available in Redis 4 and later, deletes in the background), then restart Rspamd.

## Checked

2026-11-04. Confirmed on the Rspamd General Settings page: UI purpose and random initial password, the admin menu path to set it, the /rspamd URL, rspamc and rspamadm in rspamd-mailcow, history default of 1000 elements stored compressed, history_redis.conf nrows and the 5000 or 10000 suggestion, and the redis-cli unlink command for RL* keys with a Rspamd restart. Fixed: menu path now matches the page wording (UI labels not re-verified in a running system).

Method: documentation only; no commands were run.
