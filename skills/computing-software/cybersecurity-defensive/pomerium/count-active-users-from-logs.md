---
id: computing-software.cybersecurity-defensive.pomerium.count-active-users-from-logs
name: count-active-users-from-logs
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [usage-tracking, databroker-sql, session-records, billing-users, authorize-log]
level: practitioner
status: docs-checked
description: "Identify active Pomerium users for usage or billing from authorize log user and email keys, or query sessions from the databroker Postgres database."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/audit-logs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To find which users are active (for example for billing), use either source.

1. Authorization logs: read the `user` and `email` keys on authorize entries (see find-authorize-logs for how to filter them).

2. Databroker database: if the databroker uses Postgres, session records hold the same data. The documented query is:

```sql
SELECT id AS session_id,
       data#>>'{userId}' AS user_id,
       data#>>'{claims,name,0}' AS user_display_name,
       data#>>'{claims,email,0}' AS user_email
FROM pomerium.records
WHERE "type" = 'type.googleapis.com/session.Session'
```

Notes:
- The query reads the session record type, so it returns sessions; one user can have several sessions with the same user ID.
- The page presents the query for the Postgres database used by the Databroker.

## Checked

2026-11-04. Confirmed against the Audit Logs page: user and email log keys and the exact SQL query. Removed the in-memory backend claim, the count-distinct advice and the array-index explanation, which the page does not state.

Method: documentation only; no commands were run.
