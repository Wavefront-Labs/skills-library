---
id: computing-software.cybersecurity-defensive.keycloak.ldap-federation-edit-mode-and-import
name: ldap-federation-edit-mode-and-import
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, ldap, user-federation, edit-mode, import-users]
level: practitioner
status: docs-checked
description: "Configure Keycloak LDAP or Active Directory federation choosing import users on or off and READ_ONLY, WRITABLE or UNSYNCED edit mode."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/user-federation/ldap.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldap federation edit mode and import
The **Import Users** switch on the LDAP provider page controls the storage mode.

- ON: the LDAP provider imports users into the Keycloak database the first time a user logs in or is returned by a user query (for example the admin console search), and validates the password against LDAP during authentication. All Keycloak features work efficiently because per-user data is stored locally. The cost is a database insert the first time a user is queried, and a corresponding LDAP search for each imported user returned by a search operation. Keycloak also performs an LDAP search when an imported user is queried, to validate and decorate it, so take extra care with unfiltered searches that fetch many users; operations fetching a single user (for example login) are usually cached.
- OFF: LDAP backs the common user model directly. If LDAP does not support data a Keycloak feature needs, that feature will not work. You cannot save user profile attributes into the Keycloak database, nor metadata except what is mapped to LDAP (role and group mappings depend on the mappers); for example you cannot disable a user unless the `enabled` flag maps to an LDAP attribute.

**Edit Mode** defines the user's LDAP update privileges:
- `READ_ONLY`: mapped attributes cannot be changed, Keycloak shows an error on attempts, password updates are not supported.
- `WRITABLE`: changes to mapped attributes and passwords are synchronised automatically with the LDAP store.
- `UNSYNCED`: changes to username, email, first name, last name and passwords are stored in Keycloak local storage and an administrator must synchronise them back to LDAP; this allows updating user metadata on read-only LDAP servers.

When Keycloak creates the provider it also creates initial LDAP mappers based on the combination of Vendor, Edit Mode and Import Users. Changing Edit Mode (or Import Users) later does not change the mappers, so decide Edit Mode when creating the provider.

Other options: *Console Display Name*, *Priority*, *Sync Registrations* (ON adds new users created by Keycloak to LDAP), *Allow Kerberos authentication*, *Remove invalid users during searches*.

## Checked
2026-11-03. Confirmed against server_admin/topics/user-federation/ldap.adoc (import, edit mode and other configuration options sections). Removed (not on the page): the periodic background sync claim, the least-privilege bind and vault advice, the exact menu path, and the Verify step.
Method: documentation only; no commands were run.
