---
id: computing-software.networking-hardware-and-wireless.apache-httpd.ssl-ocsp-stapling
name: ssl-ocsp-stapling
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, tls, mod-ssl, ocsp-stapling, sslusestapling, staplingcache, revocation]
level: advanced
status: docs-checked
description: "Enable OCSP stapling with SSLUseStapling and SSLStaplingCache, tune timeouts, verify with openssl s_client, and handle missing chains or OCSP URIs."
sources:
  - https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCSP stapling
The server caches signed OCSP responses and sends them to clients, so clients do not query the CA.

```apache
SSLUseStapling On
SSLStaplingCache "shmcb:logs/ssl_stapling(32768)"
```
`SSLUseStapling` defaults to off; the cache is mandatory and supports the same types as `SSLSessionCache` except `none`/`nonenotnull`. Stapling uses the `ssl-stapling` and `sss-stapling-refresh` mutexes.

## Production tuning
```apache
SSLStaplingReturnResponderErrors off
SSLStaplingResponderTimeout 4
SSLStaplingStandardCacheTimeout 172800
SSLStaplingErrorCacheTimeout 60
```

## Verify
```
openssl s_client -connect www.example.com:443 -status -servername www.example.com
```

## Troubleshooting
- AH02217 means the certificate chain is missing; configure the chain (`SSLCertificateChainFile`, obsolete since 2.4.8 because `SSLCertificateFile` can also load intermediate CA certificates).
- `SSLUseStapling Off` in vhosts that should skip stapling.
- No OCSP URI in the certificate: `SSLStaplingForceURL`.

## Related
- `SSLOCSPEnable` is a different feature: it validates the client certificate chain (`on`, `leaf`, `off`; default `off`).

## Checked

2026-11-08. SSLUseStapling default off, mandatory SSLStaplingCache and its types, mutex names, tuning directive values, openssl s_client check, AH02217, SSLStaplingForceURL and SSLOCSPEnable confirmed against the ssl_howto and mod_ssl pages. Removed the mod_md MDStapling claim, which neither page covers; noted SSLCertificateChainFile is obsolete since 2.4.8.

Method: documentation only; no commands were run.
