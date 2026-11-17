---
id: computing-software.systems-network-administration.apache-tomcat.tls-handshake-troubleshooting
name: tls-handshake-troubleshooting
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, tls, troubleshooting, handshake, logging-properties, keystore-error, ssl-howto]
level: practitioner
status: docs-checked
description: "Debug Tomcat 10.1 TLS problems: enable handshake logging in logging.properties and fix common keystore errors (file not found, tampered password, no certificate)."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/ssl-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS troubleshooting

Turn on handshake logging in `$CATALINA_BASE/conf/logging.properties`:
```
org.apache.tomcat.util.net.NioEndpoint.handshake.level=FINE
# or, depending on the Connector used (NIO2):
org.apache.tomcat.util.net.Nio2Endpoint.handshake.level=FINE
```

| Symptom | Likely cause and fix |
|---|---|
| `FileNotFoundException ... not found` | Keystore is not at the default `~/.keystore`; set `certificateKeystoreFile` on `<Certificate>` |
| `Keystore was tampered with, or password was incorrect` | Tomcat is using a different password than the one used to create the keystore; recreate the keystore or update the password in the Tomcat configuration (the page names `keystorePass` on the Connector; the Certificate attribute is `certificateKeystorePassword`). Passwords are case sensitive |
| `No available certificate or key corresponds to the SSL cipher suites...` | Tomcat cannot find the alias for the server key in the keystore; check `certificateKeystoreFile` and `certificateKeyAlias` on `<Certificate>` (alias values may be case sensitive) |

Other checks:
- JSSE vs OpenSSL attributes must not be mixed in one `SSLHostConfig`.
- For SNI with several certificates see `computing-software.systems-network-administration.apache-tomcat.sni-multiple-certificates`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 SSL/TLS how-to (Troubleshooting). Reworded the password and alias rows; removed the logging-handler note, the missing-Certificate claim, the s_client advice and the generic verify line.

Method: documentation only; no commands were run.
