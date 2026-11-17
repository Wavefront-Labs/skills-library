---
id: computing-software.cryptography-implementation.openssl.hsm-keys-via-openssl-pkcs11-provider
name: hsm-keys-via-openssl-pkcs11-provider
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, hsm-integration, pkcs11-provider, openssl-3, pkcs11-uri, rfc-7512, softhsm, ossl-store]
level: advanced
status: docs-checked
description: "Use HSM keys from OpenSSL 3 with pkcs11-provider: openssl.cnf setup, RFC 7512 URIs, signing CSRs and digests with HSM keys, and moving off the engine."
sources: ["https://github.com/latchset/pkcs11-provider", "https://www.rfc-editor.org/rfc/rfc7512", "https://docs.openssl.org/3.0/man7/provider/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using HSM keys from OpenSSL via pkcs11-provider

OpenSSL 3 replaces engines with providers. The `pkcs11-provider` project
(latchset) lets OpenSSL 3 use keys in a PKCS#11 token through RFC 7512 URIs.

## Configure

```ini
# openssl.cnf
openssl_conf = openssl_init
[openssl_init]
providers = provider_sect
[provider_sect]
default = default_sect
pkcs11 = pkcs11_sect
[default_sect]
activate = 1
[pkcs11_sect]
module = /path/to/pkcs11.so
pkcs11-module-path = /path/to/pkcs11-driver.so
pkcs11-module-token-pin = file:/path/to/userpin.txt
activate = 1
```

- The default provider must be listed and activated too, or the `openssl`
  command will not behave correctly.
- If no PIN is configured, most openssl utilities ask for it interactively.
- Instead of `pkcs11-module-path`, the driver can come from the
  `PKCS11_PROVIDER_MODULE` environment variable.
- Some drivers need `pkcs11-module-init-args`.

```bash
openssl list -providers      # pkcs11 must be listed as active
```

## Address keys by URI (RFC 7512)

Keys are named by percent-encoded `id` or by label (`object` in the URI).
Find them with `pkcs11-tool --module /path/to/pkcs11-driver.so --list-objects`.

```bash
openssl pkey -in "pkcs11:object=my-rsa-key;type=public" -pubin -pubout -text
openssl req -new -key "pkcs11:object=my-rsa-key;type=private" \
  -subj "/CN=www.example.com" -out web.csr
openssl dgst -sha256 -sign "pkcs11:object=my-rsa-key;type=private" -out f.sig f
```

`req -key` and `dgst -sign` accept a filename or a URI. `openssl storeutl
-keys -text pkcs11:` lists what the provider exposes.

## Notes

- A PIN can sit in the URI instead of `openssl.cnf`; avoid putting it on command
  lines or in shell history.
- The project recommends token-native tools such as `p11tool` for generating
  keys on a token.
- The provider replaces the deprecated engine mechanism; move `-engine`
  style invocations to URIs.

## Verify

- [ ] `openssl list -providers` shows pkcs11 active under the service's config.
- [ ] A CSR or signature made with the URI verifies against the token's public key.
- [ ] No PIN appears in process arguments or shell history.

## Checked

2026-11-01. Confirmed in the pkcs11-provider HOWTO.md and provider-pkcs11.7 man page: `module`, `pkcs11-module-path`, `pkcs11-module-token-pin = file:`, `pkcs11-module-init-args`, `PKCS11_PROVIDER_MODULE`, default provider must be activated, RFC 7512 URIs with `object`/`type`, PIN in URI, `pkcs11-tool --list-objects`, `p11tool` recommendation, `openssl storeutl -keys -text pkcs11:`, engines described as deprecated. In the OpenSSL openssl-req, openssl-dgst and openssl-list pages: `-key`/`-sign` take filename or URI, `list -providers`. Removed: distro packaging claim, SoftHSM and p11-kit specifics, per-server support claims, `pin-source=`.
Method: documentation only; no commands were run.
