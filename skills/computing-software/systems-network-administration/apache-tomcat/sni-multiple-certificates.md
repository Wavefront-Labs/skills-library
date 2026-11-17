---
id: computing-software.systems-network-administration.apache-tomcat.sni-multiple-certificates
name: sni-multiple-certificates
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, tls, sni, sslhostconfig, hostname, defaultsslhostconfigname, strictsni, multiple-certificates, virtual-host]
level: advanced
status: docs-checked
description: "Serve several certificates from one Tomcat 10.1 TLS Connector with SNI: multiple SSLHostConfig hostName entries, defaultSSLHostConfigName, strictSni and RSA plus EC certificates."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
  - https://tomcat.apache.org/tomcat-10.1-doc/ssl-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SNI with several SSLHostConfig elements

```xml
<Connector port="8443" protocol="HTTP/1.1" SSLEnabled="true"
           defaultSSLHostConfigName="www.example.com">
  <SSLHostConfig hostName="www.example.com">
    <Certificate certificateKeystoreFile="conf/www.p12"
                 certificateKeystoreType="PKCS12" type="RSA"/>
  </SSLHostConfig>
  <SSLHostConfig hostName="*.example.org">
    <Certificate certificateKeystoreFile="conf/org.p12"
                 certificateKeystoreType="PKCS12" type="RSA"/>
  </SSLHostConfig>
</Connector>
```

Rules:
- `hostName` defaults to `_default_`, is lowercased, and may be an FQDN or a wildcard such as `*.apache.org`. Names must be unique per Connector.
- One `SSLHostConfig` must match `defaultSSLHostConfigName`; it serves clients that send no SNI.
- `strictSni` (default true) rejects a request whose SNI name and `Host` header map to different `SSLHostConfig`s.
- SNI picks the certificate; the `Host` header picks the virtual host. They are separate settings, so keep them in sync.
- Nest several `Certificate` elements (RSA, EC) in one `SSLHostConfig` by giving each a distinct `type`.
- `sniParseLimit` (default 65536 bytes) caps the ClientHello Tomcat will parse (NIO/NIO2).

Verify: `openssl s_client -connect host:8443 -servername www.example.com | openssl x509 -noout -subject` for each name.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html): confirmed hostName default _default_ and lowercasing, wildcard names, unique SSLHostConfig names, defaultSSLHostConfigName, strictSni default true, the separation of SNI and Host header matching, unique Certificate type values and sniParseLimit 65536. Nothing removed.

Method: documentation only; no commands were run.
