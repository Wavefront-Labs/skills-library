---
id: computing-software.systems-network-administration.apache-guacamole.cas-sso
name: cas-sso
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, cas, sso, single-sign-on, cas-authorization-endpoint, cas-redirect-uri, cas-clearpass-key, cas-group-attribute, clearpass]
level: practitioner
status: docs-checked
description: "Single sign-on to Guacamole with CAS: authorization endpoint, redirect URI, ClearPass key in PKCS8, group attributes and formats, and extension-priority behaviour."
sources:
  - https://guacamole.apache.org/doc/gug/cas-auth.html
  - https://guacamole.apache.org/doc/gug/sso.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAS single sign-on

Install: from `guacamole-auth-sso-1.6.0.tar.gz` copy `cas/guacamole-auth-sso-cas-1.6.0.jar` to `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `CAS_ENABLED=true`.

Properties (Docker uppercase):
- `cas-authorization-endpoint` (required): base URL of the CAS server
- `cas-redirect-uri` (required): where CAS returns users, normally the Guacamole URL
- `cas-clearpass-key`: private key file to decrypt the ClearPass password
- `cas-group-attribute`: e.g. `memberOf`; without it groups are not read
- `cas-group-format`: `plain` (default) or `ldap`
- `cas-group-ldap-base-dn`, `cas-group-ldap-attribute`: filters, only with `ldap` format; the group name is the leftmost DN attribute

Login behaviour:
- `extension-priority: cas`: unauthenticated users go straight to CAS.
- `extension-priority: *, cas`: normal login form with a CAS link.

ClearPass: caches the SSO password on the CAS server and makes it available to Guacamole. Generate a keypair, install the public key on CAS, and point `cas-clearpass-key` at the private key in RSA PKCS8 format.

CAS attributes released by the server become `${CAS_...}` tokens (apache-guacamole.parameter-tokens).

SSO only authenticates; combine with a database for connections (apache-guacamole.database-auth-overview).

Verify: browsing to Guacamole redirects to CAS and returns logged in.

## Checked

2026-11-04. Confirmed against the Guacamole manual page cas-auth: jar name and location, CAS_ENABLED, the two required properties, cas-clearpass-key with a private key in RSA PKCS8 format and the public key installed on CAS, group attribute and format (plain default, ldap using the leftmost DN attribute), the ldap-only base DN and attribute filters, the two extension-priority forms, CAS_ token prefix and layering on another extension. Reworded: the ClearPass line no longer names a specific token.

Method: documentation only; no commands were run.
