---
id: computing-software.systems-network-administration.pki-tls-administration.ocsp-stapling-config
name: ocsp-stapling-config
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [ocsp-stapling-config, pki-ocsp, ocsp, stapling, nginx, apache, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Enable OCSP stapling on nginx and Apache httpd, know each server's prerequisites and check the stapled response with openssl s_client."
sources:
  - https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_stapling
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslusestapling
  - https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
  - https://docs.openssl.org/master/man1/openssl-s_client/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCSP stapling configuration
Goal: the server fetches OCSP and sends it in the handshake, saving the client a round trip.
nginx (`ssl_stapling` appeared in 1.3.7, default `off`):
```
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/ssl/chain.pem;   # issuer, root and intermediates
resolver 192.0.2.1;
```
- nginx needs the issuer's certificate: either the `ssl_certificate` file contains the intermediates, or the issuer is in the `ssl_trusted_certificate` file. A `resolver` is required to resolve the OCSP responder host name.
- `ssl_stapling_verify on` verifies responses; for it the issuer, root and all intermediates must be trusted via `ssl_trusted_certificate`.
- `ssl_stapling_responder http://...` overrides the responder URL from the Authority Information Access extension (only `http://` responders); `ssl_stapling_file` takes a DER response made with `openssl ocsp` instead of querying the responder.
Apache httpd (2.4):
```
SSLUseStapling on
SSLStaplingCache "shmcb:/path/to/stapling(32768)"
```
- `SSLUseStapling` (default `off`) is valid in server config and virtual host; `SSLStaplingCache` is server-config only and is a prerequisite. Requires OpenSSL 0.9.8h or later.
- The server staples only a response for its own certificate (RFC 6066 allows one), so intermediates are not covered.
- If mod_ssl logs AH02217 (cannot retrieve issuer certificate), the certificate chain is not configured; fix `SSLCertificateFile` / `SSLCertificateChainFile` first.
- Production tuning from the Apache SSL how-to (defaults are conservative): `SSLStaplingReturnResponderErrors off`, `SSLStaplingResponderTimeout 4` (default 10), `SSLStaplingStandardCacheTimeout 172800` (default 3600), `SSLStaplingErrorCacheTimeout 60` (default 600).
Check:
```
openssl s_client -connect HOST:443 -servername HOST -status
```
`-status` sends a certificate status request and prints the server's response, if any.
Verify:
- [ ] The s_client output contains the server's OCSP response.
- [ ] The response's Next Update time is in the future.

## Checked
Confirmed 2026-11-08 against ngx_http_ssl_module (ssl_stapling, _verify, _responder, _file, ssl_trusted_certificate), mod_ssl (SSLUseStapling, SSLStaplingCache, timeouts), the Apache SSL how-to (AH02217 and tuning) and the s_client manual (-status). Removed (not on the pages): HAProxy ocsp-update instructions, Let's Encrypt OCSP end-of-support note, nginx first-handshake behaviour.
Method: docs-only read of cited pages, 2026-11-08
