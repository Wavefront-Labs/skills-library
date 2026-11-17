---
id: computing-software.cybersecurity-defensive.keycloak.realm-smtp-email-settings
name: realm-smtp-email-settings
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, smtp, email, realm-settings, vault]
level: practitioner
status: docs-checked
description: "Configure realm SMTP in Keycloak: From and Reply-To headers, host, port, encryption, password or token authentication and UTF-8 handling."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/realms/email.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# realm smtp email settings
Keycloak emails users to verify addresses and for forgotten passwords, and emails administrators about server events. Provide SMTP settings under *Realm settings* > *Email* tab.

Template fields:
- **From**: the From SMTP header. **From display name** (optional): a friendly alias.
- **Reply to** (optional, From is used if unset) and **Reply to display name** (optional).
- **Envelope from** (optional): the bounce address used for the Return-Path header.

Connection and authentication:
- **Host** and **Port** of the SMTP server.
- **Encryption**: tick one of the checkboxes for sending username/password recovery mail, especially when the SMTP server is on an external network. You will most likely need to change the Port to 465, the default port for SSL/TLS.
- **Authentication**: switch ON if the server requires it. **Username** is needed for all mechanisms. **Authentication Type** is `password` or `token`.
- Type `password`: supply the Password; its value can refer to a value in an external vault (see the vault-secret-references skill).
- Type `token`: supply Auth Token URL (used to fetch a token via client credentials grant), Auth Token Scope, Auth Token ClientId and Auth Token Client Secret (the secret can also refer to an external vault value).
- **Allow UTF-8**: UTF-8-encode addresses sent to the server; enable only if the mail server supports the SMTPUTF8 extension. If disabled, non-ASCII domains are punycode-encoded and addresses with non-ASCII local parts return an error. With SMTP configured and Allow UTF-8 off, the built-in user profile email validator rejects emails whose local part is not ASCII.

## Checked
2026-11-03. Confirmed every field against server_admin/topics/realms/email.adoc. Removed: the example host/address flow, the claim that users without email cannot use flows, a test-connection step and the Verify step, none of which are on the page; added the token fields and Allow UTF-8 that were missing.
Method: documentation only; no commands were run.
