---
id: computing-software.cloud-infrastructure-engineering.kubernetes.attestation-verification-at-admission
name: attestation-verification-at-admission
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, verify-attestations, attestation-verification, slsa, cosign, kyverno, sigstore-policy-controller, supply-chain, cks]
level: advanced
status: docs-checked
description: "Admit only images with valid SLSA provenance or scan attestations: cosign verify-attestation, Kyverno verifyImages attestations, Sigstore policy-controller, and rollout safety."
sources: ["https://kyverno.io/docs/policy-types/cluster-policy/verify-images/sigstore/", "https://kyverno.io/docs/policy-types/image-validating-policy/", "https://docs.sigstore.dev/policy-controller/overview/", "https://docs.sigstore.dev/cosign/verifying/verify/", "https://slsa.dev/spec/v1.0/provenance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying attestations at admission

Signature verification proves *who* pushed an image. Attestation verification proves *how*
it was built (SLSA provenance: which repo, workflow, builder) or *what was checked* (vuln
scan, SBOM present). Enforce both.

## 1. Check by hand first
```bash
cosign verify-attestation ghcr.io/acme/api@sha256:<digest> \
  --type slsaprovenance1 \
  --certificate-identity-regexp '^https://github.com/slsa-framework/slsa-github-generator/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  | jq -r '.payload | @base64d | fromjson | .predicate.runDetails.builder.id'
```
For GitHub artifact attestations use `gh attestation verify oci://ghcr.io/acme/api@sha256:... --owner acme`.

## 2. Kyverno
Kyverno `ClusterPolicy` (`kyverno.io/v1`) is deprecated as of Kyverno v1.19 and removed in v1.20 (estimated Nov 2026); the CEL-based `ValidatingPolicy`/`ImageValidatingPolicy` types (`policies.kyverno.io/v1`) are stable since v1.18. The YAML below is the legacy form still used by the policy library. Prefer `ImageValidatingPolicy` for new work.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: require-provenance}
spec:
  validationFailureAction: Audit          # switch to Enforce after soak
  webhookTimeoutSeconds: 15
  rules:
  - name: slsa-provenance
    match: {any: [{resources: {kinds: [Pod]}}]}
    verifyImages:
    - imageReferences: ["ghcr.io/acme/*"]
      mutateDigest: true                  # pin tag to verified digest
      attestations:
      - type: https://slsa.dev/provenance/v1
        attestors:
        - entries:
          - keyless:
              subject: "https://github.com/acme/*/.github/workflows/release.yml@refs/heads/main"
              issuer: https://token.actions.githubusercontent.com
              rekor: {url: https://rekor.sigstore.dev}
        conditions:
        - all:
          - key: "{{ buildDefinition.buildType }}"
            operator: Equals
            value: "https://actions.github.io/buildtypes/workflow/v1"
```
The CEL-based `ImageValidatingPolicy` (`policies.kyverno.io/v1`, stable since Kyverno v1.18) takes
`matchImageReferences`, `attestors` (cosign keys, keyless identities, notary) and `attestations`
(in-toto predicate types or OCI referrers); same concepts.

## 3. Sigstore policy-controller (alternative)
Opt-in per namespace with label `policy.sigstore.dev/include=true`, then a
`ClusterImagePolicy` with `authorities` (keyless identities) and `attestations` entries
(`predicateType` plus an optional CUE or Rego policy over the predicate).

## Rollout safety
- Start in Audit; read PolicyReports (`kubectl get polr -A`) for misses.
- Exclude kube-system and third-party images you cannot attest, by image pattern (`skipImageReferences` in Kyverno), not namespace-wide.
- Admission makes network calls to the registry and Rekor: set `failurePolicy` and timeouts
  deliberately, and mirror/cache for air-gapped clusters (private Rekor/TUF root).
- Attestations attach to a **digest**; tags moved after signing fail verification. Deploy by digest.

## Verify
- [ ] An image built outside CI (local `docker push`) is rejected with a clear message.
- [ ] A CI-built image is admitted and the pod spec shows the digest.

## Checked

Checked 2026-10-27 against Kyverno docs source (kyverno/website, main; policy types overview and sigstore pages describe Kyverno v1.19), the Sigstore docs source (sigstore/docs), the cosign CLI reference and the SLSA spec source.

- `cosign verify-attestation --type` accepts `slsaprovenance1` among its predicate types, and `--certificate-identity-regexp` / `--certificate-oidc-issuer` are the keyless flags; both confirmed in the cosign reference.
- SLSA provenance v1 fields: `runDetails.builder.id` and `buildDefinition.buildType` confirmed in the SLSA spec; the earlier `externalParameters.workflow` path was not documented and was replaced with the documented Kyverno example condition on `buildDefinition.buildType`.
- Kyverno `verifyImages` keyless `subject`/`issuer`/`rekor.url`, `attestations` with `type: https://slsa.dev/provenance/v1`, `conditions`, `mutateDigest` (default true) and `skipImageReferences` confirmed; ClusterPolicy deprecation and `ImageValidatingPolicy` (stable v1.18) confirmed in the policy types overview.
- Sigstore policy-controller namespace label `policy.sigstore.dev/include=true`, `ClusterImagePolicy` authorities and attestations, and the `no-match-policy` setting confirmed.
- `gh attestation verify oci://... --owner` confirmed in the GitHub CLI manual.

Method: documentation only; no commands were run.
