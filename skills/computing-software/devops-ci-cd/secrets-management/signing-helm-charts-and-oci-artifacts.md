---
id: computing-software.devops-ci-cd.secrets-management.signing-helm-charts-and-oci-artifacts
name: signing-helm-charts-and-oci-artifacts
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, artifact-signing, sign-oci-artifacts, helm-chart-signing, helm-oci, cosign, oras, notation, helm-provenance, helm-package-sign, wasm-artifacts, oci-referrers, flux-verify]
level: advanced
status: gated
description: "Sign Helm charts and other OCI artifacts: push charts to OCI and sign with cosign, legacy helm --sign provenance, ORAS artifacts, Notation, and verifying in Flux/Argo pipelines."
sources: ["https://helm.sh/docs/topics/provenance/", "https://helm.sh/docs/topics/registries/", "https://docs.sigstore.dev/cosign/signing/other_types/", "https://fluxcd.io/flux/components/source/helmcharts/#verification", "https://notaryproject.dev/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing Helm charts and OCI artifacts

## Helm charts in an OCI registry + cosign (recommended)
```bash
helm package ./chart                                   # api-1.4.0.tgz
helm push api-1.4.0.tgz oci://ghcr.io/acme/charts 2>&1 | tee push.log
DIGEST=$(grep -o 'sha256:[a-f0-9]*' push.log | head -1)   # "Digest: sha256:..."
cosign sign --yes "ghcr.io/acme/charts/api@${DIGEST}"     # keyless or --key ...
cosign verify ghcr.io/acme/charts/api@${DIGEST} \
  --certificate-identity-regexp '^https://github.com/acme/charts/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
Run end to end on helm 4.3.1 (and 3.22.1 for the legacy flow) against a local plain-HTTP registry: `helm package`, `helm push ... --plain-http` (prints `Digest: sha256:...`),
`cosign sign --key` and `cosign verify --key` by that digest, and `cosign tree` showing the signature as an OCI referrer all worked. Against a real registry drop `--plain-http`.
Consumers pin by digest: `helm install api oci://ghcr.io/acme/charts/api --version 1.4.0`
resolves a tag; verify before install, or let the GitOps controller verify:
```yaml
# Flux HelmChart verification (field names match the Flux source-controller HelmChart spec; the controller itself was not run: gated: unconfirmed)
spec:
  verify:
    provider: cosign
    matchOIDCIdentity:
      - issuer: "^https://token.actions.githubusercontent.com$"
        subject: "^https://github.com/acme/charts/.github/workflows/release.yml@refs/tags/v.*$"
```
Argo CD has no built-in chart signature verification; verify in the pipeline that
promotes chart versions, or enforce at the image level with admission policies.

## Legacy Helm provenance (.prov, GPG)
```bash
helm package --sign --key 'Release Bot' --keyring secring.gpg ./chart   # legacy keyring file: `gpg --export-secret-keys > secring.gpg`, `gpg --export > pubring.gpg`
helm verify api-1.4.0.tgz --keyring pubring.gpg
helm install --verify --keyring pubring.gpg api ./api-1.4.0.tgz
```
Run on helm 3.22.1 and 4.3.1: `.prov` written, `helm verify` printed `Chart Hash Verified: sha256:...` (`helm install --verify` needs a cluster: gated: unconfirmed). Works with classic HTTP chart repos (`index.yaml` + `.prov`). GPG key management and the
old keyring format make this painful; OCI + cosign supersedes it.

## Other OCI artifacts
Anything pushed with ORAS (WASM modules, policy bundles, SBOM files, Terraform modules)
is signed the same way by digest:
```bash
oras push ghcr.io/acme/policies:v3 bundle.tar.gz:application/vnd.acme.policy.layer.v1+tar
cosign sign --yes ghcr.io/acme/policies@sha256:...
```
Run on ORAS 1.3.5 with a local registry: `oras push` prints `Digest: sha256:...` (also `oras resolve`), the cosign signature and an `oras attach` SBOM both appear under `oras discover` (`application/vnd.dev.sigstore.bundle.v0.3+json` and the custom artifact type).
Attach related artifacts (SBOMs, attestations) with `cosign attest` or
`oras attach --artifact-type ...` so they're discoverable via the OCI referrers API.

## Notation (Notary Project) alternative
(Notation, Azure and Ratify statements: gated: unconfirmed, not run here.)
`notation sign --key <name> <ref>` / `notation verify`, with x509 PKI and trust policies;
common in Azure (ACR + Key Vault plugin) and with Ratify on AKS. Pick one ecosystem per
org; cosign and Notation signatures aren't interchangeable.

## Gotchas
- Signing a tag instead of the digest: the tag can be re-pushed. Always sign the digest
  printed by `helm push`/`oras push`.
- Registry must support OCI artifacts (GHCR, ECR, ACR, GAR, Harbor do); some old
  registries reject chart media types.

## Verify
`cosign tree ghcr.io/acme/charts/api@sha256:...` lists the signature; Flux's HelmChart
reports `SourceVerified` true; changing the chart and re-pushing without signing makes
verification fail.
