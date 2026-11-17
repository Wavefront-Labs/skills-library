---
id: computing-software.cloud-infrastructure-engineering.cert-manager.acme-issuer
name: acme-issuer
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [acme, letsencrypt, externalaccountbinding, privatekeysecretref, solvers, selector, preferredchain]
level: practitioner
status: docs-checked
description: "Configure a cert-manager ACME issuer: server, account key, profile, External Account Binding, solver selectors and waitInsteadOfSelfCheck."
sources:
  - https://cert-manager.io/docs/configuration/acme/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core fields under `spec.acme`:
- `email`: contact address (replace the example).
- `server`: directory URL; the examples use Let's Encrypt staging `https://acme-staging-v02.api.letsencrypt.org/directory`.
- `privateKeySecretRef.name`: Secret holding the account key. Lose it and you cannot revoke certificates issued under that account.
- `profile` (v1.18.0+): optional, e.g. `tlsserver`; Let's Encrypt uses `classic` when omitted. An unsupported profile errors the CertificateRequest.
- `solvers`: list of `http01` or `dns01` stanzas.
- `disableAccountKeyGeneration: true` reuses the key in `privateKeySecretRef`; the issuer stays not-ready until that Secret exists.
- `caBundle`: base64 PEM for private ACME servers (1.11+).
- `preferredChain`: Common Name of the wanted chain issuer, e.g. `"ISRG Root X1"`; the server may ignore it.

External Account Binding: `externalAccountBinding.keyID` and `keySecretRef` (`name`, `key`) holding the base64URL MAC key. `keyAlgorithm` is deprecated (HS256 is hardcoded).

Solver selection (`solvers[].selector`): `matchLabels`, `dnsNames` (exact; `*.example.com` does not match `foo.example.com`) and `dnsZones` (zone plus subdomains). `dnsNames` beats `dnsZones`; the more specific zone wins; then most matching labels; then list order. Types within a block are ANDed.

`waitInsteadOfSelfCheck` (v1.21.0+, on a solver, e.g. `30s`; `0` allowed, negative rejected) replaces the self-check when cert-manager cannot see the ACME server's validation path (split-horizon DNS, NAT loopback). Too short risks premature validation; too long delays issuance.

## Checked

2026-11-03. Confirmed on the cert-manager ACME page (configuration/acme): core fields, profile (v1.18.0), disableAccountKeyGeneration, caBundle (1.11), preferredChain, External Account Binding and the deprecated keyAlgorithm, solver selector precedence, waitInsteadOfSelfCheck (v1.21.0, 0 allowed, negative rejected). Nothing removed.
Method: documentation only; no commands were run.
