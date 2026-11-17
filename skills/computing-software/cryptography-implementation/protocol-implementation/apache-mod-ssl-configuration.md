---
id: computing-software.cryptography-implementation.protocol-implementation.apache-mod-ssl-configuration
name: apache-mod-ssl-configuration
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, mod-ssl, apache-httpd, tls-server-configuration, ocsp-stapling, hsts]
level: practitioner
status: docs-checked
description: "Configure Apache httpd mod_ssl securely: SSLProtocol, SSLCipherSuite for TLS 1.2 and 1.3, certificates and chains, OCSP stapling, session tickets and HSTS."
sources: ["https://httpd.apache.org/docs/2.4/mod/mod_ssl.html", "https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apache mod_ssl configuration

```apache
Listen 443
SSLProtocol             -all +TLSv1.2 +TLSv1.3
SSLCipherSuite          ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305
SSLCipherSuite TLSv1.3  TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
SSLHonorCipherOrder     off
SSLSessionTickets       off
SSLUseStapling          On
SSLStaplingCache        "shmcb:logs/ssl_stapling(32768)"

<VirtualHost *:443>
  ServerName www.example.com
  SSLEngine on
  SSLCertificateFile    /etc/ssl/example/fullchain.pem    # leaf + intermediates (2.4.8+)
  SSLCertificateKeyFile /etc/ssl/example/privkey.pem
  Protocols h2 http/1.1
  Header always set Strict-Transport-Security "max-age=63072000"
</VirtualHost>
```

## Notes
- `SSLCertificateChainFile` is deprecated since 2.4.8; put intermediates in `SSLCertificateFile`.
- `SSLStaplingCache` is valid in server config only, not in a VirtualHost, and is mandatory for stapling; `SSLUseStapling` defaults to off.
- `SSLSessionTickets` defaults to on (httpd 2.4.11+); the docs warn that tickets without frequent restarts (e.g. daily) compromise forward secrecy.
- Dual certificates: repeat `SSLCertificateFile`/`KeyFile` pairs for RSA and ECDSA.

## Check
```sh
apachectl configtest && apachectl graceful
openssl s_client -connect www.example.com:443 -servername www.example.com -status </dev/null | grep -E 'Protocol|OCSP'
```

## Verify
- [ ] testssl.sh or SSL Labs shows no TLS 1.0/1.1 and stapling active.

## Checked
2026-11-01. Confirmed against mod_ssl and ssl_howto pages: SSLCertificateChainFile obsolete since 2.4.8 (SSLCertificateFile loads intermediates), SSLStaplingCache context and example, SSLUseStapling default and RFC 6066 basis, SSLSessionTickets default and 2.4.11 availability. Removed: mod_http2/prefork note, SSL Labs grade claim, ticket-key restart rationale (replaced by the documented warning).
Method: documentation only; no commands were run.
