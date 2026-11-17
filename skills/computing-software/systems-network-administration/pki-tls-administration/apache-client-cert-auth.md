---
id: computing-software.systems-network-administration.pki-tls-administration.apache-client-cert-auth
name: apache-client-cert-auth
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [apache-client-cert-auth, pki-apache, apache, sslverifyclient, sslrequire, mtls, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Require and map client certificates in Apache with SSLVerifyClient, SSLCACertificateFile and per-location rules."
sources:
  - https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html#allclients
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apache client certificate authentication
Goal: restrict locations to certificate holders.
```
SSLVerifyClient none
SSLCACertificateFile "conf/ssl.crt/ca.crt"
SSLCARevocationFile  "conf/ssl.crl/ca.crl"
SSLCARevocationCheck chain
<Location "/secure/area">
  SSLVerifyClient require
  SSLVerifyDepth 1
</Location>
```
- `SSLVerifyClient` levels: `none`, `optional`, `require`, `optional_no_ca` (the last cannot be relied on for client authentication).
- `SSLVerifyDepth` defaults to 1; `SSLCARevocationCheck` defaults to `none`, so CRLs in `SSLCARevocationFile` are ignored until you set `chain` or `leaf`.
- Per-directory or per-location `SSLVerifyClient` forces an SSL renegotiation after the request is read; mod_ssl buffers the request body in memory for it (size set by `SSLRenegBufferSize`). Server or vhost scope applies it in the normal handshake.
- To admit only some certificate holders, restrict by DN: `SSLRequire` (for example on `%{SSL_CLIENT_S_DN_O}`), or `SSLOptions +FakeBasicAuth` with a password file keyed by the subject DN. Add `+StrictRequire` so another `Require` cannot override an SSL denial.
- With `SSLVerifyClient optional`, `Require ssl-verify-client` grants access to authenticated holders and can be combined with `Require valid-user`.
- `SSLOptions +StdEnvVars` creates the standard SSL variables for CGI/SSI (off by default); `+ExportCertData` adds `SSL_CLIENT_CERT` and `SSL_CLIENT_CERT_CHAIN_n` as PEM.
Verify:
- [ ] A request without a client certificate to the protected location is refused.
- [ ] A valid client certificate gets access and the DN variables appear in the application.

## Checked
Confirmed 2026-11-08 against the Apache 2.4 SSL How-To (client authentication section) and the mod_ssl reference: SSLVerifyClient levels and renegotiation behaviour, SSLVerifyDepth default, SSLCARevocationCheck default, SSLOptions, Require ssl-verify-client. Removed: TLS 1.3 post-handshake claims, the Require expr example and the RequestHeader line (not on the cited pages).
Method: docs-only read of cited pages, 2026-11-08
