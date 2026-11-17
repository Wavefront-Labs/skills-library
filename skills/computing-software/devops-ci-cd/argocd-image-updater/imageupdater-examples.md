---
id: computing-software.devops-ci-cd.argocd-image-updater.imageupdater-examples
name: imageupdater-examples
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, examples, imageupdater-cr, git-write-back, digest, semver, pull-request]
level: practitioner
status: docs-checked
description: "Ready ImageUpdater CR patterns: global defaults, application and image overrides, git write-back to helmvalues, digest for mutable tags, semver with 1.x, and GitHub PR write-back."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/examples/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ImageUpdater example patterns

Global defaults:

```yaml
spec:
  commonUpdateSettings:
    updateStrategy: "semver"
    forceUpdate: false
  applicationRefs:
    - namePattern: "my-app-*"
      images:
        - alias: "nginx"
          imageName: "nginx:1.20"
```

Overrides: set `commonUpdateSettings.updateStrategy: "digest"` on `namePattern: "production-*"`, and `"newest-build"` on one image under `staging-*`.

Git write-back to a Helm values file:

```yaml
spec:
  writeBackConfig:
    method: "git"
    gitConfig:
      repository: "git@github.com:myorg/myrepo.git"
      branch: "main"
      writeBackTarget: "helmvalues:./values.yaml"
  applicationRefs:
    - namePattern: "my-app-*"
      images:
        - alias: "nginx"
          imageName: "nginx:1.20"
          manifestTargets:
            helm: {name: "image.repository", tag: "image.tag"}
```

Mutable tags with digest: `updateStrategy: "digest"` globally, `writeBackConfig.method: "argocd"`, `imageName: "registry.com/vendor/api:latest"` for `namePattern: "dev"`, while the Deployment starts at `image: registry.com/vendor/api@sha256:38089...`.

Semver 1.x: `imageName: "registry.com/vendor/api:1.x"` with `updateStrategy: "semver"` for `namePattern: "prod"`; the Deployment runs `registry.com/vendor/api:1.0`.

PR write-back: `method: "git:secret:git-creds"`, `repository: "https://github.com/myorg/myrepo.git"`, `branch: "main"`, `pullRequest: {github: {}}`. The controller pushes `image-updater-<targetKey>-<sha256>` and opens a PR into `main`; an existing open PR is left untouched.

## Checked

2026-11-04. Confirmed each pattern against the examples page (global defaults, overrides, Git write-back, digest, semver 1.x, GitHub pull request write-back).

Method: documentation only; no commands were run.
