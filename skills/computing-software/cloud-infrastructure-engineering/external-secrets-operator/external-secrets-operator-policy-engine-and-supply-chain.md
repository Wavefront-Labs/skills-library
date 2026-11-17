---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-policy-engine-and-supply-chain
name: external-secrets-operator-policy-engine-and-supply-chain
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [security, kyverno, opa, cosign]
level: advanced
status: docs-checked
description: "Enforce ESO usage rules with Kyverno or OPA Gatekeeper and verify the signed container images with cosign."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/security-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policy recommendations: explicitly deny unused providers in `SecretStore` specs (the docs give a Kyverno policy validating the `provider` field), restrict `spec.data[].remoteRef.key` to allowed prefixes, and limit which ExternalSecrets may reference a ClusterSecretStore. ESO does not ship policies.

Pod security: the pods meet the restricted Pod Security Standard by default since v0.8.2.

The chart is hardened for ease of use, not your threat model; misconfiguration from using it as shipped is outside the support policy. Consider using it as a dependency of your own chart to layer NetworkPolicies and RBAC. Patch ESO and the cluster regularly.

Images are signed with Cosign keyless signing. Find the digest with `crane digest ghcr.io/external-secrets/external-secrets:<tag>` then run `cosign verify` against `ghcr.io/external-secrets/external-secrets@sha256:<digest>`, checking the certificate identity and issuer.

## Checked

2026-11-03. Claims were read against guides/security-best-practices.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
