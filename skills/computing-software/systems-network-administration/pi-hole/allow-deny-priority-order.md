---
id: computing-software.systems-network-administration.pi-hole.allow-deny-priority-order
name: allow-deny-priority-order
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [domain-priority, allowlist-wins, denylist-order]
level: practitioner
status: docs-checked
description: "Know the exact order Pi-hole uses to decide whether a domain is allowed or blocked across all list types."
sources: ["https://docs.pi-hole.net/database/domain-database/", "https://docs.pi-hole.net/group_management/", "https://docs.pi-hole.net/database/query-database/", "https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Allow and deny priority

When deciding whether to block, Pi-hole checks in this order:

1. Exact allowlist entries
2. Regex allowlist entries
3. Exact denylist entries
4. Subscribed allowlists
5. Subscribed denylists
6. Regex denylist entries

**Reading the order.** An earlier rank beats a later one, so an exact allowlist entry beats every other list, and an exact denylist entry beats subscribed allowlists. Subscribed allowlists were added in Pi-hole v6.0; the database-based domain management came in v5.0.

**Domain table.** `domainlist.type` stores `0` exact allow, `1` exact deny, `2` regex allow, `3` regex deny. Disabled domains are omitted when FTL reads the views.

**Troubleshooting a wrongly blocked or allowed domain**

- Check the query log entry; its status tells whether gravity, an exact denylist or a regex blocked it.
- Compare against the order: a regex deny is last, so any allow entry defeats it.
- Remember group membership: an entry only applies to clients in its groups.

**Checklist**

1. Prefer an exact allowlist entry to fix a false positive.
2. Use regex allowlist entries for families of domains.
3. Run `pihole reloadlists` after database edits.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Domain Database (database/domain-database); Group Management (group_management); Query Database (database/query-database); The pihole Command (main/pihole-command). Nothing needed removing.
Method: documentation only; no commands were run.
