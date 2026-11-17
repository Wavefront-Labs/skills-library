---
id: computing-software.email-administration.dovecot.sieve-spam-and-virus-filtering-patterns
name: sieve-spam-and-virus-filtering-patterns
category: computing-software
field: email-administration
product: dovecot
tags: [sieve-spamtest, sieve-virustest, x-spam-flag, i-ascii-numeric, subaddress, relational]
level: practitioner
status: docs-checked
description: "File or discard scanner-tagged mail by header, use spamtest and virustest scores, and avoid the ascii-numeric comparator pitfall."
sources:
  - https://doc.dovecot.org/main/howto/sieve.html
  - https://doc.dovecot.org/main/core/config/sieve/extensions/spamtest_virustest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Most scanners add a header. You can test it directly, which works whenever the scanner adds it, or use the spamtest and virustest extensions for a uniform view.

Direct header tests:
- SpamAssassin flag: `header :contains "X-Spam-Flag" "YES"` then `fileinto "Spam"`.
- Discard at level 10 or higher: `header :contains "X-Spam-Level" "**********"`.
- Numeric score only: combine `not header :matches "x-spam-score" "-*"` with `header :value "ge" :comparator "i;ascii-numeric" "x-spam-score" "10"`. The `i;ascii-numeric` comparator handles only unsigned integers, and strings not starting with a digit count as positive infinity, so always guard against negative scores first.

With the extensions configured on the server, users can write portable rules:
- `spamtest :value "eq" :comparator "i;ascii-numeric" "0"` catches a failed test, for example a missing header; file it separately.
- Scores range 1-10; `"ge" "3"` can go to a spam folder.
- `:percent` compares relative to the maximum, for example discard above 85 percent.
- `virustest` uses 1-5: 0 means not scanned, 4 is probably infected (quarantine), 5 definitely infected.

Some scanners put the maximum score in a status header, and the server setting for spamtest can extract it from the message instead of a fixed value, using the format header-field plus optional regexp. That setting cannot be combined with the fixed-maximum one.

The `spamtest`, `spamtestplus` and `virustest` extensions are not enabled by default; enable them with `sieve_extensions`. If no matching header is found, or the header does not match the configured regexp, `spamtest` matches against 0. `sieve_spamtest_status_type` is `score`, `strlen` (a string of identical characters such as `*******`) or `text` (values mapped with `sieve_spamtest_text_value`, scores 0 to 10 recognised); the virustest settings mirror the spamtest ones.

Subaddress example: `envelope :detail "to" "spam"` matches user+spam@example.com, useful for tags without creating folders for arbitrary +tags.

## Checked
2026-11-09. Read the Dovecot "Sieve" how-to (spam and virus filtering and plus-addressing sections) and the "Spamtest and Virustest Extensions" page in full, and confirmed all examples, ranges and settings above. Added the enablement and status-type details from the second page.

Method: documentation only; no commands were run.
