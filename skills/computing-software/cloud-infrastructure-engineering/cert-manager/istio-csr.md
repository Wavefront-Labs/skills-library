---
id: computing-software.cloud-infrastructure-engineering.cert-manager.istio-csr
name: istio-csr
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [istio-csr, istio, mtls, spiffe, enable-ca-server, service-mesh]
level: advanced
status: docs-checked
description: "Use istio-csr to sign Istio mesh workload certificates through cert-manager: install order, Istio settings, issuer constraints and what not to do."
sources:
  - https://cert-manager.io/docs/usage/istio-csr/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
istio-csr is an agent that implements the gRPC Istio certificate service. It authenticates, authorizes and signs CSRs from mesh members, delegating signing to cert-manager issuers, and aims to match istiod behaviour. It covers workload and control plane mTLS, intra- and inter-cluster.

Order of installation:
1. A cluster with no Istio installed yet.
2. cert-manager.
3. An Issuer or ClusterIssuer for Istio certificates.
4. istio-csr (likely via Helm).
5. Istio with custom configuration.

Istio settings: `ENABLE_CA_SERVER` to `false`; `caAddress` to the istio-csr address. Mount and statically specify the root CA (recommended); without it istio-csr auto-discovers roots, which could allow signer hijacking if a token is stolen. Example manifests are in the istio-csr repository.

Issuer choice: an `Issuer` is the recommended start (namespaced, simpler access control); a `ClusterIssuer` fits one trust domain across the cluster. CA, Vault or external issuers work. The issuer must accept arbitrary `subjectAltName`, because Istio puts SPIFFE IDs there, so ACME issuers (Let's Encrypt) will not work.

Failure mode: installing istio-csr after Istio is unsupported and "exceptionally difficult to do safely"; it likely needs downtime because sidecars must trust both the old Istio CA and the new cert-manager CA.

## Checked

2026-11-03: Confirmed against the Securing Istio Service Mesh page: what istio-csr does, the five-step install order, `ENABLE_CA_SERVER` false and `caAddress`, the recommended static root CA and the signer hijacking risk, Issuer versus ClusterIssuer guidance, CA/Vault/external issuer types, the arbitrary `subjectAltName` requirement and why ACME fails, and the unsupported install-after-Istio case. Removed: the closing remark about Helm values (not a claim from the page).

Method: documentation only; no commands were run.
