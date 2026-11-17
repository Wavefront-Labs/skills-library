---
id: computing-software.cryptography-implementation.protocol-implementation.private-acme-with-step-ca
name: private-acme-with-step-ca
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, step-ca, private-acme, acme, eab, smallstep, internal-pki]
level: advanced
status: gated
description: "Run a private ACME CA with smallstep step-ca: init, ACME provisioner, External Account Binding, short-lived certs, and pointing certbot or cert-manager at it."
sources: ["https://smallstep.com/docs/step-ca/", "https://smallstep.com/docs/step-ca/provisioners/#acme", "https://www.rfc-editor.org/rfc/rfc8555#section-7.3.4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private ACME with step-ca

## Set up
```sh
step ca init --name "Example Internal CA" --dns ca.internal.example --address :443 --provisioner admin
step ca provisioner add acme --type ACME
step-ca $(step path)/config/ca.json
```
Root and intermediate are created; protect the root key offline (or use `--ra` / KMS-backed keys (gated: unconfirmed, source is paywalled or blocked)).

## External Account Binding
```sh
step ca provisioner add acme-eab --type ACME --require-eab
step ca acme eab add acme-eab team-payments      # prints key ID and HMAC key (gated: unconfirmed, source is paywalled or blocked)
```
Clients must present the EAB key ID and HMAC key when registering (RFC 8555 7.3.4), so only approved teams get
certificates.

## Clients
```sh
certbot certonly --server https://ca.internal.example/acme/acme/directory \
  --standalone -d app.internal.example
```
cert-manager `ClusterIssuer` with `acme.server` set to the directory URL, `caBundle` with the internal root,
and `externalAccountBinding` for EAB.

## Policy
- The provisioner `claims` set `defaultTLSCertDuration` and `maxTLSCertDuration` (the provisioners page shows 24h in its example and 2h in others); tune them per provisioner.
- Restrict names with provisioner policy (`x509.allow.dns: ["*.internal.example"]` (gated: unconfirmed, source is paywalled or blocked)).
- Distribute the root to clients (`step certificate install root_ca.crt`).

## Verify
- [ ] Certbot issuance and renewal succeed; a request outside the allowed DNS policy is rejected.

## Checked

- Date: 2026-11-02.
- Confirmed against: step-ca provisioners page (`step ca provisioner add acme --type ACME`, claims defaultTLSCertDuration / maxTLSCertDuration shown as 24h and 2h in examples) and RFC 8555 section 7.3.4 (external account binding).
- Gated: the EAB provisioner flag and `step ca acme eab add` command, the policy syntax and `--ra`; the fetched step-ca pages do not state them.

Method: documentation only; no commands were run.
