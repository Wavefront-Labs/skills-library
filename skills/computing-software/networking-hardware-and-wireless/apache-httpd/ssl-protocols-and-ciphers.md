---
id: computing-software.networking-hardware-and-wireless.apache-httpd.ssl-protocols-and-ciphers
name: ssl-protocols-and-ciphers
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, tls, mod-ssl, sslprotocol, sslciphersuite, sslhonorcipherorder, ciphers]
level: practitioner
status: docs-checked
description: "Restrict TLS versions and ciphers with SSLProtocol, SSLCipherSuite, SSLHonorCipherOrder and SSLCompression, including per-location strength with renegotiation."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
  - https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSL protocols and ciphers
## Protocols
`SSLProtocol` default is `all -SSLv3`.
```apache
SSLProtocol -ALL +TLSv1.2 +TLSv1.3
```

## Ciphers
`SSLCipherSuite` takes a colon-separated OpenSSL string. Preview with `openssl ciphers -v '<spec>'`. Since 2.4.7 `!aNULL:!eNULL:!EXP` is always applied. TLSv1.3 ciphers use the `TLSv1.3` protocol specifier.
```apache
SSLCipherSuite HIGH:!aNULL:!MD5
SSLHonorCipherOrder on
```
`SSLHonorCipherOrder` defaults to `off`; `on` makes the server's cipher order win.

## Per-location strength
Be liberal globally and strict for one URL; mod_ssl forces a renegotiation to apply it:
```apache
<Location "/strong/area">
    SSLCipherSuite HIGH:!aNULL:!MD5
</Location>
```

## Other
- `SSLCompression` defaults to `off`; enabling exposes CRIME.
- `SSLOpenSSLConfCmd` passes SSL_CONF commands:
```apache
SSLOpenSSLConfCmd Protocol "-ALL, TLSv1.2"
SSLOpenSSLConfCmd ECDHParameters brainpoolP256r1
```
- `SSLStrictSNIVHostCheck on` denies non-SNI clients the vhost (default off).
- mod_http2 `H2ModernTLSOnly` (default on) requires TLS 1.2+.

## Checked
2026-11-04. Confirmed against the mod_ssl reference and the SSL how-to: SSLProtocol default, SSLCipherSuite behaviour (per-directory renegotiation, TLSv1.3 specifier, always-disabled aNULL/eNULL/EXP since 2.4.7, openssl ciphers -v), SSLHonorCipherOrder and SSLCompression defaults, SSLOpenSSLConfCmd examples, SSLStrictSNIVHostCheck. Removed: the cipher-string prefix semantics and the RC4 remark (not on those pages).
Method: documentation only; no commands were run.
