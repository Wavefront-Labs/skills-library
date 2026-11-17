---
id: computing-software.systems-network-administration.pi-hole.regex-filter-basics-and-hierarchy
name: regex-filter-basics-and-hierarchy
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [regex-filters, regex-reload, regex-debug]
level: practitioner
status: docs-checked
description: "Use regex denylist and allowlist filters in Pi-hole: POSIX ERE, how allowlists override them, reloading and debug logging."
sources: ["https://docs.pi-hole.net/regex/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Regex filters in FTL

A regex is a pattern for arbitrarily complex filter rules. FTL implements POSIX Extended Regular Expressions, like `egrep` (`grep -E`), extended with approximate matching and special features such as query-type matching. Each domain is checked once; later queries for it are not rechecked until `pihole-FTL` restarts.

**Hierarchy.** Allowlisting always wins over denylisting:

1. When loading blocking domains from the `gravity` table, FTL skips domains that are exactly allowlisted or match an enabled allowlist regex.
2. A query matching a regex denylist entry is not blocked if the domain also matches an exact or regex allowlist entry.

**Reload after changes.** FTL reads filters from the two `regex` database views. To make it reload:

- `pihole reloadlists` (preferred; keeps the DNS cache intact and is fastest)
- `sudo killall -SIGHUP pihole-FTL`
- restart the service

**Debugging.** Enable with `pihole-FTL --config debug.regex true`. Each match is then logged to `/var/log/pihole/FTL.log`, for example:

```text
Regex blacklist (DB ID 15) >> MATCH: "whatever.twitter.com" vs. "((^)|(\.))twitter\."
```

The DB ID is the row in the `domainlist` table. Only the first occurrence of a domain is validated; the result lives in an internal cache separate from dnsmasq's.

**Checklist**

1. Add the regex through the web interface or the domain database.
2. Run `pihole reloadlists`.
3. Test the domain; check the log if debug is on.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Regex Blocking (regex). Nothing needed removing.
Method: documentation only; no commands were run.
