---
id: computing-software.devops-ci-cd.release-engineering.promotion-gated-on-attestations
name: promotion-gated-on-attestations
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, promotion-attestation, artifact-promotion, cosign-verify-attestation, kyverno-verify-images, binary-authorization, policy-gate]
level: practitioner
status: draft
description: "Gate artifact promotion between environments on signed attestations: test, scan and approval attestations with cosign, verifying them in pipelines and admission policies."
sources:
  - https://docs.sigstore.dev/cosign/verifying/attestation/
  - https://cloud.google.com/binary-authorization/docs/overview
  - https://github.com/in-toto/attestation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Promotion gated on attestations

Instead of trusting "the pipeline ran", each stage records a signed attestation about the artifact digest (tests passed, scan clean, change approved). Promotion to the next environment verifies the required attestations exist and are signed by the right identity.

## Produce attestations
```bash
DIGEST=ghcr.io/org/app@sha256:abc...
# provenance (build)
cosign attest --yes --type slsaprovenance --predicate provenance.json $DIGEST
# test results (custom predicate type)
jq -n --arg suite integration --arg result passed --arg run "$GITHUB_RUN_ID" \
  '{suite:$suite, result:$result, run:$run}' > test.json
cosign attest --yes --type https://example.com/attestations/test/v1 --predicate test.json $DIGEST
# vulnerability scan
trivy image --format cosign-vuln -o vuln.json $DIGEST
cosign attest --yes --type vuln --predicate vuln.json $DIGEST
```
Keyless signing from CI binds each attestation to the workflow identity (Fulcio cert with repo, workflow, ref).

## Verify in the promotion job
```bash
cosign verify-attestation --type https://example.com/attestations/test/v1 \
  --certificate-identity-regexp '^https://github.com/org/app/.github/workflows/test.yml@refs/heads/main$' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --policy test-policy.cue $DIGEST
```
```cue
// test-policy.cue
predicate: { result: "passed", suite: "integration" }
```
Promote by digest (copy/retag `crane copy $DIGEST registry/prod/app:1.4.0`, or update the GitOps repo with the digest) only after every required verification passes.

## Enforce at the destination
- Kubernetes: Kyverno `verifyImages` with `attestations:` conditions, or Sigstore policy-controller `ClusterImagePolicy`, so a manually pushed image without attestations is rejected at admission.
```yaml
verifyImages:
- imageReferences: ["ghcr.io/org/*"]
  attestations:
  - type: https://example.com/attestations/test/v1
    attestors: [{ entries: [{ keyless: { subject: "https://github.com/org/app/.github/workflows/test.yml@refs/heads/main", issuer: "https://token.actions.githubusercontent.com" } }] }]
    conditions: [{ all: [{ key: "{{ result }}", operator: Equals, value: passed }] }]
```
- GKE/Cloud Run: Binary Authorization attestors per stage (`build-attestor`, `qa-attestor`); prod policy requires both.
- AWS: Signer + admission webhook or ECR image signing with Notation.

## Approval as an attestation
Record human sign-off (change ticket ID, approver) as an attestation from the approval job instead of a comment; the prod gate requires it.

## Pitfalls
- Verifying tags instead of digests: tags move. Always resolve and pin the digest.
- Identity regex too broad (`.*`) lets any workflow in the org mint "tests passed".
- Attestations stored in the registry are copied with `cosign copy`, not with plain `docker push`.

## Verify
- [ ] An image missing the test attestation is refused by the promotion job and by admission.
- [ ] Attestation signed by a different workflow fails verification.
