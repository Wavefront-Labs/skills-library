---
id: computing-software.devops-ci-cd.gitea.verify-binary-signature
name: verify-binary-signature
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-cosign-verify, gitea, sigstore, cosign, gpg-verify, release-signature]
level: practitioner
status: docs-checked
description: "Verify a downloaded Gitea binary with cosign verify-blob and its sigstore.json bundle, or with the GPG .asc signature and the release key."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/from-binary.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Verifying a Gitea binary

## Sigstore (from v1.27 per the docs)
Download the binary and its `.sigstore.json` bundle, then with the `cosign` CLI:
```sh
cosign verify-blob gitea-<version>-linux-amd64 \
  --bundle gitea-<version>-linux-amd64.sigstore.json \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  --certificate-identity-regexp="https://github.com/go-gitea/gitea/.github/workflows/release-.*"
```
`Verified OK` means the file is unmodified. The regexp accepts any release workflow; tighten it to a specific workflow and ref, e.g. `https://github.com/go-gitea/gitea/.github/workflows/release-nightly.yml@refs/heads/main` for nightly builds from main only.

## GPG
Each binary also has a detached `.asc` signature:
```sh
gpg --keyserver hkps://keys.openpgp.org --recv 7C9E68152594688862D62AF62D9AE806EC1592E2
gpg --verify gitea-<version>-linux-amd64.asc gitea-<version>-linux-amd64
```
Look for `Good signature from "Teabot <teabot@gitea.io>"`. The warning "This key is not certified with a trusted signature" is expected and does not indicate tampering.

See `gitea-from-binary` for the rest of the install.

## Checked
2026-11-03. Cosign and GPG commands, key fingerprint and expected output confirmed against the Gitea docs page from-binary.md (raw markdown, gitea/docs main branch). Removed the Order of work section: the filename-must-match claim and the chmod/rename ordering are not on the page.
Method: documentation only; no commands were run.
