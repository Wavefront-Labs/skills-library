---
id: computing-software.networking-hardware-and-wireless.haproxy.client-certificate-authentication
name: client-certificate-authentication
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, client-certificate-auth, mutual-tls, verify-required, ssl-c-s-dn, crl-file]
level: practitioner
status: docs-checked
description: "Require and inspect client certificates in HAProxy with verify required, ca-file, crl-file and ssl_c_* fetches, and pass identity to backends."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client certificate authentication
Mutual TLS on a bind line:

```
frontend fe_mtls
    bind :8443 ssl crt /etc/haproxy/certs/server.pem ca-file /etc/haproxy/client-ca.pem verify required crl-file /etc/haproxy/crl.pem
    http-request del-header X-SSL-Client-CN
    http-request set-header X-SSL-Client-CN %{+Q}[ssl_c_s_dn(cn)]
    http-request set-header X-SSL-Client-Serial %[ssl_c_serial,hex]
    http-request set-header X-SSL-Client-Verify %[ssl_c_verify]
    http-request deny unless { ssl_c_used } { ssl_c_verify 0 }
    http-request deny unless { ssl_c_s_dn(cn) -m str alice bob }
```
`verify none` (the default) does not request a client certificate; `verify optional` requests one and lets clients without one in (ACL on `ssl_c_used`); `verify required` aborts the handshake without one. A presented certificate is always verified against `ca-file` (and `crl-file`), and a verify failure aborts the handshake regardless of `verify`, unless the error is listed in `ca-ignore-err` or `crt-ignore-err`.

`ca-file` holds the CAs used to verify client certificates; the CA names from it are sent to clients in the server hello. `ca-verify-file` also verifies but its CAs are not sent in that list: put intermediates in `ca-file` and the ending (root) CAs in `ca-verify-file`. `crl-file` needs a revocation list for every certificate of your CA chain; replace one at runtime with the `set ssl crl-file` command on the runtime socket (see the management guide's `new`/`set`/`commit ssl crl-file` commands).

Security: delete incoming `X-SSL-*` headers first (the `del-header` line) so clients cannot spoof them. `ssl_c_err` returns the first verification error at depth 0 (0 if none) and `ssl_c_verify` the verify result; error numbers come from your SSL library's documentation.

Verify: a request with a valid client certificate (for example `curl --cert client.pem --key client.key --cacert ca.pem https://lb:8443/`) reaches the backend, and one without a certificate is refused at the handshake.

## Checked
2026-11-03. Confirmed against configuration.html (bind keywords `verify`, `ca-file`, `ca-verify-file`, `crl-file`, `ca-ignore-err`; fetches `ssl_c_used`, `ssl_c_verify`, `ssl_c_err`, `ssl_c_s_dn`, `ssl_c_serial`) and management.html (`set ssl crl-file`). Fixed: `ca-file`/`ca-verify-file` roles were described inconsistently with the docs; removed the redundant `ca-verify-file` from the example, the "expired CRL gives unknown ca" claim, the specific error numbers 20 and 10, the browser CA-list note and the "alert certificate required" message.
Method: documentation only; no commands were run.
