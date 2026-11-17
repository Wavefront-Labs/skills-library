---
id: computing-software.devops-ci-cd.argocd-image-updater.test-recipes-credentials-and-strategies
name: test-recipes-credentials-and-strategies
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, test-command, credentials, update-strategy, semver-constraint, platforms, troubleshooting]
level: practitioner
status: docs-checked
description: "Test command recipes: semver patch lines, strategy comparison, private registry credentials, and reading log lines to diagnose empty results."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/testing.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/test.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Test command recipes

Latest patch within a minor line:

```shell
argocd-image-updater test nginx --semver-constraint 1.17.X --loglevel info
# latest image according to constraint is nginx:1.17.10
```

Try another strategy on a registry such as GHCR:

```shell
argocd-image-updater test ghcr.io/argoproj/argocd --update-strategy newest-build --loglevel info
```

In the docs sample this found 864 tags and chose `ghcr.io/argoproj/argocd:2.4.0-f8390c94`; its log shows it finishing about 139 seconds in.

Private registry with credentials from the environment (same syntax as the image `pullSecret`):

```shell
export GITHUB_PULLSECRET="<username>:<token>"
argocd-image-updater test docker.pkg.github.com/argoproj/argo-cd/argocd \
  --update-strategy newest-build --credentials env:GITHUB_PULLSECRET
```

Reading the output:

- `Inferred registry from prefix quay.io to use API https://quay.io`: registry inference worked
- `setting rate limit to 20 requests per second`: default limit in effect
- `Found 0 tags in registry` together with `Manifest list did not contain any usable reference. Platforms requested: (darwin/amd64)...` means a platform mismatch; rerun with `--platforms linux/amd64`
- `found 3 from 3 tags eligible for consideration` shows how many tags survived filters
- `no newer version of image found` means nothing qualified

Read the image configuration docs before relying on results.

## Checked

2026-11-08. Read in full: docs/install/testing.md and docs/install/cmd/test.md. Confirmed the log lines quoted and their meanings, the platform mismatch case, the credentials syntax and the semver example. Corrected: the docs sample uses the strategy name latest, which test.md no longer lists, so the example uses newest-build; the claim that metadata fetching causes the slowness was replaced by the observed timing.

Method: documentation only; no commands were run.
