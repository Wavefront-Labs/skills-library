---
id: computing-software.cloud-infrastructure-engineering.kubernetes.container-image-signing-and-verification
name: container-image-signing-and-verification
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cosign, sigstore, sign, signature, keyless, fulcio, rekor, transparency-log, oidc, image-verification, kyverno, gatekeeper, policy-controller, supply-chain, notation, notary, admission-control]
level: advanced
status: docs-checked
description: "Cosign/Sigstore keyless and keyed image signing, the Fulcio/Rekor trust chain, and wiring signature verification into admission so unsigned images can't run."
sources: ["https://docs.sigstore.dev/cosign/signing/signing_with_containers/", "https://docs.sigstore.dev/cosign/verifying/verify/", "https://docs.sigstore.dev/certificate_authority/overview/", "https://docs.sigstore.dev/logging/overview/", "https://docs.sigstore.dev/policy-controller/overview/", "https://kyverno.io/docs/policy-types/cluster-policy/verify-images/sigstore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container image signing — proving an image is what you built, not what got pushed

**Goal:** sign images as part of CI so a signature is cryptographically tied to
the exact build, then make the cluster refuse to run anything unsigned or signed
by the wrong identity. Scanning for known vulnerabilities (a different question —
"is this image safe", not "is this image ours") is in
`computing-software.cloud-infrastructure-engineering.kubernetes.container-image-scanning-and-admission-gates`;
SBOM/provenance attestations are in
`computing-software.cloud-infrastructure-engineering.kubernetes.supply-chain-security-sbom-provenance`.

## 1. Keyed vs. keyless signing
- **Keyed** (`cosign generate-key-pair` → `cosign.key`/`cosign.pub`): classic
  private-key signing. You own key custody, rotation, and the operational burden
  of keeping `cosign.key` secret — a leaked key signs anything as "trusted"
  forever until revoked, and revocation isn't built in the way cert revocation is.
- **Keyless** (Sigstore's actual contribution): no long-lived private key at all.
  CI authenticates to **Fulcio** (a short-lived CA) via OIDC (e.g. GitHub Actions'
  built-in OIDC token), Fulcio issues a certificate valid for 10 minutes binding
  the signature to that OIDC identity (`repo:org/repo:ref:refs/heads/main`), the
  signature is made, and the signing event is logged to **Rekor** (an append-only
  transparency log) before the cert expires. Nothing secret to leak or rotate —
  trust shifts to "did this identity sign it, and is that in the log."
```bash
cosign sign --yes registry.example.com/app@sha256:<digest>          # keyless, from CI with OIDC
cosign verify --certificate-identity-regexp '^https://github.com/org/repo/.*' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  registry.example.com/app@sha256:<digest>
```

## 2. Sign the digest, never the tag
Signatures attach to the image **digest** (`@sha256:...`), stored as a separate
OCI artifact (or in-registry attestation) referencing that digest. Signing/pulling
by tag (`:latest`, `:v1.2.3`) is meaningless for trust — a tag is mutable and can
be repointed after signing. Every admission-time verification and every deploy
manifest should pin by digest; `cosign verify <image>:<tag>` resolves the tag to
whatever digest it currently points to *at verification time*, which can differ
from what was actually tested.

## 3. Wiring verification into admission
Three common paths, same underlying cosign verification logic (Kyverno's `ClusterPolicy` `verifyImages`
form is deprecated as of Kyverno v1.19 and removed in v1.20; use `ImageValidatingPolicy`, stable since v1.18):
- **Kyverno `verifyImages`** (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.kyverno-policy-engine`)
  — simplest if already running Kyverno for other policy.
- **sigstore policy-controller** — a dedicated admission webhook just for
  image verification, using `ClusterImagePolicy` CRDs; lighter weight if you don't
  need general policy.
- **Gatekeeper + external data provider** — possible but more plumbing; most
  teams use Kyverno or policy-controller instead.
All three ultimately call the same cosign verification primitives — the identity
constraints (`certificate-identity`, `certificate-oidc-issuer`) are what actually
enforce *who* signed it, not just *that* it's signed; a policy that checks
"signed" without pinning the identity/issuer accepts a signature from anyone who
can authenticate to Fulcio with any OIDC token, including a different org's CI.

## 4. Mirroring and re-tagging break signatures
- Copying an image to a new registry preserves the
  manifest digest if done correctly, so a cosign signature made against the
  original digest still verifies — but any transform that changes the manifest
  (recompression, re-platform manifest-list edits, some registry "image
  optimization" features) changes the digest and **silently invalidates every
  existing signature**, with no error until something tries to verify at
  admission and fails closed (or fails open, if `failurePolicy: Ignore`).
- Private/air-gapped mirrors of public base images need their own re-signing step
  in the mirroring pipeline if admission requires signatures on everything,
  including vendor/base images.

## 5. Rekor and detecting unauthorized signing
- Rekor is public by default for the public Sigstore instance — anyone can see
  *that* an entry exists and its metadata, which is a feature (transparency: you
  can audit who signed what, when) but means keyless signing of anything you
  don't want publicly logged (proprietary image names/digests in some threat
  models) needs a **private Sigstore instance** (self-hosted Fulcio+Rekor) instead
  of the public one.
- `rekor-cli search --sha sha256:<digest>` / monitoring the log lets you detect if a
  signing identity you don't recognize produced a Rekor entry for an image digest
  you care about — a real tamper-detection signal, not just a compliance checkbox.

## Gotchas
- A `cosign verify` that succeeds only proves the signature chain is valid and
  the identity matches your constraint — it says nothing about CVEs, SBOM
  accuracy, or whether the build itself was tampered with upstream of signing
  (that's provenance/SLSA's job, not signature verification's).
- Keyless signing's short-lived Fulcio cert means you cannot "re-verify" a
  signature's cert validity window years later the way you'd check a long-lived
  cert — verification relies on Rekor's timestamped inclusion proof, not current
  cert validity; use `cosign verify`, don't hand-roll cert date checks.
- Admission-time signature verification calling out to a registry/Rekor on the
  request hot path inherits every caveat in
  `admission-webhooks-validating-and-mutating` §4 (timeout budget) — cache
  verification results or accept the added latency deliberately.

## Verify
- [ ] CI signs the image digest (not tag) immediately after build, before any
      promotion step, using keyless signing tied to the CI identity.
- [ ] Admission policy pins `certificate-identity`/`certificate-oidc-issuer` (or
      equivalent keyed-signer identity) — not just "any valid signature."
- [ ] Deploy manifests reference images by digest.
- [ ] A deliberately unsigned or wrong-identity-signed image is confirmed
      rejected at admission in a non-prod cluster.
- [ ] Mirrored/rebuilt base images have a re-signing step if admission requires
      signatures on everything running in the cluster.

## Checked

Checked 2026-10-27 against the Sigstore docs source (sigstore/docs), the cosign CLI reference, the rekor-cli docs and Kyverno docs source (kyverno/website, main; describes Kyverno v1.19).

- Fulcio issues X.509 certificates valid for 10 minutes from an OIDC identity (Fulcio overview); the public Rekor instance is at rekor.sigstore.dev; `rekor-cli search` takes `--artifact`, `--public-key` or `--sha` (the digest form is `--sha sha256:<digest>`, corrected).
- `cosign sign --yes`, `cosign verify --certificate-identity-regexp --certificate-oidc-issuer` and the requirement that keyless verification set an identity flag confirmed in the cosign reference.
- Kyverno `verifyImages` keyless identity fields, ClusterPolicy deprecation and `ImageValidatingPolicy` stable status confirmed; Sigstore policy-controller `ClusterImagePolicy` confirmed; Gatekeeper external data provider documented in the Gatekeeper docs.
- Removed the unconfirmed claim naming `crane copy` and `skopeo copy`. The prose entries in `sources` were replaced with URLs.

Method: documentation only; no commands were run.
