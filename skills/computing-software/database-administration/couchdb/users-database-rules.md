---
id: computing-software.database-administration.couchdb.users-database-rules
name: users-database-rules
category: computing-software
field: database-administration
product: couchdb
tags: [security, users-database, system-database, authentication-database, org-couchdb-user]
level: practitioner
status: docs-checked
description: "How the CouchDB _users authentication database differs from ordinary databases, and why user documents use the org.couchdb.user: id prefix."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/intro/security.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Admins are defined in config files; regular users live in the authentication database, `_users` by default. It is a system database with special constraints:

- Only admins may list all documents (`GET /_users/_all_docs`) or read its `_changes` feed.
- Only admins may run design functions such as views.
- The `_auth` design document cannot be modified.
- Every non-design document represents a registered user and belongs to them.
- Default `_security` settings disallow users from accessing or modifying documents.

If settings are changed to give access, users may only `GET` or `PUT` documents they own (for example `/_users/org.couchdb.user:Jan`). The docs say this will not be possible in CouchDB 4.0.

The reason: user documents contain login, password hash, roles and often personal data that must not be disclosed.

**Prefix.** The `org.couchdb.user:` prefix is a namespace to prevent replication conflicts when merging `_users` databases. All users currently share that one namespace and it cannot be changed.

## Checked

2026-11-04. Confirmed against the CouchDB intro/security page (Authentication Database, Why the org.couchdb.user: prefix): admins in config files, the six system-database constraints, the note about owned documents and CouchDB 4.0, the privacy reason, the namespace purpose and that it cannot be changed. Nothing removed.

Method: documentation only; no commands were run.
