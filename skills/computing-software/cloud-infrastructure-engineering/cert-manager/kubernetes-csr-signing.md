---
id: computing-software.cloud-infrastructure-engineering.cert-manager.kubernetes-csr-signing
name: kubernetes-csr-signing
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [certificatesigningrequest, csr, signername, experimental, subjectaccessreview, feature-gates]
level: advanced
status: docs-checked
description: "Let cert-manager sign native Kubernetes CertificateSigningRequests: enable the experimental gate, signerName formats, reference RBAC and request annotations."
sources:
  - https://cert-manager.io/docs/usage/kube-csr/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Experimental: behaviour may change. API is `certificates.k8s.io/v1` `CertificateSigningRequest`.

Enable the controller feature gate `ExperimentalCertificateSigningRequestControllers=true` via `--feature-gates`; with Helm set `featureGates` and `crds.enabled=true`. All internal Issuer types are supported.

Signer names:
- Issuer: `issuers.cert-manager.io/<namespace>.<name>`
- ClusterIssuer: `clusterissuers.cert-manager.io/<name>`

RBAC: CSRs are cluster-scoped, so for a namespaced Issuer cert-manager runs a SubjectAccessReview. The requester needs the verb `reference` on `signers` (apiGroup `cert-manager.io`) in that namespace; `resourceNames` is an Issuer name or `"*"`.

Approval: cert-manager does not auto-approve CSRs referencing an Issuer. Use standard flow, e.g. `kubectl certificate approve <name>`.

Requester annotations:
- `experimental.cert-manager.io/request-duration`: Go duration, default 90 days (CyberArk and ACME often reject custom durations).
- `experimental.cert-manager.io/request-is-ca`: `"true"` for a CA certificate.
- `experimental.cert-manager.io/private-key-secret-name`: required for SelfSigned; the Secret key `tls.key` holds the PEM key.
- `venafi.experimental.cert-manager.io/custom-fields`: CyberArk only, JSON array of `name`/`value`.

The CyberArk signer records its submission Pickup ID in `venafi.experimental.cert-manager.io/pickup-id`.

The experimental `cmctl` command can take a Certificate manifest, generate a key and create the CSR.

## Checked

2026-11-03: Confirmed against the CertificateSigningRequest page: experimental status, `certificates.k8s.io/v1`, the `ExperimentalCertificateSigningRequestControllers=true` feature gate (flag and Helm `featureGates`), all internal issuers supported, no auto-approval, signerName formats for Issuer and ClusterIssuer, the SubjectAccessReview with the `reference` verb on `signers` and `resourceNames` rules, the four requester annotations (90 day default duration) and the CyberArk pickup-id signer annotation, and the cmctl usage with manual approval. Nothing removed.

Method: documentation only; no commands were run.
