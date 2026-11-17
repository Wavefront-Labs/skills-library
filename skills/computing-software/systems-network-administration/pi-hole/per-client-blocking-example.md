---
id: computing-software.systems-network-administration.pi-hole.per-client-blocking-example
name: per-client-blocking-example
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [per-client-blocking, exclude-client-from-blocking, group-lists]
level: advanced
status: docs-checked
description: "Walk through per-client blocking with groups: exclude a client, give it its own blocklist, and apply group-only deny or allow entries."
sources: ["https://docs.pi-hole.net/group_management/example/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Per-client blocking with groups

Setup: three groups (1, 2, 3), three clients (`192.168.0.101` to `.103`) each linked to one group via `client_by_group`. Others stay on Default.

**Exclude a client from blocking.** Remove its Default membership:

```sql
DELETE FROM client_by_group WHERE client_id = 1 AND group_id = 0;
```

Client 1 is then completely unblocked, because removing group 0 removes association with all subscribed lists and domains.

**Give it a specific list:**

```sql
INSERT INTO adlist_by_group (adlist_id, group_id) VALUES (1,1);
```

Client 1 now uses only that list.

**Deny a domain for one group.** Add the domain (`type` 1 is exact deny), link it to group 1, then remove it from group 0 so the rest of the network is unaffected:

```sql
INSERT INTO domainlist (type, domain, comment) VALUES (1, 'denylisted.com', 'Denylisted for members of group 1');
INSERT INTO domainlist_by_group (domainlist_id, group_id) VALUES (1, 1);
DELETE FROM domainlist_by_group WHERE domainlist_id = 1 AND group_id = 0;
```

Check the `domainlist_id` with `SELECT last_insert_rowid();`.

**Reload.** Run `pihole reloadlists` after database modifications so FTL flushes its domain-blocking cache, separate from the DNS cache.

**Checklist**

1. Use the web interface where possible.
2. Run the SQL only after backing up `gravity.db`.
3. Reload and test per client.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Per-client blocking example (group_management/example). Nothing needed removing.
Method: documentation only; no commands were run.
