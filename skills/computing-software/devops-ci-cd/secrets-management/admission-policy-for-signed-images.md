---
id: computing-software.devops-ci-cd.secrets-management.admission-policy-for-signed-images
name: admission-policy-for-signed-images
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, admission-control, admission-policy, kyverno, verify-signatures, verifyimages, sigstore-policy-controller, clusterimagepolicy, cosign-verify, keyless-identity, oidc-issuer, attestation-policy, digest-mutation, validatingadmissionpolicy, cel-admission, audit-mode, enforce-mode, kubernetes]
level: advanced
status: docs-checked
description: "Refuse unsigned images at admission: Kyverno verifyImages and Sigstore policy-controller keyless identities, attestation checks, digest mutation, no-match policy."
sources: ["https://kyverno.io/docs/policy-types/cluster-policy/verify-images/sigstore/", "https://docs.sigstore.dev/policy-controller/overview/", "https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admission policy for signed images

**Goal:** a pod whose image was not signed by your release workflow, or lacks the attestations you require, never starts, and legitimate deploys do not get blocked by a policy typo.

## 1. Kyverno `verifyImages`
- A rule fails if the required signatures are not found in the OCI registry or the image was not signed by matching attestors. Images can carry multiple signatures.
- `mutateDigest` (default `true`) rewrites a tag to the image digest if none is specified, making the reference immutable so what was verified is what runs.
- A `verifyImages` rule verifies signatures or attestations, not both. The `attestors` object under the rule is for image signatures; under `attestations` it is for attestations only. Use separate rules or entries accordingly.
- Attestation policies fetch the attestation, verify the signature, decode the predicate and apply `conditions` to it. Sign attestations with `cosign attest`; view or verify with `cosign verify-attestation`.
- Keyless: match on `subject` and `issuer` (exact, or `subjectRegExp` / `issuerRegExp`), with a Rekor `url`. For GitHub workflow signing the issuer is `https://token.actions.githubusercontent.com` and the subject is the workflow identity, for example `https://github.com/ORG/REPO/.github/workflows/WORKFLOW@refs/tags/*`. The subject and issuer in the policy must match the identity used when signing.
- `ignoreTlog` and `ignoreSCT` set to `true` are for testing only; keep the defaults for higher security.
- Use `webhookTimeoutSeconds` generously (the examples use 30).

## 2. Sigstore policy-controller
- Enforcement is per namespace: by default only namespaces labelled `policy.sigstore.dev/include: "true"` are validated (opt-out is possible by editing the webhook configurations' `matchExpressions`, which may cause grief in system namespaces).
- `ClusterImagePolicy` `spec.images` lists `glob` patterns matched against image digests of PodSpec-bearing resources (Deployments and so on, by default, not only Pods). `**` matches any number of characters; a host-less glob defaults to `index.docker.io`.
- Admission: an image must satisfy every matching `ClusterImagePolicy` (AND), and within each policy at least one passing `authority` (OR).
- `no-match-policy` (`warn`, `allow` or `deny`) lives in the `config-policy-controller` ConfigMap in the release namespace (default `cosign-system`). The doc says an image matching no policy is rejected by default when `no-match-policy` is unset; while rolling out, consider `warn`.
- Authorities: `key` (secretRef or kms), or `keyless` with Fulcio `url` and `identities` (`issuer` and `subject`, or `issuerRegExp` / `subjectRegExp`); `ctlog` defaults to the public Rekor instance; `static` authorities (`pass` or `fail`) cover images with no signatures, such as sidecars.
- `attestations` entries have a `predicateType` (for example `https://slsa.dev/provenance/v1`) and can apply `cue` or `rego` policy. Plain signatures are not supported in the new bundle format; set `signatureFormat: bundle` in the policy when attesting with `--new-bundle-format`.
- policy-controller resolves image tags to digests so the image run matches what was admitted.

## 3. ValidatingAdmissionPolicy (built in)
Uses CEL expressions in `spec.validations`, with `matchConstraints` and a binding whose `validationActions` are `Deny`, `Warn` or `Audit` (`Deny` and `Warn` cannot be combined). Use `Warn`/`Audit` first, then `Deny`.

## 4. Rollout
Start in audit or warn mode, collect results, fix unsigned images, then enforce namespace by namespace. Keep policy-engine system namespaces from blocking their own upgrade by excluding them or verifying them against vendor identities.

## Verify
- [ ] A pod from an unsigned image is denied with a message naming the policy.
- [ ] A signed release image is admitted and, with Kyverno, shows the digest after mutation.
- [ ] The keyless subject is narrow (specific workflow path and tag ref), not `https://github.com/*`.

## Checked
Method: docs-checked 2026-11-09 against the Kyverno "Verify images with Sigstore" ClusterPolicy page (opening, keyless, attestations and ignoreTlog sections), the Sigstore policy-controller overview, and the Kubernetes ValidatingAdmissionPolicy reference (CEL and validationActions sections).
Removed as unconfirmed, including a correction: the draft's claim that policy-controller allows unmatched images by default is wrong per the overview (unset `no-match-policy` rejects). Also removed: the comparison table, the full ClusterPolicy and ClusterImagePolicy YAML examples, Helm install commands, `--imageVerifyCacheEnabled`, `--imagePullSecrets`, the `kyverno.io/verify-images` annotation, `PolicyException` handling, SBOM and licence conditions, per-environment guidance, HA/PDB/failurePolicy advice, metric alerts, `kyverno apply`/`kyverno test` commands, and the claim that ValidatingAdmissionPolicy cannot verify signatures.
