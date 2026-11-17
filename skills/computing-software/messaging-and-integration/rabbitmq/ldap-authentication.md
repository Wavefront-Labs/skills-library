---
id: computing-software.messaging-and-integration.rabbitmq.ldap-authentication
name: ldap-authentication
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, ldap-authentication, rmq-auth-backends]
level: advanced
status: docs-checked
description: "Enable the LDAP plugin for authN/authZ with query-based permissions and an internal fallback."
sources:
  - https://www.rabbitmq.com/docs/ldap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP authentication

**Goal:** Centralise identity.

## Steps
1. `rabbitmq-plugins enable rabbitmq_auth_backend_ldap`; `auth_backends.1 = ldap`, `auth_backends.2 = internal` (the second entry is the fallback).
2. Configure `auth_ldap.servers.1`, optionally `auth_ldap.dn_lookup_bind.*`, and TLS with `auth_ldap.use_ssl = true` (or `auth_ldap.use_starttls`). The default port is 389 (`auth_ldap.port`).
3. Map users to tags and permissions with queries (`tag_queries` and the other query settings).
4. If LDAP only handles authentication, users must also exist in the internal database for authorisation.

## Failure modes
- With only `ldap` in `auth_backends`, an unreachable LDAP server blocks logins; add `internal` as a fallback.

## Verify
- `rabbitmqctl authenticate_user <user> <password>` succeeds.

## Checked

Date: 2026-11-02. Confirmed on the LDAP guide and rabbitmqctl man page. Removed: "ldaps" wording (the guide uses `use_ssl` and StartTLS) and "groups to tags" simplification.

Method: documentation only; no commands were run.
