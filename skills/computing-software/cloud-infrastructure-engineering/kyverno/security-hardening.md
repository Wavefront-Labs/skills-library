---
id: computing-software.cloud-infrastructure-engineering.kyverno.security-hardening
name: security-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [security-hardening, cosign-verify, sbom, slsa, networkpolicy, webhook-security, supply-chain]
level: practitioner
status: docs-checked
description: "Harden a Kyverno install: verify signed releases and SBOMs, default pod security, RBAC, optional NetworkPolicy ports, webhooks, certificates and HTTP restriction flags."
sources:
  - https://kyverno.io/docs/guides/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supply chain: images, manifests and Helm charts are signed with Cosign keyless. Set `COSIGN_REPOSITORY=ghcr.io/kyverno/signatures`, verify, and compare the `Issuer` and `Subject` to the expected GitHub Actions release workflow; a mismatch means the artifact is not genuine. Builds meet SLSA Level 3 (`cosign verify-attestation --type slsaprovenance`). Each release, pre-releases included, publishes a CycloneDX SBOM at `ghcr.io/kyverno/sbom` (`cosign download sbom`).

Pod defaults follow the `restricted` Pod Security Standard: `runAsNonRoot: true`, `privileged: false`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, all capabilities dropped, plus limits and probes.

RBAC: role `kyverno:admission-controller` configures webhooks; limit and audit it. List with `kubectl get clusterroles,roles -A | grep kyverno`.

Networking: no NetworkPolicy by default, so the webhook is reachable from any pod. Helm `networkPolicy.enabled` adds ingress only; add egress yourself. Needed flows: ingress 9443 (webhook, health), ingress 8000 (metrics), egress to the API server, DNS, OCI registries and any external services. Confirm your CNI enforces NetworkPolicy and replace placeholder CIDRs and namespaces.

Webhooks (policy, resource, verify, cleanup, exception) are fail-closed by default, tunable per policy. Certificates are generated and managed automatically; custom CAs are in the installation docs. Restrict CEL HTTP calls with `allowHTTPInNamespacedPolicies`, `httpBlocklist`, `httpAllowlist`. System namespaces, the Kyverno namespace included, are excluded by default via ConfigMap.

Governance: protect policies with RBAC, vet community policies, test with `kyverno test`, and adopt at least the Pod Security Standards and Best Practices sets. Vulnerability disclosure goes to the kyverno-security group email.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
