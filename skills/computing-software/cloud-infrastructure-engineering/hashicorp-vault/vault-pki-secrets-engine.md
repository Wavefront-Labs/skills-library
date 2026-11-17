---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-pki-secrets-engine
name: vault-pki-secrets-engine
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, pki-engine, pki, intermediate-ca]
level: practitioner
status: docs-checked
description: "Build a Vault PKI hierarchy with an externally held root, an intermediate in Vault, an issuance role, TTL limits and CRL/issuing URLs."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/pki", "https://developer.hashicorp.com/vault/docs/secrets/pki/setup", "https://developer.hashicorp.com/vault/api-docs/secret/pki"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Vault setup page recommends maintaining the root CA outside Vault and giving Vault a signed intermediate. Issue leaf certificates from the intermediate.

```sh
vault secrets enable -path=pki_int pki
vault secrets tune -max-lease-ttl=43800h pki_int
vault write pki_int/intermediate/generate/internal common_name="Example Intermediate" issuer_name=int-2026
# sign the CSR with the root (outside Vault), then:
vault write pki_int/intermediate/set-signed certificate=@signed.pem
vault write pki_int/config/urls issuing_certificates="https://vault.example.com/v1/pki_int/ca" \
  crl_distribution_points="https://vault.example.com/v1/pki_int/crl"
vault write pki_int/roles/web allowed_domains=example.com allow_subdomains=true max_ttl=72h
vault write pki_int/issue/web common_name=app.example.com ttl=24h
```

- The default secrets-engine maximum lease TTL is 30 days (setup page); raise it with `vault secrets tune -max-lease-ttl=...` as above. Roles can restrict it further per certificate.
- Completing intermediate generation needs the CSR signed by an external or offline root and the signed certificate imported with `set-signed`.
- `config/urls` sets the Issuing Certificate, CRL Distribution Points and OCSP server (`ocsp_servers`) URLs; the setup page says these values can be updated later.
- A requested `ttl` cannot exceed the role's `max_ttl`.
- Role fields shown in the API sample: `allowed_domains`, `allow_subdomains`, `allow_any_name`, `max_ttl`.
- The PKI API page lists ACME, EST, CMPv2 and SCEP issuance protocols; EST, CMPv2 and SCEP carry the Enterprise label there. Unified CRLs and unified OCSP require Vault Enterprise or HCP Plus.

## Checked
2026-11-03. Confirmed on the PKI setup page (root outside Vault, 30-day default, `tune -max-lease-ttl`, `config/urls`, URLs updatable) and the PKI API page (intermediate generate/set-signed, role fields, `ttl` vs `max_ttl`, URL parameters, Enterprise labels). Removed: "short TTLs keep CRLs small", the claim that URLs are embedded so must be set before issuing (the setup page says they can be updated), `openssl verify` Verify step, and the closing advice on publishing roots and alerting on CA expiry.
Method: documentation only; no commands were run.
