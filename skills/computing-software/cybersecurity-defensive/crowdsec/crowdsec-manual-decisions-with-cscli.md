---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-manual-decisions-with-cscli
name: crowdsec-manual-decisions-with-cscli
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [cscli-decisions, manual-ban, decisions-list, decisions-delete, scope-value, decision-import]
level: practitioner
status: docs-checked
description: "Add, list, remove and import decisions by hand with cscli decisions, and understand scope, type and duration."
sources: ["https://docs.crowdsec.net/docs/cscli/cscli_decisions_add", "https://docs.crowdsec.net/docs/local_api/bouncers-api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```console
cscli decisions add --ip 1.2.3.4
cscli decisions add --range 1.2.3.0/24
cscli decisions add --ip 1.2.3.4 --duration 24h --type captcha
cscli decisions add --scope username --value foobar
```

Options: `-i/--ip` and `-r/--range` are shorthands for `--scope ip|range --value ...`; `-d/--duration` defaults to `4h`; `-t/--type` defaults to `ban` (the page lists `ban`, `captcha` and `throttle`); `--scope` defaults to `Ip` (the page lists `ip`, `range` and `username`); `-R/--reason` records a reason such as a scenario name; `-B/--bypass-allowlist` adds the decision even if the value is allowlisted.

## Checked

2026-11-03. Confirmed against the 'cscli decisions add' reference page: the four examples, all flags (-i, -r, -d, -v, --scope, -R, -t, -B) and the defaults 4h, ban and Ip. Removed: the claims about list/delete/import, the cscli and cscli-import origins, the 'manual ban from' reason text, stream-mode pickup and per-bouncer type support (the cited bouncers-api page returned 404 and the page does not state them).

Method: documentation only; no commands were run.
