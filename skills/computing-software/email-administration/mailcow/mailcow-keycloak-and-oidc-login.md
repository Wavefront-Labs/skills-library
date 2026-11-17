---
id: computing-software.email-administration.mailcow.mailcow-keycloak-and-oidc-login
name: mailcow-keycloak-and-oidc-login
category: computing-software
field: email-administration
product: mailcow
tags: [keycloak, generic-oidc, authorization-code-flow, mailpassword-flow, redirect-url, mailcow-template, external-mail-clients]
level: advanced
status: docs-checked
description: "Set up Keycloak or a generic OIDC provider for mailcow UI login, with template mapping through the mailcow_template claim and app passwords for mail clients."
sources: ["https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-keycloak/", "https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-generic-oidc/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keycloak and generic OIDC login for mailcow

Both are chosen under System, Configuration, Access, Identity Provider.

Generic-OIDC fields: Authorization, Token and User Info endpoints, Client ID and Secret, Redirect URL (your mailcow UI address), Client Scopes (default `openid profile email mailcow_template`), Attribute Mapping and Ignore SSL Errors. Keycloak instead takes Server URL, Realm, Client ID and Secret, Redirect URL, Version and Ignore SSL Errors; Keycloak background sync (import, offboarding, group sync) is described on a separate Identity Provider sync page, and generic OIDC does not support it.

Provisioning: with Auto-create users on login enabled and either a matching Attribute Mapping or a Default Template configured, on login mailcow runs an Authorization Code Flow, fetches user info, reads the `mailcow_template` value and, if it matches an Attribute Mapping entry, creates the user with that mailbox template (templates are re-checked on each UI login).

Keycloak extras: Mailpassword Flow validates credentials through the Keycloak Admin REST API and needs a hashed `mailcow_password` attribute on the user. The mailcow client then needs a service account with the `view-users` role. Keycloak 24 and newer only stores user attributes defined in the realm's user profile, so add `mailcow_template` (and `mailcow_password`) there or enable Unmanaged attributes.

Existing users can be switched under E-Mail, Configuration, Mailboxes by choosing the Identity Provider in the mailbox editor. The SQL password is not overwritten, so switching back restores the old password. External clients (IMAP, SIEVE, POP3, SMTP) cannot use the SSO login; the user creates an app password in Mailbox Settings, App Passwords tab.

## Checked

2026-11-09. Confirmed on the Keycloak and generic OIDC pages: menu path, field lists, default scopes, Authorization Code Flow provisioning via mailcow_template, Mailpassword Flow with mailcow_password and view-users, switching existing users with the SQL password kept, and app passwords. Removed the Periodic Full Sync, Import Users and interval fields (they belong to the separate sync page), the claim that import needs view-users, and added the Auto-create condition and the Keycloak 24 user profile note.

Method: docs-checked 2026-11-09 against the full Keycloak and generic OIDC pages (raw markdown in mailcow-dockerized-docs); the linked Identity Provider sync page was not read.
