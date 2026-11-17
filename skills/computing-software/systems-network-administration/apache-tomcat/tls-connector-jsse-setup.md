---
id: computing-software.systems-network-administration.apache-tomcat.tls-connector-jsse-setup
name: tls-connector-jsse-setup
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, tls, ssl, https, jsse, sslhostconfig, certificate, sslenabled, certificatekeystorefile, certificatekeyalias]
level: practitioner
status: docs-checked
description: "Configure an HTTPS Connector in Tomcat 10.1 with JSSE: SSLEnabled, SSLHostConfig, Certificate keystore attributes, defaults, and the redirectPort link to the HTTP Connector."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/ssl-howto.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPS Connector with a Java keystore

```xml
<Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
           SSLEnabled="true" maxThreads="150">
  <SSLHostConfig>
    <Certificate certificateKeystoreFile="conf/example.p12"
                 certificateKeystorePassword="<KEYSTORE_PASSWORD>"
                 certificateKeystoreType="PKCS12" type="RSA"/>
  </SSLHostConfig>
</Connector>
```
`SSLEnabled="true"` forces `scheme="https"` and `secure="true"`. Use `Http11Nio2Protocol` for NIO2. Each secure Connector needs at least one `SSLHostConfig` (unique `hostName`, default `_default_`) and each needs at least one `Certificate`.

Certificate attributes (JSSE):

| Attribute | Default |
|---|---|
| `certificateKeystoreFile` | `.keystore` in the running user's home |
| `certificateKeystorePassword` | changeit |
| `certificateKeystoreType` | JKS (or `javax.net.ssl.keyStoreType`) |
| `certificateKeyAlias` | first key found (order is implementation-dependent) |
| `certificateKeyPassword` | the keystore password |
| `type` | UNDEFINED; set RSA/DSA/EC/MLDSA, unique per type when several are nested |

Also set `redirectPort="8443"` on the plain HTTP Connector so protected URLs redirect.

Prefer `certificateKeystorePasswordFile` over inline passwords.

Verify: `openssl s_client -connect localhost:8443 </dev/null` completes a handshake.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html): confirmed SSLEnabled forcing scheme https and secure true, the at-least-one SSLHostConfig and Certificate rule, and the Certificate attribute defaults (.keystore in the user home, changeit, JKS, first key, UNDEFINED type). Removed the startup log line, which the page does not show.

Method: documentation only; no commands were run.
