---
id: computing-software.cybersecurity-defensive.cloud-security.image-signature-admission-control
name: image-signature-admission-control
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-workload-protection, image-signing-admission, cosign, sigstore, kyverno-verify-images, policy-controller, notation, binary-authorization, supply-chain-security]
level: advanced
status: draft
description: "Enforce that only signed, trusted images run in Kubernetes: cosign/Notation signing in CI, admission verification with Kyverno, Sigstore policy-controller or Binary Authorization."
sources: ["Sigstore cosign documentation", "Kyverno verifyImages documentation", "Google Cloud Binary Authorization documentation", "SLSA v1.0 specification"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image signature admission control

**Goal:** clusters run only images built and signed by your pipelines, so a pushed malicious
image or typo-squatted public image cannot be deployed.

## Sign in CI
Keyless (Sigstore, OIDC identity of the CI job):
```
cosign sign --yes registry.example.com/app@sha256:<digest>
cosign attest --yes --type slsaprovenance --predicate provenance.json registry.example.com/app@sha256:<digest>
```
Key-based alternative: `cosign sign --key awskms:///alias/cosign registry.example.com/app@sha256:<digest>`.
Notation (Notary Project) with Azure Key Vault / AWS Signer is the alternative on ACR/ECR.
Always sign by **digest**, not tag.

## Verify at admission (Kyverno)
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: verify-images}
spec:
  validationFailureAction: Enforce
  webhookTimeoutSeconds: 30
  rules:
  - name: signed-by-ci
    match: {any: [{resources: {kinds: [Pod]}}]}
    verifyImages:
    - imageReferences: ["registry.example.com/*"]
      mutateDigest: true
      attestors:
      - entries:
        - keyless:
            issuer: https://token.actions.githubusercontent.com
            subject: "https://github.com/example-org/*/.github/workflows/release.yml@refs/heads/main"
```
Alternatives: Sigstore **policy-controller**, Gatekeeper with Ratify, GKE **Binary Authorization**, AKS image integrity (preview features vary).

## Rollout
1. Audit mode (`validationFailureAction: Audit`) to find unsigned images.
2. Sign third-party images you depend on after vetting (re-sign into your registry) or allow specific publishers' signatures.
3. Exclude system namespaces carefully; enforce on application namespaces.
4. Also restrict registries (only your registry and mirrors).

## Gotchas
- Verifying the subject too loosely (any workflow in any repo) lets any pipeline sign; pin repo, workflow and branch.
- Admission webhook outage: fail-closed blocks deployments, fail-open allows unsigned; pick and monitor.
- Tags are mutable; `mutateDigest` pins the verified digest into the pod spec.

## Verify
- [ ] Deploying an unsigned test image to an enforced namespace is rejected.
- [ ] Signed release images deploy normally; policy reports show no audit violations.
