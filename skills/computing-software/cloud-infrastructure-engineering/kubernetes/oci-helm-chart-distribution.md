---
id: computing-software.cloud-infrastructure-engineering.kubernetes.oci-helm-chart-distribution
name: oci-helm-chart-distribution
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm, oci, oci-registry, helm-push, helm-pull, chart-distribution, cosign, sigstore, artifact-signing, digest-pinning, ecr, ghcr, acr, harbor, promotion, provenance]
level: practitioner
status: docs-checked
description: "Distribute Helm charts as OCI artifacts: registry push/pull/login, cosign signing and verification, and promoting a chart across environments by digest."
sources: ["https://helm.sh/docs/topics/registries/", "https://helm.sh/docs/topics/provenance/", "https://github.com/sigstore/cosign/blob/main/doc/cosign_verify.md", "https://github.com/sigstore/cosign/blob/main/doc/cosign_sign.md", "https://github.com/opencontainers/distribution-spec/blob/main/spec.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCI distribution for Helm charts — registries, signing, digest promotion

**Goal:** charts live next to the container images they deploy, in the same registry,
with the same auth and the same signature verification — not a separate `index.yaml`
HTTP chart repo with its own access model.

## 1. Push and pull
```bash
helm registry login ghcr.io -u <user> --password-stdin <<< "$TOKEN"
helm package ./mychart                       # -> mychart-1.4.0.tgz
helm push mychart-1.4.0.tgz oci://ghcr.io/org/charts
helm pull oci://ghcr.io/org/charts/mychart --version 1.4.0
helm install rel oci://ghcr.io/org/charts/mychart --version 1.4.0
```
OCI chart refs need no `helm repo add`: reference `oci://host/path/chart` directly, with
`--version` or an `@sha256:` digest. For `helm push`, the reference is the registry path
without the chart name or tag (both are inferred from the chart's name and version). Use
`helm show chart oci://...` or the registry's own UI/API to look at what is published.

## 2. Auth
- `helm registry login` takes only the registry host (optionally with port): no scheme, no path.
  The credentials file location is set with `$HELM_REGISTRY_CONFIG`.
- Some registries require the repository and/or namespace to be created before the first
  `helm push`; otherwise the push errors. Follow your registry's own OCI documentation (Helm's
  docs link ECR, ACR, Docker Hub, Google Artifact Registry, Harbor and others).
- Prefer short-lived credentials in CI over a long-lived registry password, same rationale as
  `computing-software.devops-ci-cd.secrets-management.secrets-and-supply-chain-hygiene`.

## 3. Signing and provenance
```bash
helm push mychart-1.4.0.tgz oci://ghcr.io/org/charts
cosign sign ghcr.io/org/charts/mychart:1.4.0          # keyless (Sigstore Fulcio+Rekor) or --key
cosign verify ghcr.io/org/charts/mychart:1.4.0 --certificate-identity-regexp '...' --certificate-oidc-issuer '...'
```
- `cosign verify` in a keyless flow requires `--certificate-identity` or
  `--certificate-identity-regexp`, plus the OIDC issuer flag.
- Helm's own docs describe a different path for OCI charts: the `helm-sigstore` plugin publishes
  provenance to a transparency log (`helm sigstore upload`). Which signing flow you use is your
  choice; confirm what your deploy path actually verifies, because a successful `cosign verify`
  by hand does not mean your cluster enforces anything.
- Classic provenance (`helm package --sign`, a `.prov` file) also works with OCI: a `.prov` next to
  the `.tgz` is uploaded by `helm push` as an extra manifest layer.

## 4. Promotion by digest, not by re-pushing
Promote dev → staging → prod by **referencing the same immutable digest** everywhere,
never by rebuilding or re-tagging the chart per environment:
```bash
# helm push prints the digest ("Digest: sha256:..."); record it, then pin staging and prod
# to it, for example: helm install rel oci://ghcr.io/org/charts/mychart@sha256:<digest>
```
This guarantees staging and prod install byte-identical chart content; a floating
tag (`:1.4` or `:latest`) can mutate underneath a later promotion if someone re-pushes.
See `computing-software.cloud-infrastructure-engineering.kubernetes.environment-promotion-in-gitops`
for the full dev→staging→prod workflow this slots into.

## Gotchas
- `helm push` embeds the chart name from `Chart.yaml`, not the tgz filename — pushing
  a renamed `.tgz` doesn't rename the chart in the registry, a frequent source of
  "I pushed X but see Y" confusion.
- An OCI chart can be a dependency in another chart's `Chart.yaml`: `repository` is the
  registry reference without the chart name (`oci://host/path`), fetched by
  `helm dependency update`.

## Verify
- [ ] `helm pull oci://.../mychart --version X` reproduces the digest that `helm push` printed in CI.
- [ ] Whichever signature check you chose succeeds against the pushed chart with the expected identity.
- [ ] The staging and prod deploy manifests reference the chart by the same digest,
      not independently re-resolved tags.
- [ ] CI registry auth uses short-lived credentials, not a static long-lived token committed anywhere.

## Checked

2026-10-25, against Helm registries and provenance docs, cosign `cosign_verify` and `cosign_sign` references (main), Helm `helm push` reference. Confirmed: push reference without chart name or tag, digest install, dependency `repository` form, certain registries needing pre-created repositories, `--certificate-identity`/`--certificate-identity-regexp` for keyless verify, `helm-sigstore` plugin, `.prov` upload on push. Removed as unconfirmed: the claim that `helm search repo` does not work on OCI, ECR login and repository details, the Kyverno and Harbor/Artifactory remarks, the claim that cosign supersedes provenance, name-length rules, and the crane digest commands.

Method: documentation only; no commands were run.
