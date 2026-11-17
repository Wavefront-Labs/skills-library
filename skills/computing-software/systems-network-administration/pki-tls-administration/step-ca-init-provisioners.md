---
id: computing-software.systems-network-administration.pki-tls-administration.step-ca-init-provisioners
name: step-ca-init-provisioners
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [step-ca-init-provisioners, pki-step-ca, step-ca, smallstep, provisioner, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Initialise a step-ca private CA, add an ACME provisioner, set certificate lifetimes and bootstrap clients with the root fingerprint."
sources:
  - https://smallstep.com/docs/step-ca/getting-started/
  - https://smallstep.com/docs/step-ca/provisioners/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# step-ca initialisation and provisioners
Goal: a private online CA with automated issuance.
```
step ca init --name "Example Internal CA" --dns ca.example.com --address :443 --provisioner admin@example.com
step ca provisioner add acme --type ACME
step ca bootstrap --ca-url https://ca.example.com --fingerprint <FP>
step ca certificate app.example.com app.crt app.key
```
- Config lives in `$(step path)/config/ca.json`; `step ca provisioner` commands edit it and are recommended over hand edits. The CA starts with `step-ca $(step path)/config/ca.json`.
- `defaultTLSCertDuration` can be set per provisioner; the default certificate lifetime is 24 hours.
- Provisioner types include JWK, OAuth/OIDC, X5C, ACME, SCEP and others; the Provisioners page tabulates what each can do.
- Production: keep the root key offline (HSM or air-gapped device) and the intermediate key in a cloud HSM or KMS the CA uses for signing; change the intermediate key password right after init with `step crypto change-pass`.
Gotcha: the root is self-signed, so clients are not trusted automatically; they establish trust by supplying the CA fingerprint to `step ca bootstrap`. Record the fingerprint printed at init.
Verify:
- [ ] `step ca certificate app.example.com app.crt app.key` succeeds from a bootstrapped client.
- [ ] `openssl x509 -in app.crt -noout -dates` shows the expected lifetime.

## Checked
2026-11-03. Confirmed on the step-ca Getting Started, `step ca init` reference, Provisioners and Production pages: `--name`, `--dns`, `--address`, `--provisioner`, `step ca provisioner add acme --type ACME`, `ca.json` location and `step ca provisioner` recommendation, `defaultTLSCertDuration`, 24 hour default, `step ca bootstrap --ca-url --fingerprint`, `step ca certificate`, `step ca root root.crt`, `step-ca $(step path)/config/ca.json`, offline root and HSM/KMS intermediate guidance, `step crypto change-pass`. Removed: the OIDC command and its flags, `maxTLSCertDuration` and the `claims` wording, the systemd and `setcap` advice, `step ca health` and `step certificate inspect` checks.
Method: documentation only; no commands were run.
