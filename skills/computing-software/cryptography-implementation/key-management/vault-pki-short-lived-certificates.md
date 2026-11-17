---
id: computing-software.cryptography-implementation.key-management.vault-pki-short-lived-certificates
name: vault-pki-short-lived-certificates
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, secrets-managers, vault-pki, hashicorp-vault, short-lived-certificates, private-ca, intermediate-ca, cert-manager]
level: practitioner
status: docs-checked
description: "Issue short-lived internal certificates from Vault PKI: root and intermediate mounts, intermediate CSR flow, URL config and roles with tight constraints."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/pki", "https://developer.hashicorp.com/vault/tutorials/secrets-management/pki-engine", "https://cert-manager.io/docs/configuration/vault/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault PKI short-lived certificates

With certificates that live hours to days, you rarely need revocation:
compromise windows close by expiry. Vault's PKI engine makes issuance cheap
enough to do that.

## Hierarchy

Keep the root offline (or in a separate mount used only to sign the
intermediate); issue leaves from an intermediate mount.

```bash
vault secrets enable -path=pki_int pki
vault write -format=json pki_int/intermediate/generate/internal \
  common_name="Example Internal Issuing CA" key_type=ec key_bits=256 > csr.json
# sign csr with the root (offline or pki/ mount), then:
vault write pki_int/intermediate/set-signed certificate=@int.pem
```

Set the issuing-certificate and CRL URLs with `config/urls`. With multiple issuers in one mount, HashiCorp recommends
the per-issuer AIA fields instead of the global variant, because some applications use them for chain building and CRL
detection.

## Roles constrain what can be issued

```bash
vault write pki_int/roles/web allowed_domains=svc.example.internal \
  allow_subdomains=true allow_bare_domains=false allow_ip_sans=false \
  key_type=ec key_bits=256 max_ttl=72h ttl=24h \
  server_flag=true client_flag=false
vault write pki_int/issue/web common_name=api.svc.example.internal ttl=24h
```

- `allow_bare_domains` (default false) controls whether the domain itself can be requested; `allowed_domains` is
  used with it and `allow_subdomains`. `allow_ip_sans` defaults to true, so set it false when IP SANs are not wanted.
- Separate roles for server and client certificates.
- Bind roles to policies so a service can only issue for its own names.

## Verify

- [ ] A service token cannot issue names outside its role.
- [ ] Services reload certificates without restart.

## Checked

2026-11-01. Confirmed against the Vault PKI engine tutorial (intermediate `generate/internal` and `set-signed` flow,
`config/urls`, per-issuer AIA recommendation, role fields `allowed_domains`, `allow_bare_domains`, `allow_ip_sans`,
`server_flag`, `no_store` default). Removed: `no_store` semantics, tidy parameters, ACME version gate, Vault Agent and
cert-manager renewal timing, max-lease-ttl tune, expiry alert threshold and the 1 h renewal test.
Method: documentation only; no commands were run.
