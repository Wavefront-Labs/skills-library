---
id: computing-software.email-administration.mailcow.mailcow-ldap-identity-provider
name: mailcow-ldap-identity-provider
category: computing-software
field: email-administration
product: mailcow
tags: [ldap, identity-provider, attribute-mapping, mailbox-templates, auto-provisioning, periodic-sync, bind-dn]
level: advanced
status: docs-checked
description: "Authenticate mailcow users against LDAP, map LDAP attribute values to mailbox templates and import or sync users on a schedule."
sources: ["https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-ldap/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring LDAP as identity provider

Configure under System, Configuration, Access, Identity Provider, choosing LDAP. Fields: Host (one name or a comma-separated list for fallback), Port, Encryption (None, StartTLS on the normal port or SSL/LDAPS, where port 389 is changed to 636 automatically), Ignore SSL Errors, Bind DN and Bind Password (an account that can read the needed attributes), Base DN, an optional Filter, Username Field (the attribute with the email address, default `mail`), an optional ID attribute and Disabled filter, Auto-create users on login, Attribute Field, Default Template and Attribute Mapping. Import of users, periodic sync, offboarding and group sync are described on a separate Identity Provider sync page.

Automatic provisioning: if Auto-create users on login is enabled and a user does not exist but logs in through IMAP, SIEVE, POP3, SMTP or the UI, mailcow binds to LDAP, reads the attribute named in Attribute Field, and if its value matches an Attribute Mapping entry creates the mailbox from the linked mailbox template (otherwise the Default Template is used). Example: the user has LDAP attribute `otherMailbox` with value `default`; set Attribute Field to `othermailbox` and map the attribute `default` to a template.

On every login mailcow checks whether the mapped template changed and updates the mailbox; templates of groups take precedence over the attribute mapping. Users can also be imported and updated in the background by a crontask without waiting for a login.

## Checked

2026-11-09. Confirmed on the LDAP page: menu path, host fallback list, LDAP bind provisioning, Attribute Field example, template update on login and group precedence. Corrected the connection fields: Use SSL and Use TLS are now a single Encryption setting (None, StartTLS, SSL/LDAPS). Moved the Periodic Full Sync, Import Users and interval fields out, since the page defers them to a separate sync page that was not read.

Method: docs-checked 2026-11-09 against the full LDAP page (u_e-mailcow_ui-ldap.en.md in mailcow-dockerized-docs); the linked sync page was not read.
