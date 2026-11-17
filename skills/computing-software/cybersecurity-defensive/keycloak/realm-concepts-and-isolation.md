---
id: computing-software.cybersecurity-defensive.keycloak.realm-concepts-and-isolation
name: realm-concepts-and-isolation
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, realm, isolation, roles, groups]
level: practitioner
status: docs-checked
description: "Keycloak core vocabulary: realms, users, roles, composite roles, groups, clients, client scopes, service accounts and sessions, and what a realm isolates."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/overview/concepts.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# realm concepts and isolation
A realm manages a set of users, credentials, roles and groups. A user belongs to and logs into one realm. Realms are isolated from one another and can only manage and authenticate the users they control.

Vocabulary from the server administration guide:
- **Users**: entities that can log in; they have attributes (email, username, address, phone, birthday), group membership and roles.
- **Roles**: identify a type or category of user (admin, user, manager, employee). Applications often grant access by role rather than per user.
- **User role mapping**: links a role to a user (zero or more); it can be put into tokens and assertions so applications decide access.
- **Composite role**: a role associated with other roles; for example `superuser` with `sales-admin` and `order-entry-admin`; a user mapped to it inherits them.
- **Groups**: can have attributes and role mappings; members inherit both.
- **Clients**: entities that ask Keycloak to authenticate a user (applications and services), or that just want an identity or access token to call other secured services.
- **Client role**: a role namespace specific to a client.
- **Client scope**: shared protocol mappers and role scope mappings reused across clients; also lets claims or roles depend on the `scope` parameter.
- **Service account**: each client has a built-in one that lets it obtain an access token. **Direct grant**: a client gets an access token on behalf of a user via a REST call.
- **Protocol mappers**: per client, tailor claims and assertions in the OIDC token or SAML assertion.
- **Consent**: after credentials, a screen shows the requesting client and requested identity information for the user to grant or refuse.
- **Session**: created at login; holds the login time and the applications that took part in SSO; admins and users can view it.
- **User federation provider**: validates credentials and pulls identity from external stores such as LDAP or Active Directory.
- **Identity provider**: authenticates a user; Keycloak is one. **Identity provider federation** delegates to other OIDC or SAML 2.0 IDPs (including social login), and **identity provider mappers** map incoming tokens and assertions to user and session attributes.
- **Required actions**, **authentication flows** (login, registration, credential reset), **events** (audit streams) and **themes** (every screen is backed by one).

## Checked
2026-11-03. Confirmed against server_admin/topics/overview/concepts.adoc. Removed: the unsourced design guidance (realm per tenant, keep master for admin, roles to groups, shallow composites), the token-inflation gotcha and the Verify step.
Method: documentation only; no commands were run.
