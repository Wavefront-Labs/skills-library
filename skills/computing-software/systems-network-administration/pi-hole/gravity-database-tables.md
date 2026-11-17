---
id: computing-software.systems-network-administration.pi-hole.gravity-database-tables
name: gravity-database-tables
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [gravity-db-schema, adlist-status, domainlist-types]
level: advanced
status: docs-checked
description: "Understand gravity.db: domainlist, adlist, gravity, antigravity and client tables, including adlist status codes."
sources: ["https://docs.pi-hole.net/database/domain-database/", "https://docs.pi-hole.net/main/pihole-command/", "https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The gravity database

`/etc/pihole/gravity.db` is a SQLite3 database.

| Table | Content |
| --- | --- |
| `domainlist` | Allow and deny entries: `id`, `type`, `domain`, `enabled`, `date_added`, `date_modified`, `comment` |
| `adlist` | Subscribed list sources collected by `pihole -g` |
| `gravity` | Domains from enabled blocklists, rebuilt on every `pihole -g` |
| `antigravity` | Domains from subscribed allowlists, also rebuilt |
| `client` | Clients by IP address or CIDR subnet |

Dates are UNIX timestamps. Only `comment` may be `NULL`.

**adlist columns include** `address` (unique URL), `enabled`, `date_updated` (not updated if the list was unchanged), `number` (domains on the list) and `invalid_domains`.

**adlist.status**

| Value | Meaning |
| --- | --- |
| 1 | Download successful |
| 2 | Unchanged upstream; local copy used |
| 3 | Unavailable; local copy used |
| 4 | Unavailable; no local copy exists |

Uniqueness in `gravity` and `antigravity` is on (`domain`, `adlist_id`), so the same domain can appear once per list.

**Safe editing.** After manual SQL edits, run `pihole reloadlists`.

**Checklist**

1. Back up `gravity.db` first.
2. Edit with `sqlite3`.
3. Reload.
4. Check `adlist.status` when a list shows zero domains.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Domain Database (database/domain-database); The pihole Command (main/pihole-command); FTL Configuration Reference (ftldns/configfile). Removed the real-time signal 0 reload claim (not on the pages); `pihole reloadlists` is confirmed.
Method: documentation only; no commands were run.
