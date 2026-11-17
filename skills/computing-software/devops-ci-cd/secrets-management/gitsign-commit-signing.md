---
id: computing-software.devops-ci-cd.secrets-management.gitsign-commit-signing
name: gitsign-commit-signing
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, gitsign, commit-signing, keyless-signing, sigstore, x509-signing, git-config-gpg-format, verified-commits, signed-tags, source-integrity, slsa-source]
level: advanced
status: gated
description: "Sign git commits and tags keylessly with Sigstore gitsign: git config, OIDC login and credential cache, verifying with gitsign verify, and its limits on GitHub's Verified badge."
sources: ["https://docs.sigstore.dev/cosign/signing/gitsign/", "https://github.com/sigstore/gitsign", "https://github.com/sigstore/gitsign/blob/main/docs/committer-verification.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gitsign commit signing

gitsign signs commits with short-lived Fulcio certificates tied to your OIDC identity
(Google/GitHub/Microsoft login) and logs them in Rekor. No GPG/SSH key to manage.

## Setup (per repo, or `--global`)
```bash
brew install sigstore/tap/gitsign        # or go install github.com/sigstore/gitsign@latest
git config --local commit.gpgsign true
git config --local tag.gpgsign true
git config --local gpg.x509.program gitsign
git config --local gpg.format x509
# optional: pin the identity provider and skip the browser chooser
git config --local gitsign.connectorID https://github.com/login/oauth
```
Each commit opens a browser for OIDC login. Avoid repeated logins with a credential cache (README FAQ): the
built-in OS-keyring cache `git config --global gitsign.credentialCacheMode system` (no daemon), or the
`gitsign-credential-cache` daemon with `GITSIGN_CREDENTIAL_CACHE=<socket path>` (`credentialCacheMode socket`); the cert
is reused for its ~10-minute lifetime on the public instance. `connectorID` valid values: `https://github.com/login/oauth`,
`https://accounts.google.com`, `https://login.microsoftonline.com`. (Signing itself needs a browser OIDC login: gated: unconfirmed, not run here.)

## In CI (bot commits)
GitHub Actions with `id-token: write`: gitsign uses the ambient OIDC token, so release
bots can sign version-bump commits/tags identifying the workflow.

## Verify
```bash
git verify-commit HEAD                # integrity + Rekor entry only; prints "Validated Certificate claims: false" and a warning
gitsign verify --certificate-identity=alice@example.com \
  --certificate-oidc-issuer=https://github.com/login/oauth HEAD
git log --show-signature -1
```
The gitsign README says `gitsign verify` is preferred: git's own verify commands pass no expected identity, so they prove integrity and that the
entry exists on Rekor, not who signed.
Like cosign, verification must pin identity and issuer; "has a valid Sigstore
signature" alone proves nothing about *who*.

## Limits
- GitHub/GitLab don't show *Verified* for gitsign signatures, because the Sigstore CA
  isn't in their trust store; commits show *Unverified*. Enforce in CI instead: a job
  running `gitsign verify` with identity flags (not `git verify-commit`, which does not check claims) on each commit of the PR with an
  allow-list of identities. Branch-protection "require signed commits" won't accept them.
- Email in the certificate must match the commit author email for most policies; set
  `user.email` to your IdP email.
- Rekor entries are public: your email and repo commit SHAs become visible. For private
  orgs consider a private Sigstore instance or SSH signing.
- Rebases/squash-merges done by the forge create new commits signed by the forge, not you.

## Verify it works
`git log --show-signature -1` prints `Good signature from [alice@example.com]` and a
`Validated Git signature: true` / `Validated Rekor entry: true` line.
