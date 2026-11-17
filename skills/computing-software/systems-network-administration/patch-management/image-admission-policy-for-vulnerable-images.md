---
id: computing-software.systems-network-administration.patch-management.image-admission-policy-for-vulnerable-images
name: image-admission-policy-for-vulnerable-images
category: computing-software
field: systems-network-administration
product: patch-management
tags: [image-admission-policy, image-scanning, kyverno, container-images, immutable-infrastructure, cosign]
level: advanced
status: docs-checked
description: "Block vulnerable or unscanned container images at Kubernetes admission with Kyverno: allowed registries, signatures and vulnerability attestations, with break-glass."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/verify-images/
  - https://kyverno.io/docs/policy-types/cluster-policy/policy-settings/
  - https://kyverno.io/docs/exceptions/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Admission policy for vulnerable images

Scanning in CI is advisory unless the cluster refuses what failed. Enforce at admission,
but base the decision on **signed scan results**, not a live scan at admission time.

## Layers
1. **Allowed registries only** (your registry/proxy, not docker.io directly).
2. **Signed images** (Sigstore Cosign or Notary, as supported by Kyverno) from your CI identity.
3. **Vulnerability attestation**: signed metadata attached to the image (for example created with cosign attest) that records the scan result and scan date, checked with `attestations` conditions.
4. Runtime rescans (registry scanning, Trivy Operator) to catch newly disclosed CVEs in
   already-running images; those trigger rebuilds, not evictions.

## Kyverno image verification
Kyverno's `verifyImages` rule (in a ClusterPolicy) checks image signatures and attestations. Fields to use: `imageReferences` (patterns to match), `skipImageReferences`, `required` (all matching images must be verified), `mutateDigest` (converts tags to digests; true by default), `verifyDigest` (enforces digests), `attestors` (how signatures are checked; Cosign supports public keys, certificates and keyless) and `attestations` (signed metadata whose JSON content is checked with `conditions`). Take the exact policy syntax for your Kyverno version from the verifyImages documentation, and add a separate rule denying images outside your registry.

## Rollout
Audit mode first (the `spec.validationFailureAction` field is deprecated as of Kyverno 1.13; use `failureAction` under the validate rule), review policy reports, fix pipelines,
then Enforce per namespace. Exclude system namespaces carefully.

## Break-glass
Documented exception: a PolicyException resource (disabled by default; enabled with the
`enablePolicyException` flag and limited to the namespaces set with `exceptionNamespace`),
approved by security, logged and reviewed for removal.

## Gotchas
- Admission webhooks failing closed can block all deployments during an outage: set
  timeouts and failurePolicy deliberately; run the policy engine HA.
- Tag-based references can change: enforce digests (`mutateDigest`).

## Verify
Unsigned or out-of-registry image is rejected with a clear message; signed, recently
scanned image deploys; PolicyReports show no unexpected violations.

## Checked
Date: 2026-10-27. Documentation checked against Kyverno (v1.19 documentation set): verifyImages page (field names above, Cosign and Notary support, `mutateDigest` default true), policy settings page (`validationFailureAction` deprecated as of 1.13), validate page, and the Policy Exceptions page (`enablePolicyException`, `exceptionNamespace`). Removed the full YAML example, the SARIF/KEV attestation wording and the exception-expiry claim, none of which the documentation confirms; the description no longer mentions Gatekeeper because the body does not cover it.

Method: documentation only; no commands were run.
