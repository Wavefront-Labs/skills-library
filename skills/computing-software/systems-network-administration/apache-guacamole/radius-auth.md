---
id: computing-software.systems-network-administration.apache-guacamole.radius-auth
name: radius-auth
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, radius, radius-auth, radius-shared-secret, radius-auth-protocol, eap-ttls, mschapv2, lgpl-extensions, mfa]
level: advanced
status: docs-checked
description: "Authenticate Guacamole users against RADIUS: building the extension, radius-hostname, shared secret, auth protocol (pap, chap, mschap, eap), key files, timeouts."
sources:
  - https://guacamole.apache.org/doc/gug/radius-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RADIUS authentication

Not distributed as a binary (LGPL). Build:
```
mvn -Plgpl-extensions clean package
cp extensions/guacamole-auth-radius/target/guacamole-auth-radius-1.6.0.jar GUACAMOLE_HOME/extensions/
```
Docker: `docker build --build-arg MAVEN_ARGUMENTS="-Plgpl-extensions -DskipTests=true" -t guacamole/guacamole .`

Properties (Docker uppercase, e.g. `RADIUS_HOSTNAME`):
| Property | Default |
|---|---|
| `radius-hostname` | localhost |
| `radius-auth-port` | 1812 |
| `radius-shared-secret` | required (extension will not load without it) |
| `radius-auth-protocol` | required: `pap`, `chap`, `mschapv1`, `mschapv2`, `eap-md5`, `eap-tls`, `eap-ttls` (PEAP is currently broken) |
| `radius-key-file`, `radius-key-type`, `radius-key-password` | `radius.key` in GUACAMOLE_HOME, `pkcs12` (also pem, jceks, jks) |
| `radius-ca-file`, `radius-ca-type`, `radius-ca-password` | `ca.crt` in GUACAMOLE_HOME, `pem` |
| `radius-trust-all` | `false` |
| `radius-retries` | 5 |
| `radius-timeout` | 60 s |
| `radius-eap-ttls-inner-protocol` | required with `eap-ttls`; anything except `eap-ttls` |
| `radius-nas-ip` | auto-detected |

Use absolute paths for key and CA files. Layered on another extension for connections (apache-guacamole.database-auth-overview). The manual does not describe challenge/response handling.

Avoid `radius-trust-all=true` outside testing.

Verify: a RADIUS account logs in.

## Checked

2026-11-04. Confirmed against the Guacamole manual page radius-auth: LGPL dependency so no binary is distributed, mvn -Plgpl-extensions build and jar location, the Docker build argument including -DskipTests=true, every property in the table with its default (localhost, 1812, pkcs12, pem, false, 5 retries, 60 seconds), protocol list with PEAP broken, eap-ttls inner protocol rule, NAS IP auto-detection, and layering on another extension. Changed: install path now uses GUACAMOLE_HOME; removed the unsupported RADIUS-server-log check from Verify.

Method: documentation only; no commands were run.
