---
id: computing-software.systems-network-administration.apache-guacamole.duo-mfa
name: duo-mfa
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, duo, mfa, multi-factor-authentication, duo-client-id, duo-api-hostname, duo-redirect-uri, duo-bypass-hosts, web-sdk]
level: practitioner
status: docs-checked
description: "Add Duo as a second factor to Guacamole: Web SDK app in Duo, duo-api-hostname, duo-client-id, duo-client-secret, duo-redirect-uri, timeout and bypass/enforce host lists."
sources:
  - https://guacamole.apache.org/doc/gug/duo-auth.html
  - https://guacamole.apache.org/doc/gug/mfa.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duo multi-factor authentication

In Duo's admin panel add an application of type **Web SDK**, rename it (users see the name), and copy API hostname, Client ID and Client secret.

Install: copy `guacamole-auth-duo-1.6.0.jar` to `GUACAMOLE_HOME/extensions/`, restart Tomcat. Docker: `DUO_ENABLED=true`.

Required (native / Docker):
- `duo-api-hostname` / `DUO_API_HOSTNAME`: e.g. `api-XXXXXXXX.duosecurity.com`
- `duo-client-id`, `duo-client-secret`
- `duo-redirect-uri`: the full URL users type to reach Guacamole

Older versions used `duo-integration-key` and `duo-secret-key`; 1.6.0 uses the client names.

Optional:
- `duo-auth-timeout`: minutes, default 5
- `duo-bypass-hosts`, `duo-enforce-hosts`: IPs or CIDR subnets; enforce wins if both are set. Default is Duo for everyone.

Behaviour:
- Duo is a second factor only; another extension (database, LDAP) authenticates first.
- It cannot be combined with SSO; configure Duo or TOTP on the SSO provider instead (apache-guacamole.mfa-overview-sso).

Restart disconnects users; check Tomcat logs if startup fails.

Verify: after normal login the Duo prompt appears; a host in the bypass list skips it.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages duo-auth and mfa: Web SDK application and rename step, copying client ID, secret and API hostname, DUO_ENABLED, the four required properties, old duo-integration-key/duo-secret-key names, duo-auth-timeout in minutes with default 5, bypass and enforce lists (CIDR, enforce wins, default is Duo for all), Duo needing another extension first, and no use alongside SSO. Removed: the line saying host rules need real client IPs (not on the page).

Method: documentation only; no commands were run.
