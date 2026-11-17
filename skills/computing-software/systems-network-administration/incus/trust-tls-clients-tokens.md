---
id: computing-software.systems-network-administration.incus.trust-tls-clients-tokens
name: trust-tls-clients-tokens
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, authentication, tls, trust, trust-token, jwt, client-certificate, encrypted-key]
level: practitioner
status: docs-checked
description: "Trust Incus clients: incus config trust add/add-certificate/list/remove, token expiry, JWT client tokens, TLS 1.3 and key advice, encrypted client keys."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS client trust

```
incus config trust list
incus config trust add-certificate <file>
incus config trust add                 # trust token; prompts for a client name
incus config trust remove <fingerprint>
incus remote add <name> <token>
incus remote get-client-token
incus remote generate-certificate --encrypt --tls-cert <path> --tls-key <path>
```

- Client and server generate key pairs on first launch; delete the old ones to regenerate. TLS 1.3 or later (`INCUS_INSECURE_TLS` forces 1.2, unsupported). Keys: 4096-bit RSA minimum, preferably 384-bit ECDSA, SHA-2 signatures.
- Tokens expire per `core.remote_token_expiry` or once used. Behind NAT, give the external address to `remote add`.
- JWT: Subject is the certificate's full fingerprint, with valid NotBefore/NotAfter. Browsers POST it to `/tls/login` (cookie `tls_jwt`, `Secure`, `HttpOnly`); `/tls/logout` clears it.
- Encrypt an existing key with `ssh-keygen -p -o -f .config/incus/client.key`; keepalive cuts passphrase prompts.
- Revoked trust still returns HTTP 403 on API calls.

## Checked

2026-11-09. Confirmed against the Incus Remote API authentication page: key generation on first launch, TLS 1.3 and INCUS_INSECURE_TLS, key advice, trust list/add/add-certificate/remove, token expiry and NAT note, JWT Subject/NotBefore/NotAfter, /tls/login and /tls/logout cookie, encrypted keys and keepalive, 403 on revoked trust. Nothing removed.
Method: documentation only; no commands were run.
