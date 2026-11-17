---
id: computing-software.devops-ci-cd.argocd-image-updater.test-command-flags
name: test-command-flags
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, test-command, test-flags, dry-check, credentials, rate-limit, registries-conf-path]
level: intro
status: docs-checked
description: "Use argocd-image-updater test IMAGE to see which tag an image would update to, with flags for strategy, constraint, filters and credentials."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/test.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/testing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The test command

`argocd-image-updater test IMAGE [flags]` shows to which tag an image would be updated, before you configure anything. It runs from your workstation, needs no changes to Argo CD or applications and does not install into the cluster. It does not talk to Argo CD and only needs cluster access if you use a pull secret stored in Kubernetes.

Flags:

- `--update-strategy`: `semver` (default), `newest-build`, `alphabetical`, `digest`, `calver`
- `--semver-constraint <constraint>`
- `--calver-layout <layout>` (otherwise read from the image tag, default `YYYY.0M.0D`)
- `--allow-tags <match function>` and `--ignore-tags <glob>` (repeatable)
- `--platforms` (default is your own platform, e.g. `darwin/arm64`)
- `--credentials <definition>` overrides registry config
- `--rate-limit <n>` (default 20; overrides registries.conf)
- `--registries-conf-path <path>` and `--kubeconfig <path>`
- `--loglevel` (default `debug`)

Examples:

```
argocd-image-updater test nginx
argocd-image-updater test nginx --semver-constraint v1.17.x
argocd-image-updater test nginx --allow-tags '^1.19.\d+(\-.*)*$' --update-strategy newest-build
```

Sample result for the first: `Found 923 tags in registry` then `latest image according to constraint is nginx:1.29.1`.

Use `--loglevel info` to cut the noise.

## Checked

2026-11-08. Read in full: docs/install/cmd/test.md and docs/install/testing.md. Confirmed every flag, default and example, the strategy list, and the notes that the command needs no Argo CD changes and only needs cluster access for pull secrets. Removed: the 'quickest check' superlative.

Method: documentation only; no commands were run.
