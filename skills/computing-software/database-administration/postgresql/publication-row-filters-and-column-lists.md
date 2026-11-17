---
id: computing-software.database-administration.postgresql.publication-row-filters-and-column-lists
name: publication-row-filters-and-column-lists
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-logical-replication, logical-replication, publication-row-filter, column-lists, create-publication, replica-identity, publish-via-partition-root]
level: practitioner
status: verified
description: "Publish only some rows and columns over PostgreSQL logical replication with WHERE row filters and column lists, and avoid the replica-identity traps."
sources:
  - https://www.postgresql.org/docs/current/logical-replication-row-filter.html
  - https://www.postgresql.org/docs/current/logical-replication-col-lists.html
  - https://www.postgresql.org/docs/current/sql-createpublication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publication row filters and column lists (15+)

**Goal:** replicate a subset (one tenant, one region, no PII columns) to a subscriber without triggers or views.

## Syntax
```sql
CREATE PUBLICATION eu_orders
  FOR TABLE orders (id, customer_id, region, total, created_at) WHERE (region = 'eu'),
            customers (id, region, country) WHERE (region = 'eu');
ALTER PUBLICATION eu_orders SET TABLE orders (id, customer_id, region, total, created_at) WHERE (region IN ('eu','uk'));
```
Inspect: `SELECT * FROM pg_publication_tables WHERE pubname = 'eu_orders';` (shows `rowfilter` and `attnames`).

## Rules that bite
- **The example above fails on `UPDATE`/`DELETE` as written** (PG17): with the default replica identity (`id`) the filter column `region` is not covered (`Column used in the publication WHERE expression is not part of the replica identity`), and `REPLICA IDENTITY FULL` with a column list that omits any column fails with `Column list used by the publication does not cover the replica identity`. Make the filter column part of a replica identity index, e.g. `CREATE UNIQUE INDEX ON orders (id, region); ALTER TABLE orders REPLICA IDENTITY USING INDEX orders_id_region_idx;` (region NOT NULL) and keep `id, region` in the column list; that variant replicated updates, deletes and region migrations.
- **UPDATE/DELETE with a row filter:** columns in the WHERE must be covered by the table's replica identity, otherwise those operations error on the publisher (`cannot update table ... column used in the publication WHERE expression is not part of the replica identity`). Keep filters on PK columns or `ALTER TABLE ... REPLICA IDENTITY FULL` (costly).
- **Column lists:** must include all replica identity columns if the publication publishes UPDATE/DELETE.
- Filter expressions allow only simple immutable built-ins; no user functions, subqueries, or non-immutable calls (`now()`).
- **Row migrations:** an UPDATE moving a row into the filter is sent as INSERT, out of the filter as DELETE. Old and new values are both evaluated.
- Initial table sync applies the filter too, so the subscriber starts with only matching rows.
- Several publications on one subscription with different filters for the same table combine with OR; a publication without a filter means all rows.
- Partitioned tables: `publish_via_partition_root = true` makes the root's filter apply; otherwise each partition's own.

## Subscriber side
Subscriber table may have extra columns (defaults) but must have all published columns with compatible types.

## Gotchas
- Column lists are not a security boundary against a superuser on the publisher; they do keep PII off the subscriber.
- Changing a filter does not resync existing data: rows already on the subscriber stay. `REFRESH PUBLICATION WITH (copy_data = true)` does NOT re-copy a table already in the subscription (tested: nothing copied even after truncating the subscriber table). To resync, `ALTER PUBLICATION ... DROP TABLE t`, `REFRESH PUBLICATION`, `ADD TABLE` again, `REFRESH PUBLICATION WITH (copy_data = true)` (that copied the rows), or recreate the subscription.

## Verify
Insert a row outside the filter on the publisher; it must not appear on the subscriber. Update a filter-column value to move a row in and out and watch INSERT/DELETE on the subscriber.

## Checked
- PostgreSQL 17.6 publisher and subscriber: `pg_publication_tables` shows `attnames` and `rowfilter`; mutable functions (`now()`), user functions and subqueries in `WHERE` are rejected with `invalid publication WHERE expression`; the initial sync honoured the filter; with an index replica identity covering `id, region`, an update moving a row into the filter arrived as an INSERT, one moving out as a DELETE, and a non-migrating update applied; a changed filter did not resync existing rows; the subscriber's extra column kept its default and the unpublished `ssn` column was absent; two publications for one table were OR-ed (rows matching either arrived); the example publication errors on UPDATE/DELETE as described above. `publish_via_partition_root` behaviour was not exercised.
