---
id: computing-software.systems-network-administration.apache-tomcat.ssl-valve-proxy-client-cert
name: ssl-valve-proxy-client-cert
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, sslvalve, client-certificate, proxy-headers, ssl-client-cert, nginx, httpd]
level: advanced
status: docs-checked
description: "Pass client TLS certificate data from httpd or nginx to Tomcat 10.1 with SSLValve: header names, escaped cert header and the spoofing risk if the proxy does not set them."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSLValve

Class `org.apache.catalina.valves.SSLValve`. Reads TLS details a front-end proxy forwards in headers, so Tomcat can use client-certificate auth when TLS ends at the proxy.

| Attribute | Default header |
|---|---|
| `sslClientCertHeader` | ssl_client_cert |
| `sslClientEscapedCertHeader` | ssl_client_escaped_cert (wins over the plain one; handy for nginx) |
| `sslCipherHeader` | ssl_cipher |
| `sslSessionIdHeader` | ssl_session_id |
| `sslCipherUserKeySizeHeader` | ssl_cipher_usekeysize |

```xml
<Valve className="org.apache.catalina.valves.SSLValve"/>
```

Proxy side (httpd example on the page, using mod_headers): the headers must always be set by httpd for all requests, so a client cannot spoof SSL information with fake headers. The example sets SSL_CLIENT_CERT, SSL_CIPHER, SSL_SESSION_ID and SSL_CIPHER_USEKEYSIZE inside `<IfModule ssl_module>`, unsets them in `<IfModule !ssl_module>`, and always runs `RequestHeader unset SSL_CLIENT_ESCAPED_CERT`.

For direct client-cert TLS see `computing-software.systems-network-administration.apache-tomcat.client-certificate-authentication`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Valve reference (SSL Valve): attribute names, default header names, escaped-cert precedence, httpd mod_headers example and spoofing note. Removed the empty-value claim and the generic verify line.

Method: documentation only; no commands were run.
