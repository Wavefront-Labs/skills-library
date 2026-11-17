---
id: computing-software.cloud-infrastructure-engineering.docker.notation-signing-and-trust-policy
name: notation-signing-and-trust-policy
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, notation, notary-project, image-signing, notation-sign, trust-policy, x509, ratify]
level: advanced
description: "Sign images with Notation (Notary Project) using X.509 keys or KMS plugins, store signatures as OCI referrers, and verify against a trust policy and trust store."
sources: ["https://notaryproject.dev/docs/quickstart-guides/quickstart-sign-image-artifact/", "https://notaryproject.dev/docs/user-guides/how-to/manage-trust-policy/", "https://github.com/notaryproject/specifications/blob/main/specs/trust-store-trust-policy.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notation signing and trust policy

Notation signs with X.509 PKI, using local keys or a KMS through plugins (Azure Key Vault and AWS Signer
plugins exist), rather than Sigstore's keyless model. Signatures use a JWS (default) or COSE envelope and
are stored as OCI artifacts associated with the signed image; by default Notation uses the referrers tag
schema, and `--allow-referrers-api` (experimental) uses the Referrers API with tag-schema fallback.

## Sign
```sh
notation cert generate-test --default "acme.io"        # test only: self-signed key + cert
notation sign registry.example.com/app@sha256:<digest>
notation ls registry.example.com/app@sha256:<digest>
```
Production via plugin:
```sh
notation plugin install --url <azure-kv plugin release> --sha256sum <sum>
notation key add --plugin azure-kv --id https://myvault.vault.azure.net/keys/release/<ver> release-key --default
notation sign --signature-format cose registry.example.com/app@sha256:<digest>
```
AWS Signer has its own Notation plugin; follow the AWS Signer documentation for its plugin name and key id.

## Trust store and trust policy
```sh
notation cert add --type ca --store acme acme-root-ca.crt
```
```json
{
  "version": "1.0",
  "trustPolicies": [
    {
      "name": "prod-images",
      "registryScopes": ["registry.example.com/app", "registry.example.com/worker"],
      "signatureVerification": { "level": "strict" },
      "trustStores": ["ca:acme"],
      "trustedIdentities": ["x509.subject: C=US, ST=WA, O=Acme, CN=release"]
    },
    {
      "name": "legacy-unsigned",
      "registryScopes": ["registry.example.com/legacy/tools"],
      "signatureVerification": { "level": "skip" }
    }
  ]
}
```
```sh
notation policy import trustpolicy.json
notation verify registry.example.com/app@sha256:<digest>
```
Levels (Notary Project trust policy spec): `strict` enforces integrity, authenticity, authentic timestamp,
expiry and revocation; `permissive` enforces integrity and authenticity and only logs timestamp, expiry and
revocation failures; `audit` enforces integrity only and logs the rest; `skip` performs no verification and
cannot be used with the global scope `*`. Each scope must be a fully qualified repository URI (no
asterisk) or the single value `*`, and an artifact with no applicable trust policy fails verification.
Revocation uses the OCSP or CRL information in the certificate, if present.

## In Kubernetes
Admission controllers that support Notation verification (the Notary Project documents Kubernetes
verification scenarios) can enforce signatures before deployment.

## Gotchas
- The registry must store OCI artifacts that reference the signed image (the Harbor docs describe Notation
  signing in distribution spec v1.1 mode).
- Tag references are resolved to digests before signing; sign in the same job that pushed.
- A `trustedIdentities` entry starting with `x509.subject:` must list RDNs and include country (C), state
  (ST or S) and organization (O); entries must not overlap. `*` trusts any certificate chaining to the trust store.

## Verify
`notation verify` returns the digest of the artifact on success; verifying an image whose signing
certificate is not in the trust store or whose identity is not trusted fails.

## Checked

2026-10-26. Documentation release: notaryproject/notaryproject.dev main (user guides and CLI reference), notaryproject/specifications trust-store-trust-policy.md main, Azure/notation-azure-kv docs and goharbor/website docs, checked 2026-10-26. Confirmed: notation cert generate-test --default, cert add --type ca --store, sign flags (--signature-format cose, --plugin/--id, --allow-referrers-api experimental), key add --plugin --id --default, plugin install --url --sha256sum, policy import/show, trust policy fields and level semantics, global scope and skip restriction, trustedIdentities subject rules, ls to list signatures. Fixed: the sample "everything-else" policy used level skip with the global scope, which the specification forbids. Removed unconfirmed claims: the AWS Signer plugin name, a list of supported registries, Ratify and Kyverno specifics, an exact-match rule for RDN order and spacing, and the "Successfully verified signature" message.

Method: documentation only; no commands were run.
