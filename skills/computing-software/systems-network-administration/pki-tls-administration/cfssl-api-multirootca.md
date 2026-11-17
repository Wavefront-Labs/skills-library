---
id: computing-software.systems-network-administration.pki-tls-administration.cfssl-api-multirootca
name: cfssl-api-multirootca
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cfssl-api-multirootca, pki-cfssl, cfssl, multirootca, api, auth-key, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Run cfssl serve or multirootca as a signing API with authentication keys, restricting profiles per caller."
sources:
  - https://github.com/cloudflare/cfssl
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/README.md
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/doc/cmd/multiroot.txt
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/doc/authentication.txt
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/doc/api/endpoint_sign.txt
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/doc/api/endpoint_authsign.txt
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/doc/api/endpoint_info.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cfssl serve API and multirootca
Goal: let services request certificates without holding the CA key.
```
cfssl serve -address 127.0.0.1 -port 8888 -ca ca.pem -ca-key ca-key.pem -config config.json
curl -d '{"certificate_request":"...CSR..."}' http://127.0.0.1:8888/api/v1/cfssl/sign
```
- Address and port default to `127.0.0.1:8888`; `-ca` and `-ca-key` default to `ca.pem` and `ca_key.pem` (note the underscore).
- `/api/v1/cfssl/sign` (POST) takes `certificate_request` (PEM CSR); optional `hosts`, `subject`, `serial_sequence`, `label`, `profile`, `bundle`.
- Authenticated signing uses `/api/v1/cfssl/authsign` with `token` and `request`. In config, define `auth_keys` (each with `type` and `key`) and set `auth_key` in the profile to the key name.
- The standard authenticator computes an HMAC-SHA-256 of the request with a hex-encoded key. The key may be a hex string, `env:NAME` (environment variable) or `file:/path` (file holding the hex key).
- `cfssl gencert -remote=remote_server csr.json` has a remote cfssl sign the certificate; a comma-separated remote list is tried in order.
- `multirootca` is an authenticated-signer-only server meant as the remote for cfssl instances; it offers only the `sign`, `authsign` and `info` endpoints.
- multirootca takes an ini-style config. Each section is a signer label with `private` (`file://` path, or `rofile://` for Red October), `certificate`, `config` (a cfssl config file) and optional `nets` (a network whitelist; absent means all networks) and `dbconfig`.
- `/api/v1/cfssl/info` (POST) needs a `label` and returns the signer certificate, `usage` and `expiry` of the profile.
- Bind to localhost or a private network, put TLS in front, and log requests.
- The `-db-config` flag of `cfssl serve` and `cfssl ocspserve` are the documented pieces for a certificate database and OCSP responses.
Advice: restrict who can reach the port and use `authsign` with an `auth_key` for callers, rather than exposing `cfssl serve` raw.
Verify:
- [ ] `curl -d '{"label":"primary"}' http://127.0.0.1:8888/api/v1/cfssl/info` returns the expected signer certificate, usages and expiry.
- [ ] A request without a valid token is rejected on the profile that sets `auth_key`.

## Checked
Confirmed 2026-11-08 against the cfssl README (serve flags, defaults, multirootca endpoints), doc/cmd/multiroot.txt (config format, nets, key URLs), doc/authentication.txt, the sign, authsign and info endpoint pages, and doc/cmd/cfssl.txt (remotes, auth_keys). Removed: `roots.conf` and the `-l` label flag (not in the pages), the claim that revocation commands "silently do nothing", and the claim that `/info` lists profiles (it returns one signer's certificate, usage and expiry).
Method: docs-only read of cited pages, 2026-11-08
