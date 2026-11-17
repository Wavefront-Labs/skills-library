---
id: computing-software.systems-network-administration.pki-tls-administration.apache-mod-ssl-config
name: apache-mod-ssl-config
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [apache-mod-ssl-config, pki-apache, apache, mod_ssl, sslcertificatefile, sslprotocol, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Configure Apache httpd TLS with mod_ssl: certificate chain, protocols, cipher suites, session tickets and OCSP stapling."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apache mod_ssl configuration
Goal: hardened HTTPS vhost.
```
<VirtualHost *:443>
  ServerName example.com
  SSLEngine on
  SSLCertificateFile    /etc/ssl/example/fullchain.pem
  SSLCertificateKeyFile /etc/ssl/example/privkey.pem
  SSLProtocol           -all +TLSv1.2 +TLSv1.3
  SSLCipherSuite        ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
  SSLHonorCipherOrder   off
  SSLSessionTickets     off
  SSLUseStapling        on
</VirtualHost>
SSLStaplingCache "shmcb:/var/run/ocsp(128000)"
```
- Since httpd 2.4.8 `SSLCertificateFile` may also hold the intermediate CA certificates; `SSLCertificateChainFile` is deprecated.
- Defaults to know: `SSLProtocol` is `all -SSLv3` (up to 2.4.16: `all`); `SSLSessionTickets` is `on` (2.4.11 and later); `SSLHonorCipherOrder` is `off`; `SSLUseStapling` is `off`.
- `SSLCipherSuite` accepts a protocol specifier: `TLSv1.3` configures the TLS 1.3 suites (OpenSSL 1.1.1 and later). TLS 1.3 has no renegotiation, so cipher suites for it cannot be set in directory context.
- `SSLOpenSSLConfCmd name value` (httpd 2.4.8 and later, OpenSSL 1.0.2 or later) passes any OpenSSL `SSL_CONF_cmd` command through, for options mod_ssl has no directive for.
- Stapling: `SSLUseStapling` is valid in server config and virtual host, but `SSLStaplingCache` is server-config only and mandatory. Stapling covers only the server certificate's own response, not the intermediates.
Verify:
- [ ] The server's configuration syntax check passes before reload.
- [ ] `openssl s_client -status -connect HOST:443` shows an OCSP response once the cache has filled.

## Checked
Confirmed 2026-11-08 against the mod_ssl reference page: directive defaults and contexts, the 2.4.8 chain change, TLSv1.3 cipher specifier, SSLOpenSSLConfCmd, stapling notes. Corrected: the old gotcha said stapling directives are ignored inside a VirtualHost; SSLUseStapling is allowed there, only SSLStaplingCache must be server-wide. Removed (not on the page): HSTS header, `Protocols h2`, a2enmod and apachectl commands.
Method: docs-only read of cited pages, 2026-11-08
