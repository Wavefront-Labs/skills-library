---
id: computing-software.systems-network-administration.apache-guacamole.connection-groups-balancing
name: connection-groups-balancing
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, connection-groups, balancing-group, organizational-group, load-balancing, session-affinity, connection-weight, failover-only, max-connections]
level: practitioner
status: docs-checked
description: "Organise Guacamole connections with organizational folders and balancing groups routing to the least-loaded member, with affinity."
sources:
  - https://guacamole.apache.org/doc/gug/administration.html
  - https://guacamole.apache.org/doc/gug/jdbc-auth-schema.html
  - https://guacamole.apache.org/doc/gug/mysql-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connections and connection groups

Names must be unique within their location. New connections are admin-only until access is granted.

Group types:
- **Organizational**: behaves like a folder; no other behaviour.
- **Balancing**: behaves as a connection; each new session goes to the member with the fewest active users. Session affinity keeps a user on the same underlying connection until logout; balancing then applies only to the user's first connection.

Schema fields (see apache-guacamole.jdbc-schema-reference): `guacamole_connection_group.type` is ORGANIZATIONAL or BALANCING; `enable_session_affinity` (off by default) and `max_connections` / `max_connections_per_user` (NULL uses the guacamole.properties default, 0 unlimited) only affect BALANCING groups. On connections, `connection_weight` (integer, 1 or greater weights the member, below 1 disables it in the group, NULL means 1) and `failover_only` ("hot spare", used only when another member of the same BALANCING group has failed) only matter inside BALANCING groups.

Concurrency limits (database extensions, shown with the MySQL prefix; the other databases use their own prefix): `mysql-default-max-connections`, `mysql-default-max-group-connections`, `mysql-default-max-connections-per-user`, `mysql-default-max-group-connections-per-user`, `mysql-absolute-max-connections`; 0 means unlimited. By default each user may hold only one active connection per connection group. Defaults can be overridden per connection in the admin UI.

Bulk creation: apache-guacamole.batch-import.

Verify: open the group from two accounts; sessions land on different members.

## Checked

2026-11-08. Read the whole of administration.html and the connection group, connection weight and failover columns of jdbc-auth-schema.html (partial read, those tables only), plus the concurrent-use section of mysql-auth.html (partial read). Confirmed group types, affinity behaviour, weight and failover semantics, and the limit properties and defaults. Removed the claims that KSM vault tokens do not work with balancing groups and that login restrictions apply to balancing groups (not on the cited pages), and the note telling readers to check the UI help for weight semantics (now documented).
Method: documentation only; no commands were run.
