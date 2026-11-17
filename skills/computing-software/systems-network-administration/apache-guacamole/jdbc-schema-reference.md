---
id: computing-software.systems-network-administration.apache-guacamole.jdbc-schema-reference
name: jdbc-schema-reference
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, database-schema, jdbc-auth-schema, guacamole-entity, guacamole-user, permissions-tables, password-hash, sql-reference]
level: advanced
status: docs-checked
description: "Reference to the Guacamole JDBC database tables: entities, users, groups, connections, parameters, sharing profiles, permissions, history and password hashing."
sources:
  - https://guacamole.apache.org/doc/gug/jdbc-auth-schema.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database schema reference

- `guacamole_entity`: one row per user or group (`entity_id`, `name`, `type` USER or USER_GROUP). Delete through this table so cascades clean up.
- `guacamole_user`: `user_id`, `entity_id`, `password_hash`, `password_salt`, `password_date`, `disabled`, `expired`, `access_window_start/end`, `valid_from/valid_until`, `timezone`, profile fields (`full_name`, `email_address`, `organization`, `organizational_role`).
- `guacamole_user_password_history`, `guacamole_user_history` (`remote_host`, `start_date`, `end_date`).
- `guacamole_user_group` (`disabled`), `guacamole_user_group_member` (`user_group_id`, `member_entity_id`; members may be users or groups).
- `guacamole_connection`: `connection_name`, `protocol`, `parent_id`, limits, `proxy_hostname/port/encryption_method`, `connection_weight`, `failover_only`.
- `guacamole_connection_parameter` (`connection_id`, `parameter_name`, `parameter_value`), `guacamole_connection_history` (user, connection, sharing profile, dates).
- `guacamole_connection_group`: `type` ORGANIZATIONAL or BALANCING, `parent_id`, `enable_session_affinity`.
- `guacamole_sharing_profile` (`primary_connection_id`) and `guacamole_sharing_profile_parameter`.

Permissions pair an `entity_id` with a target:
- `guacamole_system_permission`: ADMINISTER, AUDIT, CREATE_CONNECTION, CREATE_CONNECTION_GROUP, CREATE_SHARING_PROFILE, CREATE_USER, CREATE_USER_GROUP.
- `guacamole_user_permission`, `_user_group_permission`, `_connection_permission`, `_sharing_profile_permission`, `_connection_group_permission`: ADMINISTER, READ, UPDATE, DELETE.

Password format: `password_hash` = SHA-256 of password followed by `password_salt` (32 random bytes when set via Guacamole). A NULL salt means plain unsalted SHA-256, which is weak; avoid.

Verify: `SELECT name,type FROM guacamole_entity;` shows `guacadmin` on a database created from the provided schema scripts.

## Checked

2026-11-04. Confirmed against the Guacamole manual page jdbc-auth-schema (and the MySQL page for the guacadmin default): entity cascading delete advice, guacamole_user columns including access_window_*, valid_from/valid_until and timezone, password history and user history tables, group membership columns, connection columns including proxy_* and weighting/failover, connection group types and session affinity, the system permission names, the four object permissions, SHA-256 of password plus salt, the 32-byte random salt and the NULL-salt unsalted case. Nothing removed.

Method: documentation only; no commands were run.
