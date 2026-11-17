---
id: computing-software.cybersecurity-defensive.authelia.oidc-provider-hmac-and-signing-keys
name: oidc-provider-hmac-and-signing-keys
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, oidc, jwks, hmac-secret, rs256, signing-keys, key-id]
level: advanced
status: docs-checked
description: "Set up Authelia's OIDC provider with hmac_secret and issuer JWKS keys: RS256 requirement, key IDs and default key selection."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/provider/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The OpenID Connect provider needs a secret and at least one signing key.

```yaml
identity_providers:
  oidc:
    hmac_secret: '<OIDC_HMAC_SECRET>'
    jwks:
      - key_id: 'main-rsa'
        algorithm: 'RS256'
        use: 'sig'
        key: |
          -----BEGIN PRIVATE KEY-----
          ...
          -----END PRIVATE KEY-----
```

- `hmac_secret` signs JWTs. The string is hashed to a SHA256 byte string. Use 64 or more random alphanumeric characters.
- `jwks` lists issuer keys. At least one must be an RSA private key with algorithm `RS256`. You may add other RSA and ECDSA keys.
- The first key for each algorithm is the default when a client does not name a key ID. For example a client with `id_token_signed_response_alg: ES256` and no key ID uses the first `ES256` key in the list.
- `key_id` is optional and discouraged unless auto-generated IDs collide. It must be 100 characters or fewer, start and end alphanumeric and contain only RFC 3986 unreserved characters. The default is the first 7 hex characters of the public key SHA256 thumbprint, a hyphen, and the lowercase algorithm.
- `use` is `sig` (default) or `enc`.
- `key` must be a PEM private key: RSA of at least 2048 bits in PKCS#8 or PKCS#1, or ECDSA on P-256, P-384 or P-512 in PKCS#8 or SECG1. Load it from a file with the `template` file filter.
- `certificate_chain` is rarely needed; it enables `x5c` and `x5t` in the JWKS document.

Check: fetch the JWKS discovery endpoint and confirm your key IDs are listed.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Provider configuration page (hmac_secret hashing and length advice, jwks RS256 requirement and default-key ordering, key_id rules and default, use, key formats and sizes, template file filter, certificate_chain and x5c/x5t). Removed: nothing.

Method: documentation only; no commands were run.
