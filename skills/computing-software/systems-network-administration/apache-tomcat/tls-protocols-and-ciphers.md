---
id: computing-software.systems-network-administration.apache-tomcat.tls-protocols-and-ciphers
name: tls-protocols-and-ciphers
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, tls, sslhostconfig, protocols, ciphers, ciphersuites, honorcipherorder, tls-1-3, sessiontimeout]
level: advanced
status: docs-checked
description: "Restrict TLS versions and cipher suites in Tomcat 10.1 SSLHostConfig: protocols, ciphers vs cipherSuites (TLS 1.3), honorCipherOrder, groups, session cache and timeout defaults."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS protocols and ciphers

On `<SSLHostConfig>`:

| Attribute | Default / note |
|---|---|
| `protocols` | `all` = SSLv2Hello,TLSv1,TLSv1.1,TLSv1.2,TLSv1.3. SSLv3 is inherently unsafe |
| `ciphers` | `HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!kRSA` plus the three TLS 1.3 suites; applies to TLS 1.2 and below |
| `cipherSuites` | `TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256`; TLS 1.3 only, others ignored with a warning |
| `honorCipherOrder` | false; true enforces the server's order |
| `groups` | `jdk.tls.namedGroups` property; case-sensitive list |
| `sslProtocol` | TLS (JSSE only) |
| `sessionTimeout` | 86400 s |
| `sessionCacheSize` | -1 (implementation default); 0 = unlimited, not recommended |
| `disableSessionTickets` | false (OpenSSL only) |
| `disableCompression` | true (OpenSSL only) |
| `insecureRenegotiation` | false (OpenSSL only) |

Example, TLS 1.2 and 1.3 only:
```xml
<SSLHostConfig protocols="TLSv1.2,TLSv1.3" honorCipherOrder="true">
  <Certificate .../>
</SSLHostConfig>
```
`ciphers` takes the OpenSSL syntax or a comma-separated list of OpenSSL or JSSE cipher names; unsupported entries are ignored with a warning at startup.

Verify: `openssl s_client -connect host:8443 -tls1_1` fails; `nmap --script ssl-enum-ciphers -p 8443 host` lists only the allowed suites.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html): confirmed defaults and notes for protocols, ciphers, cipherSuites, honorCipherOrder, groups, sslProtocol, sessionTimeout, sessionCacheSize, disableSessionTickets, disableCompression and insecureRenegotiation. Replaced the vague cipher-name sentence with what the page states.

Method: documentation only; no commands were run.
