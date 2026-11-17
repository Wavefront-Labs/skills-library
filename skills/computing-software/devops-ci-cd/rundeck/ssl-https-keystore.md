---
id: computing-software.devops-ci-cd.rundeck.ssl-https-keystore
name: ssl-https-keystore
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, ssl-https, keystore, ssl-properties, port-4443]
level: advanced
status: docs-checked
description: "Enable HTTPS directly in Rundeck: generate a keystore with keytool, set ssl.properties, framework.properties and grails.serverURL, and start with SSL; or import a PFX."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/security/ssl.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs warn that letting Rundeck manage certificates is not recommended; terminating SSL at a proxy or load balancer is better practice. For direct SSL, with Rundeck stopped (WAR installs first run the launcher once to generate config):

1. Generate a keystore (WAR: `$RDECK_BASE/etc/keystore`; RPM/DEB: `/etc/rundeck/ssl/keystore`). Use the real server name in the SAN, since modern clients ignore CN:

```bash
keytool -keystore /etc/rundeck/ssl/keystore -ext san=dns:$HOSTNAME -alias rundeck -genkey -keyalg RSA -keypass <password> -storepass <password>
```

2. Copy it as the CLI truststore: `cp .../keystore .../truststore` (CLI tools look for `$RDECK_BASE/etc/truststore`).
3. Edit `ssl.properties` with `keystore`, `keystore.password`, `key.password`, `truststore`, `truststore.password`.
4. In `framework.properties` set `framework.server.url=https://localhost:4443` and `framework.server.port=4443`.
5. In `rundeck-config.properties` set `grails.serverURL=https://localhost:4443`.
6. RPM/DEB: set `RUNDECK_WITH_SSL=true` and optionally `RDECK_HTTPS_PORT` in `/etc/default/rundeckd` (DEB) or `/etc/sysconfig/rundeckd` (RPM), then `service rundeckd start`.
7. WAR: `java -Drundeck.ssl.config=$RDECK_BASE/server/config/ssl.properties -Dserver.https.port=1234 -jar rundeck-<version>.war`.

Success shows `Grails application running at https://localhost:<port>`.

Gotcha: make sure no firewall rule filters packets to the HTTPS port.

Existing PFX: extract the key, cert and CA with three `openssl pkcs12` commands, merge with `openssl pkcs12 -export ... -out keystore.p12`, then `keytool -importkeystore -srckeystore keystore.p12 -srcstoretype pkcs12 -destkeystore keystore -deststoretype JKS`.

## Checked

2026-11-04: the recommendation against Rundeck-managed certificates, keystore locations and keytool command, the truststore copy, ssl.properties, framework.properties and grails.serverURL settings, RPM/DEB and WAR start options, the success message, the firewall note and the PFX import steps confirmed against the Rundeck SSL page.

Method: documentation only; no commands were run.
