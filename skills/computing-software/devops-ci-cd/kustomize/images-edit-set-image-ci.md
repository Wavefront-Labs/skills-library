---
id: computing-software.devops-ci-cd.kustomize.images-edit-set-image-ci
name: images-edit-set-image-ci
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [images, edit, set-image, ci, git-sha]
level: practitioner
status: docs-checked
description: "Use kustomize edit set image in CI to stamp a git SHA or environment variable tag onto an image, then apply and optionally commit the change."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/images/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A common CI/CD pattern tags images with the git commit SHA. With the standalone kustomize tool, `kustomize edit set image` updates the image tags for you after an image has been built and pushed.

Tag from the latest commit SHA, as the reference page shows it:

```bash
kustomize edit set image foo:$(git log -n 1 --pretty=format:"%H")
kubectl apply -f .
```

Tag from an environment variable:

```bash
kustomize edit set image foo:$FOO_IMAGE_TAG
kubectl apply -f .
```

Committing the change: the kustomization.yaml changes may be committed back to git so that they can be audited. When committing image tag updates that a CI/CD system has already pushed, be careful not to trigger new builds and deployments for those changes (for example by skipping CI on that commit).

Notes:

- The page says to download the standalone kustomize tool for this command.
- Run it in a CI workspace or throwaway checkout, since it changes kustomization.yaml.
- Argument syntax beyond the `name:tag` form above is not shown on the page; check the command's help for your version.

## Checked

2026-11-08: read the kustomize images reference page in full. Confirmed the commit-SHA and environment-variable examples, the standalone tool requirement and the committing advice. Corrected the command syntax to the `foo:<tag>` form the page prints and `kubectl apply -f .` (the draft used `foo=foo:` and `apply -k`). Removed the claims about editing the file in place and the images list diff, which the page does not state.

Method: documentation only; no commands were run.
