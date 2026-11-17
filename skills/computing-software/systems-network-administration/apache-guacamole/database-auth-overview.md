---
id: computing-software.systems-network-administration.apache-guacamole.database-auth-overview
name: database-auth-overview
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, database-authentication, jdbc-auth, mysql, mariadb, postgresql, sql-server, admin-interface, load-balancing]
level: intro
status: draft
description: "Why and how to use Guacamole's JDBC database authentication (MariaDB/MySQL, PostgreSQL, SQL Server) and how it combines with LDAP, SSO and other extensions."
sources:
  - https://guacamole.apache.org/doc/gug/jdbc-auth.html
  - https://guacamole.apache.org/doc/gug/ldap-auth.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database authentication overview

Supported: MariaDB/MySQL, PostgreSQL, SQL Server. Highly recommended over `user-mapping.xml` because it provides:
- a web-based admin interface (users, groups, connections, history)
- connection sharing links (sharing profiles)
- load-balancing connection groups

Setup pages per database: apache-guacamole.mysql-auth-setup, apache-guacamole.postgresql-auth-setup, apache-guacamole.sqlserver-auth-setup. Schema layout: apache-guacamole.jdbc-schema-reference.

Combining with other extensions:
- The database can play a subordinate role: users and groups authenticated by LDAP, SSO, header, etc. can be given connections and permissions stored in the database.
- A database user and an external user are treated as the same when names match, using the `case-sensitivity` setting (see apache-guacamole.guacamole-properties-reference).
- If another extension authenticates a user successfully, that result is trusted; to force a database account too set `<db>-user-required: true`; to create accounts automatically set `<db>-auto-create-accounts: true`.
- LDAP plus database: connections and permissions in the database, LDAP only for authentication, is the recommended pattern.

Default account after loading the schema: `guacadmin` / `guacadmin`. Change it immediately.

Verify: log in as guacadmin, open Settings and confirm the administration sections (users, connections, sessions, history) appear.
