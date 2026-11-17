---
id: computing-software.email-administration.mailcow.mailcow-rspamd-learning-spam-and-ham
name: mailcow-rspamd-learning-spam-and-ham
category: computing-software
field: email-administration
product: mailcow
tags: [bayes, learn-spam, learn-ham, fuzzy-storage, imapsieve, reset-learned-data, neural]
level: advanced
status: docs-checked
description: "How mailcow trains Rspamd from the junk folder, bulk-learns existing mail with rspamc and resets Bayes, neural or fuzzy data in Redis."
sources: ["https://docs.mailcow.email/manual-guides/Rspamd/u-e-rspamd-work-with-spamdata/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Training Rspamd with spam and ham

Rspamd learns a message as spam or ham when a user moves it into or out of the junk folder to any mailbox other than trash. This uses the Dovecot Sieve plugin `sieve_imapsieve` with parser scripts. Rspamd also auto-learns on very high or low scores, and mailcow configures it to keep a sane spam to ham ratio. Bayes statistics are Redis keys `BAYES_HAM` and `BAYES_SPAM`. A local fuzzy storage learns recurring text or image patterns. The Rspamd web UI can also learn ham and spam.

Bulk learning from plain-text maildir files:
- ham: `for file in /my/folder/cur/*; do docker exec -i $(docker compose ps -q rspamd-mailcow) rspamc learn_ham < $file; done`
- spam: the same loop over `.Junk/cur/*` with `rspamc learn_spam`.
For compressed mail, attach a folder as a volume to rspamd-mailcow and decompress with `zcat` inside the container.

Resetting learned data means deleting Redis keys, so first copy `dump.rdb` from the Redis volume (preferably with Redis stopped). Separate procedures reset Bayes data, neural data and fuzzy data; the fuzzy reset runs a Lua `EVAL` in `redis-cli` that deletes keys matching `fuzzy*`.

## Checked

2026-11-09. Confirmed on the Rspamd spam data page: sieve_imapsieve learning, autolearn, BAYES_HAM and BAYES_SPAM keys, fuzzy storage, the rspamc learn loops, zcat workaround, Redis dump.rdb copy and the Bayes, neural and fuzzy reset procedures. No changes needed.

Method: docs-checked 2026-11-09 against the full Rspamd spam data page (raw markdown in mailcow-dockerized-docs).
