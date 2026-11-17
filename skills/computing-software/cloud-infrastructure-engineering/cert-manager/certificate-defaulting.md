---
id: computing-software.cloud-infrastructure-engineering.cert-manager.certificate-defaulting
name: certificate-defaulting
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [defaulting, kyverno, kustomize, csi-annotations, issuerref, policy]
level: practitioner
status: docs-checked
description: "Apply defaults to cert-manager certificates at the two defaulting points (before the CSR, before the X.509 certificate) and know what each point can default."
sources:
  - https://cert-manager.io/docs/policy/defaulting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults are pre-filled values that simplify requests; they do not block overrides, so pair them with an approval policy when you need enforcement.

Defaulting point 1, before the CSR is created (cert-manager side):
- Applied to the inputs that build the CSR, not the CSR; a CSR cannot be changed without breaking its signature.
- Targets the `Certificate` resource that generates the CSR, or CSI annotations/driver configuration.
- Can default private key properties (the key is not generated yet) and the issuer reference, for example a namespace defaulting to a particular issuer.

Defaulting point 2, before the X.509 certificate (issuer side):
- The issuer may default properties of the resulting certificate, or map CSR properties by any logic.
- It cannot default the issuer reference or private key properties; the key already exists.

Mechanisms the page names: Kyverno, to apply defaults dynamically to Certificate or CSI resources; and CI/CD templating such as Helm and kustomize.

Related: approval policy, which enforces; issuing policy, which describes what each issuer does.

## Checked

2026-11-03: Confirmed against the Defaulting Policy page: the two defaulting points, what each can default (private key properties and issuerRef only before the CSR), CSR immutability, Certificate or CSI annotations as the target, and Kyverno, Helm and kustomize as mechanisms. Removed: the claim that a tutorial on default values exists in the docs (not on this page).

Method: documentation only; no commands were run.
