---
id: computing-software.email-administration.dovecot.sieve-extension-settings-vacation-extlists-editheader
name: sieve-extension-settings-vacation-extlists-editheader
category: computing-software
field: email-administration
product: dovecot
tags: [sieve-vacation, sieve-extlists, sieve-editheader, resource-limits, implicit-delivery, duplicate-extension]
level: advanced
status: docs-checked
description: "Per-extension Sieve settings: vacation implicit-delivery check and periods, extlists dict lists, editheader forbidden headers and size limit."
sources:
  - https://doc.dovecot.org/main/core/config/sieve/extensions/vacation.html
  - https://doc.dovecot.org/main/core/config/sieve/extensions/extlists.html
  - https://doc.dovecot.org/main/core/config/sieve/extensions/editheader.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vacation: a setting controls whether the check for implicit delivery runs. Skipping it means vacation does not verify that the message is explicitly addressed to the recipient. Turning it off violates the Sieve standard and can send vacation replies for messages not directly addressed to the user, so do so with caution.

Extlists: a named list filter defines a list for the `:list` match type. The filter name refers to `sieve_extlists_list_name`, which is the name Sieve scripts use. A `dict` definition inside the list filter serves as the lookup, so values from Sieve are looked up there. This is often used for an address book or whitelist kept outside the script. If no dict is present, the list acts as empty.

Editheader: a header filter configures a header that may be forbidden from being added or deleted. The filter name refers to `sieve_editheader_header_name`. Set `forbid_add` and `forbid_delete` inside the filter. Subject can never be protected, and deleting Received and Auto-Submitted is always forbidden. `sieve_editheader_max_header_size` defaults to 2k, minimum 1024 bytes.

Vacation periods: `sieve_vacation_min_period` (default 1d), `sieve_vacation_default_period` (default 7d) and `sieve_vacation_max_period` (default 60d, 0 means no limit). Extlists: `sieve_extlists_list_max_lookup_size` defaults to 1k.

Remember that extlists and editheader are not enabled by default; enable them in the extension settings first. Vacation tracks replied senders in a `.dovecot.lda-dupes` file in the user's home directory.

## Checked

2026-11-03. Confirmed on the Sieve vacation, extlists and editheader pages: sieve_vacation_check_recipient (default yes; no violates the standard), the vacation period defaults, sieve_extlists_list with sieve_extlists_list_name and the dict lookup (empty list without a dict), sieve_editheader_header with its name, forbid_add and forbid_delete settings, extlists and editheader not enabled by default, and the .dovecot.lda-dupes file in the home directory. Removed: the variables, include and duplicate limits (including "minimum 128"), which are on pages not read in this review.

Method: documentation only; no commands were run.
