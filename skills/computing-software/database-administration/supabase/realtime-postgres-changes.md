---
id: computing-software.database-administration.supabase.realtime-postgres-changes
name: realtime-postgres-changes
category: computing-software
field: database-administration
product: supabase
tags: [realtime, postgres-changes, publication, replica-identity, filters]
level: practitioner
status: docs-checked
description: "Subscribe to Postgres changes in Supabase Realtime: publication SQL, filter operators, select columns, replica identity and scaling limits."
sources:
  - https://supabase.com/docs/guides/realtime/postgres-changes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stream row changes to clients.

```js
supabase.channel('schema-db-changes').on('postgres_changes', { event: '*', schema: 'public' }, callback).subscribe()
```

Add `table: 'todos'` to scope to one table; `event` is `INSERT`, `UPDATE`, `DELETE` or `*`. Add `filter: 'id=eq.1'` and `select: ['id', 'username']`. For a custom JWT call `supabase.realtime.setAuth('your-custom-jwt')` before subscribing. Builder: `postgresChangesFilter().gte('quantity', 10).eq('status', 'open')`.

SQL:

```sql
alter publication supabase_realtime add table your_table_name;
alter table messages replica identity full;
grant select on "non_private_schema"."some_table" to authenticated;
```

Operators: `eq`, `neq`, `lt`, `lte`, `gt`, `gte`, `in` (max 100 values), `like`/`ilike`, `match`/`imatch` (POSIX regex), `is` (null, true, false, unknown), `isdistinct`; prefix `not.` to negate.

Rules:
- Channel names can be anything except `realtime`.
- Filters run on the server. Multiple conditions combine as AND; OR is unsupported.
- Values containing `,`, `(`, `)`, `"` or `\` must be double-quoted.
- `is.true/false/unknown` need a boolean column; `like`, `ilike`, `match`, `imatch` need text.
- By default only the new record is sent; set `replica identity full` on the table to also receive the old record on UPDATE and DELETE. DELETE events can be filtered only with replica identity `full`, and RLS is not applied to DELETE because Postgres cannot verify access to a deleted record.
- `select` needs an explicit schema and table, is not supported on wildcard subscriptions, always includes the primary key, and its columns must be readable by the role.
- `public` works by default; for other schemas grant `select` to the database role in the access token. The page strongly encourages RLS and policies on tables in private schemas, since otherwise any granted role has unfettered read access.
- Set a custom JWT with `supabase.realtime.setAuth(...)` after creating the client and before joining a channel; never expose the `service_role` token on the client.
- Authorization runs per subscriber (one check per user for each change) and changes are processed on a single thread to preserve order, so larger compute add-ons do not meaningfully raise throughput. Filters, column selection and cheap indexed RLS policies help. If you expect more than about 3,000 concurrent subscribers on the same changes, the page advises using Broadcast.

## Checked

2026-11-04: Read the Postgres Changes guide in full. Confirmed the client calls, publication SQL, every filter operator and its type requirement, the quoting rule, `select` restrictions, replica identity behaviour, private schema grants, custom tokens and the scaling advice. Added the replica-identity, private-schema and single-thread details.
Method: documentation only; no commands were run.
