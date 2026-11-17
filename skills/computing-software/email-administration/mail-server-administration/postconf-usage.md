---
id: computing-software.email-administration.mail-server-administration.postconf-usage
name: postconf-usage
category: computing-software
field: email-administration
product: mail-server-administration
tags: [postconf-usage, postconf, postconf-n, postconf-e]
level: intro
status: draft
description: "Use postconf to read, set and compare Postfix parameters safely: -n, -e, -d, -M, -m."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Postconf usage

**Goal:** inspect and change settings without opening main.cf blind.
## Commands
- `postconf -n`: settings changed from defaults. `postconf -d name`: built-in default.
- `postconf -e 'name = value'`: edit main.cf in place.
- `postconf -M`: master.cf services; `postconf -P` shows master.cf `-o` parameter overrides.
- `postconf -m`: lookup table types compiled in; `postconf -a` SASL server plugin types.
- `postconf smtpd_recipient_restrictions` prints one value; `postconf -x` expands $parameters.
## Failure modes
- `postconf -e` with unquoted spaces splits arguments.
- Using a table type not listed by `postconf -m` gives "unsupported dictionary type".
## Verify
- `postfix check` prints nothing; `postconf -n` after the edit shows the new value.
- A reload (`postfix reload`) logs no warnings in the mail log.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
