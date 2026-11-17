---
id: computing-software.networking-hardware-and-wireless.caddy.header-matchers
name: header-matchers
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [header-matcher, header-regexp, capture-groups, re-placeholders, re2, caddyfile]
level: practitioner
status: docs-checked
description: "Match request headers in Caddy with header and header_regexp: prefix, suffix, substring and absence forms, AND/OR combination, capture-group placeholders and RE2."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: classify requests by header.

`header <field> [<value>]`: a leading `!` on the field requires the field to be absent. A value starting with `*` is a suffix match, ending with `*` a prefix match, wrapped in `*` a substring match, otherwise exact. Different fields in one set are AND-ed; to accept several values of the same field, give one `header` matcher per value (OR-ed). Header fields can repeat, so backends must treat values as arrays. Examples: `@upgrade header Connection *Upgrade*`; `@foo { header Foo bar  header Foo baz }`; `@not_foo header !Foo`. WebSocket in CEL covers HTTP/2: `header({'Connection':'*Upgrade*','Upgrade':'websocket'}) || header({':protocol': 'websocket'})`.

`header_regexp [<name>] <field> <regexp>` uses Go's RE2. From v2.8.0 an omitted name is taken from the named matcher. Naming matters when you combine several regexp matchers (for example with `path_regexp`) in one set. Captures are available afterwards as `{re.<name>.<group>}` or the convenient `{re.<group>}`, which later regexp matchers overwrite; group 0 is the full match. Only one regexp per header field; use `expression` for more.

Example: `@login header_regexp login Cookie login_([a-f0-9]+)` gives `{re.login.1}` or `{re.1}`; the shorter `@login header_regexp Cookie login_([a-f0-9]+)` infers the name. CEL: `header_regexp('login', 'Cookie', 'login_([a-f0-9]+)')`.

## Checked

2026-11-03: read caddyfile/matchers against this skill. Confirmed: header value matching rules, ! absence, AND/OR behaviour, CEL forms, header_regexp naming from v2.8.0, {re.name.group} placeholders, RE2 and one regexp per field.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
