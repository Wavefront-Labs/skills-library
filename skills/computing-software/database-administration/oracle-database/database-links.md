---
id: computing-software.database-administration.oracle-database.database-links
name: database-links
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, database-link, distributed-queries, security]
level: practitioner
status: docs-checked
description: "Create and manage Oracle database links: fixed-user, connected-user and current-user links, public vs private, GLOBAL_NAMES, OPEN_LINKS and closing links."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-a-distributed-database.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-DATABASE-LINK.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database links

A database link is a communication path to another database. When a statement uses it, Oracle opens a session in the
remote database on behalf of the request. The kind of link decides which remote schema that session uses.

## Kinds of link
```sql
-- fixed user: always connects as the named remote user, whoever uses the link
CREATE DATABASE LINK billing_link
  CONNECT TO <REMOTE_USER> IDENTIFIED BY "<PASSWORD>"
  USING '<NET_SERVICE_NAME>';
-- connected user: omit CONNECT TO; connects with the local user's own user name and password
CREATE DATABASE LINK hr_link USING '<NET_SERVICE_NAME>';
-- current user: CONNECT TO CURRENT_USER (the current user must be a global user on both databases;
-- documented as part of the Oracle Advanced Security option)
CREATE DATABASE LINK cu_link CONNECT TO CURRENT_USER USING '<NET_SERVICE_NAME>';
SELECT * FROM dual@billing_link;
```
- Add `PUBLIC` to make the link visible to all users; without it the link is private to its creator.
- Privileges: `CREATE DATABASE LINK` (private) or `CREATE PUBLIC DATABASE LINK` (public), plus `CREATE SESSION` on the
  remote database.
- Inside a stored object, `CURRENT_USER` is the object's owner, except for invoker-rights objects, where it is the
  caller.
- If `GLOBAL_NAMES` is TRUE the link must have the same name as the database it connects to.

## Security
A public fixed-user link is visible to every user and connects as the fixed remote user, so every user gets that
remote account's rights. Prefer private links, use a least-privilege remote account, and avoid putting passwords in
scripts.

## Sessions and limits
- A link stays open for the life of the session that used it. Close it manually with
  `ALTER SESSION CLOSE DATABASE LINK <link_name>;`.
- `OPEN_LINKS` and `OPEN_LINKS_PER_INSTANCE` limit how many links can be open in one session or one RAC instance.

## Views
`DBA_DB_LINKS` lists all links in the database, `ALL_DB_LINKS` those accessible to the connected user, and
`USER_DB_LINKS` those the user owns (any user can query it). For links created with a connect identifier, the `HOST`
column is not resolved to connect data; the guide shows `DBMS_TNS.RESOLVE_TNSNAME(HOST)` for that.

## Verify
`SELECT * FROM dual@<link>` works for the intended users only, and `DBA_DB_LINKS` shows no unnecessary `PUBLIC` links.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Administrator's Guide chapter "Managing a Distributed Database"
and the SQL Language Reference page "CREATE DATABASE LINK" (read by targeted search): link kinds and syntax, PUBLIC,
privileges, CURRENT_USER behaviour, `GLOBAL_NAMES`, `OPEN_LINKS`, close statement, dictionary views. Removed (not on
those pages): `DRIVING_SITE` hint advice, LOB restrictions, two-phase commit and in-doubt transaction handling
(`DBA_2PC_PENDING`, `COMMIT FORCE`, `PURGE_LOST_DB_ENTRY`, RECO), `SYS.LINK$` password remark, audit advice, and the
list of ORA error causes.
Method: documentation only; no commands were run.
