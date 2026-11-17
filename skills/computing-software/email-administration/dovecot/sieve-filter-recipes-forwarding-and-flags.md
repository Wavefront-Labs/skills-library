---
id: computing-software.email-administration.dovecot.sieve-filter-recipes-forwarding-and-flags
name: sieve-filter-recipes-forwarding-and-flags
category: computing-software
field: email-administration
product: dovecot
tags: [sieve-script, if-elsif, redirect, addflag, lda-dupes, anyof]
level: intro
status: docs-checked
description: "Common Sieve recipes: foldering by header, forwarding with loop protection, flagging cron mail and keeping a copy of sent mail."
sources:
  - https://doc.dovecot.org/main/howto/sieve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
These are examples from the Sieve howto for users writing scripts.

Folder by header: chain `if address :is "to" "list@example.org"`, `elsif envelope :is "from" "..."`, and `anyof(...)` over header tests such as `X-listname` or `List-Id`. `anyof` is logical OR and `allof` is AND. Each branch uses `fileinto`.

Forwarding: `if header :contains "subject" ["order", "buy"]` then `redirect "other@address"`. To prevent mail loops Dovecot stores the Message-ID and recipient of forwarded messages in `.dovecot.lda-dupes` in the user's home directory.

Flagging: some mail readers show flags as labels. A rule can match `exists "X-Cron-Env"` or a `header :regex` over subjects like security, daily, weekly or monthly run output, then `addflag "$label1"`, which Thunderbird displays as Important (red).

Local copy of sent mail: `require ["envelope", "imap4flags"];` then `if envelope "from" "my_address@my_domain.com" { setflag "\\seen"; }` marks your own outgoing mail as seen. This is useful when you want Sieve to manage incoming and outgoing mail, and requires your mail reader to Bcc outgoing mail to your Dovecot address.

The examples declare the extensions they use at the top, for example `require ["fileinto", "envelope"];`, `require "imap4flags";` and `require "regex";`. The `:regex` header test needs `regex`, `addflag` needs `imap4flags`, and the `:detail` address part needs `subaddress`. The page also covers vacation replies, `include`, and other recipes not summarised here.

## Checked
2026-11-09. Read the whole Dovecot "Sieve Examples" page (doc.dovecot.org/main/howto/sieve.html) and confirmed the recipes above. Corrected the sent-mail recipe, which uses `setflag "\\seen"` rather than `fileinto`. Removed the unsupported claims about compile failure for disabled extensions and the `log_debug = category=sieve` hint.

Method: documentation only; no commands were run.
