---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-pki-rotation-tidy
name: vault-pki-rotation-tidy
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, pki-tidy, issuer-rotation, tidy]
level: practitioner
status: docs-checked
description: "Add a new issuer to a Vault PKI mount, switch the default, and run tidy to remove expired certificates and revocations."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/pki", "https://developer.hashicorp.com/vault/api-docs/secret/pki", "https://developer.hashicorp.com/vault/docs/secrets/pki/rotation-primitives"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A PKI mount can hold several issuers, and one is the default. Rotation adds a new issuer and moves the default to it.

```sh
vault write pki_int/intermediate/generate/internal common_name="Example Intermediate 2027" issuer_name=int-2027
vault write pki_int/intermediate/set-signed certificate=@signed2027.pem
vault write pki_int/config/issuers default=int-2027
vault list pki_int/issuers
vault write pki_int/tidy tidy_cert_store=true tidy_revoked_certs=true safety_buffer=72h
vault read pki_int/tidy-status
```

- `default` on `/pki/config/issuers` takes an issuer name or ID.
- A role can pin an issuer with `issuer_ref` (default `default`), so a role pinned to the old issuer keeps using it after you change the default. Use ACLs on `/pki/issuer/:issuer_ref/{issue,sign}/:name` if users must not override the role's issuer.
- `tidy_cert_store` tidies the certificate store; `tidy_revoked_certs` removes invalid and expired certificates from storage, and a certificate removed for expiry also leaves the CRL (the CRL is rotated).
- `safety_buffer` is the extra time after a certificate's expiry (by Vault's local clock) before it may be removed; it guards against clock skew. The documented default is `72h`.
- Automatic tidy is configured at `/pki/config/auto-tidy` (`enabled`, `interval_duration`, default `12h`).
- Cross-signing and reissuing are the documented primitives for moving trust between roots; rotating a root takes long because roots sit in client trust stores.

## Checked
2026-11-03. Confirmed on the PKI API page (tidy parameters, `safety_buffer`, `tidy-status`, `config/auto-tidy`, `config/issuers` `default`, role `issuer_ref`, list issuers) and the rotation primitives page. Removed: the Verify step, the staging-mount and error-rate advice, "old issuers must stay until all certificates expire", snapshot advice, the claim that unrotated listing slows down, and "clients must trust the new chain" (not stated as a rule on these pages).
Method: documentation only; no commands were run.
