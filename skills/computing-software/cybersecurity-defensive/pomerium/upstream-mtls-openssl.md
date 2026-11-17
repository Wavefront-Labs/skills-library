---
id: computing-software.cybersecurity-defensive.pomerium.upstream-mtls-openssl
name: upstream-mtls-openssl
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [upstream-mtls, tls-client-cert-file, tls-custom-ca-file, tls-upstream-server-name, openssl-s-server]
level: advanced
status: docs-checked
description: "Verify upstream identity and present a Pomerium client certificate to upstream services, with the route TLS settings and an openssl s_server test."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/certificates-and-tls.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Pomerium authenticates user traffic but does not require or verify the upstream's identity. Recommended: the upstream presents a valid TLS certificate and Pomerium optionally presents its own client certificate.

Route settings:
- Verify upstream: `tls_custom_ca_file` or `tls_upstream_server_name`.
- Client certificate: `tls_client_cert_file` and `tls_client_key_file`.

Proof of concept (mkcert and OpenSSL, test only):
1. `mkcert openssl.localhost` and `mkcert -client "pomerium@localhost"`; move files to e.g. `/etc/pomerium/`.
2. Start an upstream:

```
openssl s_server -key ./openssl.localhost-key.pem -cert ./openssl.localhost.pem -accept 44330 -www
```

3. Route `from: https://openssl.localhost.pomerium.io`, `to: https://localhost:44330`, `tls_upstream_server_name: openssl.localhost`, plus a policy. The server reporting "no client certificate available" shows Pomerium connects but sends none.
4. Restart the server with `-Verify 1` to require a client certificate.
5. Add `tls_client_cert_file` and `tls_client_key_file` pointing to the Pomerium client cert and key. The server output should now show a validated certificate.

See mutual-auth-methods for when to use this.

## Checked

2026-11-04. Confirmed against the Certificates and TLS page: upstream defaults, route settings tls_custom_ca_file, tls_upstream_server_name, tls_client_cert_file, tls_client_key_file, the mkcert and openssl s_server steps, port 44330, -Verify 1 and the expected outputs. Nothing removed.

Method: documentation only; no commands were run.
