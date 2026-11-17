---
id: computing-software.cloud-infrastructure-engineering.docker.cosign-attest-and-verify-attestation
name: cosign-attest-and-verify-attestation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, attestations, cosign-attest, verify-attestation, in-toto, sbom, vuln-attestation, sigstore]
level: advanced
status: docs-checked
description: "Attach signed in-toto attestations (SBOM, vuln scan, custom predicates) to images with cosign attest, and verify them with predicate types, identities and CUE/Rego policies."
sources: ["https://docs.sigstore.dev/cosign/verifying/attestation/", "https://github.com/sigstore/cosign/blob/main/doc/cosign_attest.md", "https://github.com/sigstore/cosign/blob/main/doc/cosign_verify-attestation.md", "https://github.com/in-toto/attestation/tree/main/spec/predicates", "https://trivy.dev/latest/docs/configuration/reporting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign attest and verify-attestation

BuildKit attestations (`--sbom`, `--provenance`) are unsigned unless you sign the image
index. `cosign attest` creates a **signed** in-toto statement about an image digest, for
any predicate you produce: SBOMs, scan results, test reports, approvals.

## Attest
```bash
IMG=reg.example.com/app@sha256:<digest>          # always the digest
syft "$IMG" -o cyclonedx-json > sbom.cdx.json
cosign attest --yes --type cyclonedx --predicate sbom.cdx.json "$IMG"           # keyless (OIDC)
trivy image --format cosign-vuln -o vuln.json "$IMG"
cosign attest --yes --type vuln --predicate vuln.json "$IMG"
cosign attest --key cosign.key --type https://example.com/test-report/v1 --predicate tests.json "$IMG"
```
Built-in `--type` shortcuts: `slsaprovenance`, `slsaprovenance02`, `slsaprovenance1`, `spdx`, `spdxjson`,
`cyclonedx`, `vuln`, `openvex`, `link`, `custom`; or any predicate type URI.

## Verify
```bash
cosign verify-attestation --type cyclonedx \
  --certificate-identity-regexp '^https://github.com/org/app/\.github/workflows/release\.yml@refs/tags/v' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  "$IMG" | jq -r .payload | base64 -d | jq '.predicateType'

cosign verify-attestation --key cosign.pub --type vuln --policy policy.cue "$IMG"
```
`--policy` takes CUE or Rego files and validates the attestation predicate; the default `--type` is `custom`. Shape of a CUE policy (from the Sigstore docs, for the custom predicate type):
```cue
// the predicateType field must match this string
predicateType: "https://cosign.sigstore.dev/attestation/v1"
// the predicate must match these constraints
predicate: {
    Data: "foo\n"
}
```
Rego policies are passed the same way (`--policy policy.rego`) and report violations through an `allow[msg]` rule in `package signature`. Write the constraints for the predicate layout your scanner emits.

## Download without verifying (for tooling)
```bash
cosign download attestation "$IMG" | jq -r .payload | base64 -d | jq .predicateType
```

## Storage and transport
- Cosign stores signatures and attestations using the OCI 1.1 referrers specification; `cosign tree <image>` lists what is attached. Older output shows `sha256-<digest>.att` tags.
- Set `COSIGN_REPOSITORY` to keep signatures and attestations in a different repository from the image.
- `cosign attest --no-upload` prints the attestation to stdout instead of pushing it.

## Gotchas
- Attesting a tag attests whatever digest the tag points to at that moment; use digests.
- Each `cosign attest` adds another attestation to the image; scope verification with `--type`, the identity flags and a `--policy`.
- Payloads are signed as DSSE envelopes; `cosign verify-attestation` prints them with a base64 `payload` field.

## Checked
Documentation release: cosign v3.1.4 CLI reference (sigstore/cosign doc/, checked 2026-10-26) and docs.sigstore.dev sources (sigstore/docs main).
Confirmed: the `--type` values (`slsaprovenance`, `slsaprovenance02`, `slsaprovenance1`, `link`, `spdx`, `spdxjson`, `cyclonedx`, `vuln`, `openvex`, `custom`) and default `custom`; `--policy` accepts CUE or Rego; `--no-upload`; `cosign download attestation`; `trivy --format cosign-vuln`; OCI 1.1 referrer storage and `COSIGN_REPOSITORY`.
Corrected: `slsaprovenance02` added; `--registry-referrers-mode` is not an `attest` or `verify-attestation` flag; the vulnerability CUE example, Kyverno reuse, any-match and Rekor claims were removed as unsupported.
Method: documentation only; no commands were run.
