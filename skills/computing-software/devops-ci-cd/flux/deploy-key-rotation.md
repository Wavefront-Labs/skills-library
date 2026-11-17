---
id: computing-software.devops-ci-cd.flux.deploy-key-rotation
name: deploy-key-rotation
category: computing-software
field: devops-ci-cd
product: flux
tags: [deploy-key, ssh, bootstrap, secret-rotation, git-credentials]
level: sme
status: docs-checked
description: "Rotate the SSH deploy key Flux uses for Git by deleting the flux-system Secret and recreating it."
sources:
  - https://fluxcd.io/flux/installation/configuration/deploy-key-rotation/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
Rotate the key when a token has expired, the key may be compromised, or you want a different scope such as write access via `flux bootstrap --read-write-key`.

Rerunning `flux bootstrap` does not overwrite the existing `flux-system` Secret, so rotation is manual.

1. Delete the Secret:

```sh
kubectl -n flux-system delete secret flux-system
```

2. Create a new key, either:

```sh
flux create secret git flux-system \
  --url=ssh://git@<host>/<org>/<repository>
```

This prints the SSH public key. Once you register it as the deploy key at your Git provider, Flux resumes all operations.

or rerun `flux bootstrap ...`, which generates a new key pair and prints the public key, or sets it automatically for providers such as GitHub.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/deploy-key-rotation/ (raw source in the fluxcd/website repository).

Removed or corrected: the claim that sync stalls between the two steps, the advice to remove the old public key, and the closing verification commands, none of which is on the page.

Method: documentation only; no commands were run.
