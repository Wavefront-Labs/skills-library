---
id: computing-software.devops-ci-cd.flux.bootstrap-git-providers
name: bootstrap-git-providers
category: computing-software
field: devops-ci-cd
product: flux
tags: [bootstrap, flux-bootstrap-github, flux-bootstrap-git, token-auth, ssh]
level: sme
status: docs-checked
description: "Bootstrap Flux onto a cluster against GitHub with a PAT or any Git server over SSH, and what permissions are needed."
sources:
  - https://fluxcd.io/flux/installation/bootstrap/github/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`flux bootstrap` installs the controllers, pushes their manifests to the repository, and configures Flux to update itself from Git. Afterwards all changes, including Flux upgrades, go through Git. You need cluster-admin rights, and must be the owner of the GitHub repository or have admin rights of the GitHub organization.

GitHub personal account:

```sh
export GITHUB_TOKEN=<gh-token>
flux bootstrap github \
  --token-auth \
  --owner=my-github-username \
  --repository=my-repository-name \
  --branch=main \
  --path=clusters/my-cluster \
  --personal
```

For an organization, drop `--personal` and consider a dedicated Flux user; `--team=slug1,slug2` grants maintainer access on a new repository. For GitHub Enterprise add the hostname. A missing repository is created private (`--private=false` for public). The PAT can come from `GITHUB_TOKEN`, a prompt or a pipe. A fine-grained PAT needs Administration read-only, Contents read and write, Metadata read-only (Administration read and write with `--token-auth=false`).

With `--token-auth` the PAT is stored in the cluster as the Secret `flux-system` in `flux-system`; to avoid that, use deploy keys instead.

Any Git server over SSH:

```sh
flux bootstrap git \
  --url=ssh://git@<host>/<org>/<repository> \
  --branch=main \
  --private-key-file=<path/to/private.key> \
  --path=clusters/my-cluster
```

Generate the SSH private key and set the public key as a deploy key on GitHub in advance; add `--password=<key-passphrase>` if the key has one. This route needs no GitHub PAT and suits existing repositories. For GitHub deploy keys via `--token-auth=false`, the key defaults to ECDSA P-384, read-only access, and `--read-write-key=true` is needed for image automation. A GitHub App is the alternative that avoids tying credentials to a user account.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/bootstrap/github/ (raw source in the fluxcd/website repository).

Removed or corrected: the push-rights claim for generic Git, the claim that the generic Git key is stored as the Secret flux-system, and the list of other provider pages, none of which is on this page.

Method: documentation only; no commands were run.
