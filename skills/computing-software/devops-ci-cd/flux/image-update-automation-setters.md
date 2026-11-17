---
id: computing-software.devops-ci-cd.flux.image-update-automation-setters
name: image-update-automation-setters
category: computing-software
field: devops-ci-cd
product: flux
tags: [imageupdateautomation, setters, imagepolicy-marker, git-push, commit-author]
level: advanced
status: docs-checked
description: "Let Flux commit image tag updates to Git using setter comments, ImageUpdateAutomation git settings and push branches."
sources:
  - https://fluxcd.io/flux/components/image/imageupdateautomations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ImageUpdateAutomation edits manifests in a Git checkout when an ImagePolicy selects a new image, commits, and pushes.

Mark each line to update with a setter comment naming the policy as `namespace:name`:

```yaml
image: ghcr.io/my-org/my-app:4.0.6 # {"$imagepolicy": "flux-system:my-policy"}
```

For Helm values with separate fields, append `:name`, `:tag` or `:digest`:

```yaml
repository: ghcr.io/my-org/my-app # {"$imagepolicy": "flux-system:my-policy:name"}
tag: 4.0.6 # {"$imagepolicy": "flux-system:my-policy:tag"}
```

The `digest` setter works only if the policy sets `digestReflectionPolicy` to `IfNotPresent` or `Always`.

```yaml
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImageUpdateAutomation
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 30m
  sourceRef:
    kind: GitRepository
    name: flux-system
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: fluxcdbot@users.noreply.github.com
        name: fluxcdbot
      messageTemplate: "Automated image update"
    push:
      branch: main
  update:
    path: ./clusters/my-cluster
    strategy: Setters
```

`git.commit.author.email` is required. The Git credentials need write access. Without `push`, the checkout branch is used. A different `push.branch` is created locally from the checkout branch and force-pushed by default; `push.refspec` supports Gerrit and automatic pull requests in Gitea or Forgejo. `git.commit.signingKey` signs commits with gpg (default) or ssh. `policyChangeDelay` batches close-together updates into one commit.

Only `Setters` is a supported update strategy.

## Checked

2026-11-08: read the image-automation-controller ImageUpdateAutomation spec (docs/spec/v1/imageupdateautomations.md in the fluxcd/image-automation-controller repo, the source of the fluxcd.io page) in part: the example, git checkout, commit, signing key, push branch and refspec, policyChangeDelay, update strategy and setter sections, via search plus targeted reads. Confirmed: the setter comment forms including name, tag and digest, the digestReflectionPolicy requirement, required author email, checkout fallback for push, signingKey gpg or ssh, refspec use with Gerrit and Gitea or Forgejo, policyChangeDelay, and Setters as the only strategy. Removed: the claim that a different push branch is for opening pull requests.

Method: documentation only; no commands were run.
