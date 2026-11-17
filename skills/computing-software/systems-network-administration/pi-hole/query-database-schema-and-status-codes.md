---
id: computing-software.systems-network-administration.pi-hole.query-database-schema-and-status-codes
name: query-database-schema-and-status-codes
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [queries-table, query-status-ids, sqlite-query-stats]
level: advanced
status: docs-checked
description: "Read pihole-FTL.db with SQLite: the queries view, status and reply type codes, and a sample top-domains query."
sources: ["https://docs.pi-hole.net/database/query-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Query database schema and codes

`/etc/pihole/pihole-FTL.db` stores the long-term history; FTL needs it to fill the last 24 hours after a restart. If the database is disabled, history is empty after a restart. If the file does not exist FTL creates it.

**Tables.** The `queries` view combines `query_storage` with the linking tables `domain_by_id`, `client_by_id`, `forward_by_id` and `addinfo_by_id`. Key columns: `timestamp`, `type`, `status`, `domain`, `client`, `forward`, `reply_type`, `reply_time`, `dnssec`. The `counters` table holds total queries (id 0) and blocked queries (id 1).

**Common status IDs**

| ID | Meaning |
| --- | --- |
| 1 | Blocked, in gravity |
| 2 | Allowed, forwarded |
| 3 | Allowed, from cache |
| 4 | Blocked, regex denylist |
| 5 | Blocked, exact denylist |
| 9 to 11 | Blocked during deep CNAME inspection |
| 15 | Blocked because the database is busy |
| 16 | Blocked special domain |
| 17 | Replied from stale cache |

Query types: 1 `A`, 2 `AAAA`, 3 `ANY`, 6 `PTR`, 16 `HTTPS`; types not listed are stored with an offset of 100.

**Sample query** for the three most queried domains:

```bash
sqlite3 "/etc/pihole/pihole-FTL.db" "SELECT domain,count(domain) FROM queries WHERE (STATUS == 2 OR STATUS == 3) GROUP BY domain ORDER BY count(domain) DESC LIMIT 3"
```

**Checklist**

1. Open read-only when exploring.
2. Filter on `status` rather than guessing.
3. Use the online backup before heavy queries.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Query Database (database/query-database). Nothing needed removing.
Method: documentation only; no commands were run.
