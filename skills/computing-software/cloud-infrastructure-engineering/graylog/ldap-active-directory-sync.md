---
id: computing-software.cloud-infrastructure-engineering.graylog.ldap-active-directory-sync
name: ldap-active-directory-sync
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [ldap, active-directory, group-sync, starttls, authentication-services]
level: practitioner
status: docs-checked
description: "Connect Graylog to Active Directory or LDAP: server, TLS or StartTLS, system user and user and group synchronization."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/active_directory_ldap.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ldap active directory sync

At **System > Authentication**, Create service and choose Active Directory or LDAP. The steps are the same for both: server configuration, user synchronization, then group synchronization (Graylog Enterprise only).

Server configuration fields:
- Title and optional Description.
- Server Address with port; IP or FQDN. Every Graylog server must resolve and reach it.
- Encryption: None, TLS or StartTLS (uses a secure connection if available but allows an insecure one).
- Verify Certificates: validate certificates on connect.
- System User DN and System Password for the initial connection.

You need AD or LDAP credentials from your identity provider and administrator rights in Graylog.

## Checked

2026-11-04. Confirmed against the Active Directory and LDAP page. Nothing removed.

Method: documentation only; no commands were run.
