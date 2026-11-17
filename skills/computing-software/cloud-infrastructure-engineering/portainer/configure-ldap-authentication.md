---
id: computing-software.cloud-infrastructure-engineering.portainer.configure-ldap-authentication
name: configure-ldap-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [authentication, ldap, openldap, service-account, user-provisioning]
level: practitioner
status: docs-checked
description: "Configure LDAP authentication in Portainer with a read-only service account, automatic user provisioning, fallback servers and the OpenLDAP Reader DN format."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/settings/authentication/ldap.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Portainer authenticates users against your LDAP directory; a successful bind lets them in. First create a service account in the directory for Portainer to read LDAP, with read-only access.

Enable it as an administrator: Settings, Authentication, LDAP Authentication.

Automatic user provisioning creates a Portainer user on first successful LDAP login. If off, create users manually with the same username as the directory entry.

Server Type is either a custom configuration or a preconfigured OpenLDAP template. Enter the LDAP server IP or FQDN and port, then connect anonymously (the server must allow it) or use an account with READ access. For OpenLDAP the Reader DN format is `cn=user,dc=domain,dc=tld`; adjust it if your layout differs. Use Test connectivity to validate. Click Add additional server to define fallback servers for authentication.

LDAP security settings on the same page include Use StartTLS (upgrades the connection after the initial connect), Use TLS, and Skip verification of server certificate (encrypts, but you must then verify by other means that you are talking to the right server), plus a TLS CA certificate upload for the secure connection. Once external authentication is enabled, only the initial admin user can still log in with internal authentication.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
