---
id: computing-software.systems-network-administration.apache-tomcat.client-certificate-authentication
name: client-certificate-authentication
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, tls, mutual-tls, mtls, client-certificate, certificateverification, truststorefile, ocsp, crl, sslhostconfig]
level: advanced
status: docs-checked
description: "Require client certificates in Tomcat 10.1 SSLHostConfig: certificateVerification modes, truststore attributes, verification depth, CRL and OCSP options."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mutual TLS on the Connector

Attributes on `<SSLHostConfig>`:

| Attribute | Default / note |
|---|---|
| `certificateVerification` | `none`; `required`, `optional`, or `optionalNoCA` (OCSP disabled) |
| `certificateVerificationDepth` | 10 intermediates |
| `truststoreFile` | `javax.net.ssl.trustStore` property; relative to `$CATALINA_BASE` (JSSE) |
| `truststorePassword`, `truststoreType` | property default; type JKS (JSSE) |
| `caCertificateFile` / `caCertificatePath` | PEM CA bundle / directory (OpenSSL only) |
| `certificateRevocationListFile` | PEM CRL bundle; JSSE also accepts a URL |
| `revocationEnabled` | false (JSSE); forced on if a CRL file is set |
| `ocspEnabled` | false; validate via the cert's AIA OCSP responder |
| `ocspSoftFail` | true: handshake proceeds if the responder fails |
| `trustManagerClassName` | custom `X509TrustManager` (JSSE) |

Example:
```xml
<SSLHostConfig certificateVerification="required"
               truststoreFile="conf/clients-trust.p12" truststoreType="PKCS12"
               truststorePassword="<TRUSTSTORE_PASSWORD>">
  <Certificate .../>
</SSLHostConfig>
```

Then in the app's web.xml use `<auth-method>CLIENT-CERT</auth-method>`; the Realm maps the certificate subject (see `X509UsernameRetrieverClassName` in the Realm page). `maxSavePostSize` (default 4096) limits POST data saved across the re-handshake.

If TLS ends at a proxy, use `computing-software.systems-network-administration.apache-tomcat.ssl-valve-proxy-client-cert`.

Verify: `curl --cert client.pem --key client.key https://host:8443/` works; without a cert the handshake fails under `required`.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html) and Realm page (config/realm.html): confirmed certificateVerification values, depth 10, truststore attributes and defaults, CRL, revocationEnabled, ocspEnabled, ocspSoftFail, trustManagerClassName, maxSavePostSize 4096 and the X509UsernameRetrieverClassName Realm attribute. Nothing removed.

Method: documentation only; no commands were run.
