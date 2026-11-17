---
id: computing-software.systems-network-administration.apache-guacamole.header-auth
name: header-auth
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, header-auth, http-auth-header, remote-user, external-authentication, trusted-header, reverse-proxy-sso]
level: practitioner
status: docs-checked
description: "Trust an HTTP header (default REMOTE_USER) for Guacamole login with the header extension, http-auth-header, and stripping the header from untrusted requests."
sources:
  - https://guacamole.apache.org/doc/gug/header-auth.html
  - https://guacamole.apache.org/doc/gug/external-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP header authentication

An external gateway authenticates the user and passes the username in a header; Guacamole trusts it.

Install: `guacamole-auth-header-1.6.0.jar` into `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `HTTP_AUTH_ENABLED=true` (false disables; the extension also installs when any related variable is set).

Property: `http-auth-header` (Docker `HTTP_AUTH_HEADER`), default `REMOTE_USER`. Set only if your gateway uses another header.

Danger: the manual states all external requests must be sanitised. The chosen header must be stripped from untrusted requests so the authentication service is the only possible source of it; otherwise malicious users can add the header manually and gain unrestricted access.

Connections: the header gives only a username, so layer a database (or other extension that supports delegated auth) to supply permissions and connections (apache-guacamole.database-auth-overview). The page gives no proxy examples.

When connection data should travel with the login, see apache-guacamole.json-auth.

Restart disconnects users.

Verify: a request carrying the header from the gateway is logged in, and a client-supplied copy of the header is stripped before it reaches Guacamole.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages header-auth and external-auth: delegation to an external service via an HTTP header, the layering requirement and the need for a delegation-capable extension such as the databases, the sanitising Danger notice, jar name and location, HTTP_AUTH_ENABLED behaviour, the REMOTE_USER default for http-auth-header and HTTP_AUTH_HEADER, and the restart warning. Changed: removed the claims about binding Tomcat to the proxy, the REMOTE_USER: admin example and the standard-SSO advice, none of which the pages state; the verify line now tests header stripping.

Method: documentation only; no commands were run.
