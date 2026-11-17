---
id: computing-software.cybersecurity-defensive.authentik.provider-ldap
name: provider-ldap
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, ldap-provider, base-dn, bind-flow, app-password, code-based-mfa, ldaps]
level: advanced
status: docs-checked
description: "Reference for the authentik LDAP provider: Base DN layout, user and group attributes, LDAPS, bind flow, app password bind, search permission, cached modes and MFA codes."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: expose authentik users and groups over LDAP through an LDAP outpost.

## Directory layout
Default **Base DN** `DC=ldap,DC=goauthentik,DC=io` (Protocol settings); give each LDAP provider a unique Base DN, for example `OU=appname,DC=ldap,DC=goauthentik,DC=io`. Users: `ou=users,<base DN>`; groups: `ou=groups,<base DN>`; each user also has a generated virtual group under `ou=virtual-groups,<base DN>` whose `gidNumber` equals the user's `uidNumber`.
User attributes: `cn`, `uid`, `uidNumber`, `name`, `displayName`, `mail`, `objectClass`, `memberOf`, `homeDirectory` (default `/home/$username`), `ak-active`, `ak-superuser`. Group attributes: `cn`, `uid`, `gidNumber`, `member`, `memberOf`, `objectClass`. Custom attributes are returned and override built-ins with the same name (periods and slashes sanitized).

## LDAPS
Set **Certificate** and **TLS Server Name**; the certificate is chosen by server name, not Bind DN, because StartTLS happens before the bind. Enables port 636.

## Binding
Binds run the provider's **Bind Flow** (and **Unbind Flow**). Supported stages: Identification, Password, Authenticator validation, User Logout, User Login, Deny. Modes: **Direct bind** (flow on every bind) and **Cached bind** (result cached per credentials in memory for the session duration; revoking sessions or changing credentials does not evict it).

App password bind: edit the bind flow's Password stage (or the one set on Identification) and add **User database + app passwords** to Backends; bind with a DN like `cn=ldapservice,ou=users,dc=ldap,dc=goauthentik,dc=io` and the app password. API tokens do not work, and other flow stages including MFA still apply.

## Searching
The user needs access to the LDAP application (bindings). By default a user sees only themselves and their groups. To search everything, give the user's role the **Search full LDAP directory** permission, preferably as an object permission on the provider's **Permissions** tab. Search modes: direct (always fresh, slower) or cached (outpost holds all users and groups, may be stale).

## Code-based MFA
Enable **Code-based MFA Support** and include an Authenticator Validation stage; supports Duo, TOTP and static (not SMS). Append the code after a semicolon in the password: `example-password;123456`. Users without an authenticator may have passwords containing a semicolon rejected.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/ldap/.
Nothing was removed.
Method: documentation only; no commands were run.
