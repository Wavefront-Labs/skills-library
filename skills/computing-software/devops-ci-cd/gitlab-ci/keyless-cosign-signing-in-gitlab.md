---
id: computing-software.devops-ci-cd.gitlab-ci.keyless-cosign-signing-in-gitlab
name: keyless-cosign-signing-in-gitlab
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, sigstore-id-token, cosign, keyless-signing]
level: advanced
status: docs-checked
description: "Sign container images and blobs keylessly from GitLab CI with cosign and the SIGSTORE_ID_TOKEN id_token, then verify with the GitLab certificate identity."
sources: ["https://docs.gitlab.com/ci/yaml/signing_examples/", "https://docs.sigstore.dev/cosign/signing/overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyless cosign signing with SIGSTORE_ID_TOKEN

```yaml
sign-image:
  image: alpine:3.20
  stage: deploy
  id_tokens:
    SIGSTORE_ID_TOKEN:
      aud: sigstore
  before_script:
    - apk add --update cosign
    # authenticate to the registry first (GitLab's example uses docker login with $CI_REGISTRY_USER / $CI_REGISTRY_PASSWORD)
  script:
    - cosign sign --yes "$CI_REGISTRY_IMAGE@$IMAGE_DIGEST"
  rules: [{ if: $CI_COMMIT_TAG }]
```
cosign detects `SIGSTORE_ID_TOKEN` automatically, gets a Fulcio certificate whose SAN is built from the GitLab URL, project path, `//`, the CI config path and the ref, and records the signature in a transparency log.

Always sign by **digest** (from the build job's dotenv artifact, e.g. `IMAGE_DIGEST`), never by tag.

## Verify
```bash
cosign verify "$IMAGE@$DIGEST" \
  --certificate-identity "https://gitlab.com/group/project//.gitlab-ci.yml@refs/tags/v1.2.3" \
  --certificate-oidc-issuer "https://gitlab.com"
```
Note the double slash between project path and config file in the identity.

## Gotchas
- GitLab Self-Managed: see GitLab's page on signing with self-hosted Sigstore infrastructure.
- Blobs: use `cosign sign-blob` and keep the bundle it writes for verification (GitLab's signing examples show the full command).

## Verify
- [ ] `cosign verify` passes with exact identity and fails with another project path.

## Checked

2026-11-02. Confirmed: `id_tokens` with `aud: sigstore` exposed as `SIGSTORE_ID_TOKEN` and picked up by Cosign; `--certificate-identity` is the SAN built from instance URL + project path + `//` + CI config path + `@` + ref; `--certificate-oidc-issuer`; `apk add --update cosign`; sign-blob bundle (GitLab Sigstore signing docs). Removed: cosign login line, the regexp variant, public-Fulcio/Rekor and private-project statements, exact sign-blob flags.

Method: documentation only; no commands were run.
