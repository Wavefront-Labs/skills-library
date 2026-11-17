---
id: computing-software.rpa-and-low-code.n8n.connect-ldap
name: connect-ldap
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, ldap, sso, bind, user-filter, attribute-mapping, enterprise]
level: practitioner
status: docs-checked
description: "Enable LDAP login in n8n as instance owner: connection security, bind method, base DN, user filter, account merging and what happens when LDAP is turned off."
sources:
  - https://docs.n8n.io/administer/manage-users-and-access/verify-user-identity/connect-ldap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let users sign in with directory credentials. Availability: Cloud Enterprise; self-hosted Business and Enterprise. You must be the instance owner.

## Enable
**Settings > LDAP**, toggle **Enable LDAP Login**, fill the fields, then **Test connection** or **Save connection**. After enabling, anyone on the LDAP server can sign in unless **User Filter** excludes them. Email users can still be created under **Settings > Users**.

## Connection fields
- **LDAP Login**: label replacing "Email" on the login username field.
- **LDAP Server Address** and **LDAP Server Port**: pre-filled `389`; with **TLS** use the LDAPS port (default `636`).
- **Connection Security**: **None**, **TLS** (`ldaps://`) or **STARTTLS** (`ldap://` then upgraded). **Ignore SSL/TLS Issues** appears unless None.
- **Base DN** such as `o=acme,dc=example,dc=com`.
- **Binding as**: **Admin** (enter **Binding DN**, e.g. `uid=2da2de69435c,ou=Users,o=Acme,dc=com`, and **Binding Password**) or **Anonymous** (empty DN and password; the server must allow anonymous search). Simple bind only: no SASL, GSSAPI or Kerberos, so Kerberos-only directories (common with Active Directory) cannot use LDAP login; use SAML or OIDC.
- **User Filter**, e.g. `(ObjectClass=user)`: only returned users can sign in.
- **Attribute mapping** (ID, login ID, email, first and last name): the shown examples do not suit every server; query with a tool such as `ldapsearch`.
- Periodic synchronization via **Enable periodic LDAP synchronization**. **Enforce Email Uniqueness** blocks sign in when several LDAP accounts share an email.

## Behaviour
- Matching email between an email user and LDAP user: the user must sign in with LDAP. Owner accounts are never converted.
- First sign-in creates the n8n account. Manage details on the LDAP server; updates or deletions apply at the next sync or the user's next login. Removed users lose access on the next sync.
- Turning LDAP off converts LDAP users to email users on next login; they must reset their password.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/administer/manage-users-and-access/verify-user-identity/connect-ldap

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
