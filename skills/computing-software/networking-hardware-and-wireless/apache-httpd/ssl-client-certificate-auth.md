---
id: computing-software.networking-hardware-and-wireless.apache-httpd.ssl-client-certificate-auth
name: ssl-client-certificate-auth
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, tls, mod-ssl, client-certificates, sslverifyclient, sslrequire, fakebasicauth]
level: advanced
status: docs-checked
description: "Require and authorise client certificates: SSLVerifyClient levels, SSLVerifyDepth, per-location rules, SSLRequire, FakeBasicAuth and revocation checking."
sources:
  - https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client certificate authentication
## Server-wide
```apache
SSLVerifyClient require
SSLVerifyDepth 1
SSLCACertificateFile "conf/ssl.crt/ca.crt"
```
Levels: `none` (default), `optional`, `require`, `optional_no_ca` (not reliable for authentication). `SSLVerifyDepth` default is 1; 0 accepts only self-signed certificates.

## One area only
```apache
SSLVerifyClient none
SSLCACertificateFile "conf/ssl.crt/ca.crt"
<Location "/secure/area">
    SSLVerifyClient require
    SSLVerifyDepth 1
</Location>
```

## Authorisation
`SSLRequire` checks certificate fields:
```apache
SSLOptions +FakeBasicAuth
SSLRequireSSL
SSLRequire %{SSL_CLIENT_S_DN_O} eq "Snake Oil, Ltd." \
    and %{SSL_CLIENT_S_DN_OU} in {"Staff", "CA", "Dev"}
```
For arbitrary certificates pair `+FakeBasicAuth` with a password file listing each allowed DN. `SSLRequire` is deprecated in favour of `Require expr`.

## Mixed access
Combine `SSLVerifyClient optional`, `Satisfy any`, `Require ip 192.168.1.0/24` and Basic auth.

## Revocation
`SSLCARevocationCheck chain` checks CRLs for the whole chain; CRLs must exist unless `no_crl_for_cert_ok`. Set `SSLCARevocationFile` or `SSLCARevocationPath`.

## Checked
2026-11-04. Confirmed against the mod_ssl reference and the SSL how-to: SSLVerifyClient levels and default, SSLVerifyDepth default and depth 0, server-wide and per-location examples, FakeBasicAuth with SSLRequire, SSLRequire deprecation in favour of Require expr, mixed Satisfy any example, SSLCARevocationCheck chain and no_crl_for_cert_ok. Nothing removed.
Method: documentation only; no commands were run.
