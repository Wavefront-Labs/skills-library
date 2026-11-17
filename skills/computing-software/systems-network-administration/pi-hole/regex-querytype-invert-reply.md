---
id: computing-software.systems-network-administration.pi-hole.regex-querytype-invert-reply
name: regex-querytype-invert-reply
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [regex-querytype, regex-invert, regex-reply]
level: advanced
status: docs-checked
description: "Use Pi-hole's regex extensions: ;querytype=, ;invert and ;reply= to filter by record type and choose the blocked response."
sources: ["https://docs.pi-hole.net/regex/pi-hole/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Regex extensions: querytype, invert, reply

Append keywords after the regex, separated by `;`.

**Query type.** `abc;querytype=AAAA` blocks `dig AAAA abc` but not `dig A abc`. Multiple types are comma-separated, and `!` inverts:

- `.*;querytype=!A`: denylist everything except `A`; one user-provided example for devices such as Chromecast.
- `.*;querytype=PTR`: an allowlist entry to permit PTR lookups next to the above.
- `.*;querytype=ANY`: block `ANY` network-wide.
- `.*;querytype=OTHER`: block query types not otherwise covered, such as `IXFR` and `AXFR`.
- `.*;querytype=!A,AAAA`: everything except `A` and `AAAA`.

**Invert.** `^abc$;invert` does not block `abc` but blocks everything else for the group's clients. `^abc$;querytype=AAAA;invert` is independent per query type.

**Reply type.** `;reply=` selects the answer: `nodata`, `nxdomain` (can cause unintended side-effects), `refused`, `none` (silently dropped), `ip` (the Pi-hole address unless `reply.blocking.IPv4/IPv6` overrides), or an IPv4 or IPv6 address. Give one option, except an IPv4 plus an IPv6 address:

```text
myregex;reply=1.2.3.4;reply=fe80::1234
```

An IPv4-only reply returns `A 1.2.3.4` and `AAAA ::`.

**Comments:** `(?#some comment)` text is ignored by the parser (it cannot contain `)`).

**Checklist**

1. Add the extension suffix after the pattern.
2. Run `pihole reloadlists`.

## Checked

2026-11-03. Read the Pi-hole regex extensions page (query types and the five examples, `OTHER`, comma lists and `!`, `;invert`, all `;reply=` options and the IPv4/IPv6 outcomes, comments) and the Regex Blocking page (`pihole reloadlists`). Removed the dig verification item.

Method: documentation only; no commands were run.
