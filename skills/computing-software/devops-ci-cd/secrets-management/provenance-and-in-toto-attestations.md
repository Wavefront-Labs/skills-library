---
id: computing-software.devops-ci-cd.secrets-management.provenance-and-in-toto-attestations
name: provenance-and-in-toto-attestations
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, in-toto, attestation, attestations, artifact-attestations, attest-build-provenance, attest-sbom, slsa-github-generator, slsa-provenance, provenance-verification, slsa-verifier, gh-attestation-verify, dsse-envelope, predicate-type, subject-digest, statement, sigstore-bundle, rekor, fulcio, cosign-attest, cosign-verify-attestation, oci-referrers, vsa, verification-summary-attestation, policy-at-deploy, build-l3]
level: advanced
status: gated
description: "Produce and verify build provenance: in-toto statement and DSSE structure, GitHub artifact attestations and slsa-github-generator, cosign attest, verifying with gh/slsa-verifier/cosign, deploy gates."
sources: ["https://slsa.dev/spec/v1.0/provenance", "https://github.com/in-toto/attestation/tree/main/spec", "https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds", "https://github.com/slsa-framework/slsa-verifier", "https://docs.sigstore.dev/cosign/verifying/attestation/", "https://github.com/slsa-framework/slsa-github-generator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provenance and in-toto attestations

**Goal:** every release artifact carries a signed statement of *where it came from and
how it was built*, and something downstream refuses artifacts that don't.

## 1. The format (so the tooling makes sense)
An **in-toto attestation** = a **Statement** wrapped in a **DSSE envelope** (signed JSON):
```json
{ "_type": "https://in-toto.io/Statement/v1",
  "subject": [{ "name": "ghcr.io/org/app", "digest": { "sha256": "9f86d0…" } }],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": { "buildType": "https://actions.github.io/buildtypes/workflow/v1",
      "externalParameters": { "workflow": { "ref": "refs/tags/v1.4.2", "repository": "https://github.com/org/app", "path": ".github/workflows/release.yml" } },
      "internalParameters": { "github": { "event_name": "push", "repository_id": "…" } },
      "resolvedDependencies": [{ "uri": "git+https://github.com/org/app@refs/tags/v1.4.2", "digest": { "gitCommit": "3c1f…" } }] },
    "runDetails": { "builder": { "id": "https://github.com/org/app/.github/workflows/release.yml@refs/tags/v1.4.2" },
      "metadata": { "invocationId": "https://github.com/org/app/actions/runs/123/attempts/1" } } } }
```
The **subject** is the artifact digest; the **predicate** is the claim (SLSA provenance,
SBOM `https://spdx.dev/Document`/CycloneDX, test results, vulnerability scan, a
Verification Summary Attestation). Signature via Sigstore (Fulcio cert bound to the
workflow's OIDC identity, logged in Rekor) or a key. Storage: GitHub's attestation API,
the OCI registry as a referrer (`cosign attest` pushes `sha256-<digest>.att`/referrers),
or a file next to the artifact (`.intoto.jsonl`, `.sigstore.json` bundle).

## 2. Producing provenance
**GitHub native (L2; L3 via reusable workflow on hosted runners):**
```yaml
permissions: { id-token: write, attestations: write, contents: read, packages: write }
steps:
  - id: build
    uses: docker/build-push-action@v7
    with: { push: true, tags: ghcr.io/${{ github.repository }}:${{ github.sha }} }
  - uses: actions/attest-build-provenance@v4        # latest tag v4.2.2 (README checked; not run in Actions)
    with:
      subject-name: ghcr.io/${{ github.repository }}
      subject-digest: ${{ steps.build.outputs.digest }}
      push-to-registry: true
  - uses: actions/attest-sbom@v4              # attach an SBOM predicate too (deprecated in favour of actions/attest with sbom-path)
    with: { subject-name: ghcr.io/${{ github.repository }}, subject-digest: ${{ steps.build.outputs.digest }}, sbom-path: sbom.spdx.json, push-to-registry: true }
```
For files: `subject-path: 'dist/*'` (one attestation per file, stored in GitHub; also
`.sigstore.json` bundles you can attach to the release).

**slsa-github-generator (L3):**
```yaml
jobs:
  build:
    outputs: { hashes: ${{ steps.hash.outputs.hashes }} }
    steps:
      - run: make dist
      - id: hash
        run: echo "hashes=$(sha256sum dist/* | base64 -w0)" >> "$GITHUB_OUTPUT"
  provenance:
    needs: build
    permissions: { actions: read, id-token: write, contents: write }
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v2.1.0   # pin by tag per their docs (v2.1.0 is the latest release)
    with: { base64-subjects: ${{ needs.build.outputs.hashes }}, upload-assets: true }
```
The generator runs as its *own* reusable workflow with its own identity — the build job
cannot forge it. Container variant: `generator_container_slsa3.yml` with `image` + `digest`.

**cosign (any CI):**
```bash
cosign attest --yes --type slsaprovenance1 --predicate provenance.json ghcr.io/org/app@sha256:…   # slsaprovenance1 = SLSA v1; plain `slsaprovenance` is v0.2
cosign attest --yes --type cyclonedx --predicate sbom.cdx.json ghcr.io/org/app@sha256:…
```
Run with a key against a local registry (cosign 3.1.3): `--type slsaprovenance1` produced predicateType `https://slsa.dev/provenance/v1` and `--type slsaprovenance`
produced `https://slsa.dev/provenance/v0.2`; `verify-attestation --type` filters on the same names, so pair them. Keyless in CI uses the job's OIDC token (GitHub, GitLab, Buildkite, Google, …); the
predicate here is written by your job → L2-class unless the signer is isolated.

**GitLab:** `RUNNER_GENERATE_ARTIFACTS_METADATA: "true"` → `artifacts-metadata.json`
per job (SLSA v1 provenance signed by GitLab); GitLab's `id_tokens` + cosign for images.

## 3. Verifying
```bash
# GitHub attestations (images or files); flags --owner --repo --signer-workflow --predicate-type --format --bundle exist in gh 2.92 `attestation verify --help`; no attested artifact was verified here (gated: unconfirmed)
gh attestation verify oci://ghcr.io/org/app:v1.4.2 --owner org
gh attestation verify dist/app-linux-amd64 --repo org/app --signer-workflow org/app/.github/workflows/release.yml
gh attestation verify … --predicate-type https://spdx.dev/Document --format json | jq '.[0].verificationResult.statement.predicate'

# slsa-github-generator output (flags below exist in slsa-verifier --help; a real provenance file was not available here: gated: unconfirmed)
slsa-verifier verify-artifact dist/app --provenance-path app.intoto.jsonl --source-uri github.com/org/app --source-tag v1.4.2
slsa-verifier verify-image ghcr.io/org/app@sha256:… --source-uri github.com/org/app --builder-id https://github.com/slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@refs/tags/v2.0.0

# cosign
cosign verify-attestation --type slsaprovenance1 \
  --certificate-identity-regexp '^https://github.com/org/app/.github/workflows/release.yml@refs/tags/v.*' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/org/app@sha256:… | jq -r .payload | base64 -d | jq .predicate.buildDefinition.externalParameters
```
What to assert, in order of value: (1) subject digest matches what you're deploying,
(2) signer identity = your release workflow at a protected ref (not `.*`), (3) issuer =
your CI, (4) source repo/tag match, (5) builder id is the trusted builder. A verify step
that only checks "a signature exists" is theatre.

## 4. Gating on it
- **Deploy pipeline**: verification step before `kubectl apply`/`helm upgrade`; fail
  closed. Cache the verification result as a **VSA** (`https://slsa.dev/verification_summary/v1`)
  signed by the deploy pipeline so admission can check one small attestation.
- **Admission**: Kyverno `verifyImages` with `attestations:` conditions on the predicate
  (`builder.id`, `externalParameters.workflow.repository`), or Sigstore policy-controller
  `ClusterImagePolicy` with `attestations: [{predicateType: slsaprovenance, policy: cue/rego}]`
  — see the admission-policy skill.
- **Package consumers**: npm `--provenance` publishes link to the workflow; `npm audit signatures`
  verifies; PyPI shows attestations (PEP 740) — ask upstreams for them.

## 5. Gotchas
- Subject must be the **digest** of what's deployed (image manifest digest, not the tag;
  for multi-arch, attest the index digest and/or each platform digest).
- `attest-build-provenance` from a **reusable** workflow records the caller's repo in
  `workflow.repository` and the reusable file as builder — your verify flags must match.
- Rekor transparency log is public: subjects/identities of private repos are visible as
  hashes and identities. GitHub attestations for private repos avoid the public log
  (use `gh attestation verify` with GitHub as the trust root).
- Attestations in registries are extra manifests: retention/cleanup jobs that delete
  "untagged" manifests will delete them — use tools that understand referrers.
- Clock/trust roots: `cosign` needs the Sigstore TUF root (`cosign initialize` in
  air-gapped setups with a mirrored root).

## Verify
- [ ] Every release image/file has a provenance attestation discoverable by digest.
- [ ] `gh attestation verify`/`slsa-verifier` with a *tight* identity passes; the same command with a wrong tag/repo fails.
- [ ] Deploy pipeline fails closed when the attestation is missing (tested by deploying a hand-built image).
- [ ] Predicate shows the expected builder id, source repo and tag for a sampled release.
