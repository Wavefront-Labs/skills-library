---
id: computing-software.data-engineering.snowflake.cloning-grants-and-dependent-objects
name: cloning-grants-and-dependent-objects
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, zero-copy-clone, clone-grants, copy-grants, cloned-pipes, cloned-streams, cloned-tasks, dev-environments]
level: practitioner
status: docs-checked
description: "Know what a Snowflake zero-copy clone carries over: grants (COPY GRANTS), pipes, streams, tasks, sequences, stages and policies, and avoid surprises in cloned environments."
sources:
  - https://docs.snowflake.com/en/user-guide/object-clone
  - https://docs.snowflake.com/en/sql-reference/sql/create-clone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clone behaviour: grants and dependent objects

**Goal:** clones used for dev/test/recovery behave predictably: right access, no duplicate ingestion, no tasks firing against prod.

## Privileges
- Cloning a **database or schema**: the clone does not inherit the privileges granted on the source container itself; read the cloning considerations page for how child-object privileges are handled.
- Cloning a **table**: privileges are not copied unless `COPY GRANTS`:
```sql
create table dev.sales.orders clone prod.sales.orders copy grants;
```
- A cloned table does not inherit future grants defined for its object type in the schema.

## Dependent objects in database/schema clones
| Object | Behaviour in clone |
|---|---|
| Tables, views, sequences | cloned; a cloned table with a default sequence references the cloned sequence when the sequence is in the cloned container |
| Streams | cloned only when a database or schema containing the table and stream is cloned (cloning a table directly does not clone its streams); unconsumed records in the cloned stream are inaccessible |
| Tasks | cloned **suspended** |
| Pipes | only pipes that reference external stages are cloned; internal pipes are not. Default state depends on AUTO_INGEST (see create-clone page) |
| Named stages | external stages present at clone start are cloned; internal named stages are cloned only with `INCLUDE INTERNAL STAGES` |
| Hybrid tables, Iceberg tables | restrictions apply (check docs per type) |

## Safe dev-clone recipe
```sql
create or replace database dev_alice clone prod;
-- tasks are suspended; keep them so, or point them to dev warehouses before resuming
-- check the state of cloned pipes (SHOW PIPES) so dev does not ingest prod files
alter database dev_alice set data_retention_time_in_days = 1;   -- reduce Time Travel storage on the clone
grant usage on database dev_alice to role dev_alice_role;
```

## Clone at a point in time
```sql
create table recover.orders clone prod.sales.orders at (timestamp => '2026-10-17 06:00:00'::timestamp_ltz);
create schema prod.sales_restore clone prod.sales before (statement => '01b2...');
```

## Gotchas
- A clone is writable and independent of its source: changes to either are not reflected in the other.
- A cloned table does not include the load history of the source, so files loaded into the source can be loaded again into the clone.

## Verify
- [ ] `show grants on table dev.sales.orders` shows expected access.
- [ ] `show tasks in database dev_alice` all `suspended`; `show pipes` states checked.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: COPY GRANTS on table clone, no inheritance of container or future grants, tasks cloned suspended, pipes cloned only for external stages, INCLUDE INTERNAL STAGES, streams cloned only with a containing database/schema and unconsumed records inaccessible, sequence behaviour, clone independence and load history (object-clone and create-clone pages).

Removed or corrected: the wrong stream-offset claim (unconsumed records are inaccessible in the clone, not shared), the wrong 'internal stages not cloned' claim, external-table and policy rows, owner-role and Time Travel bullets (not on the pages read).

Method: documentation only; no commands were run.
