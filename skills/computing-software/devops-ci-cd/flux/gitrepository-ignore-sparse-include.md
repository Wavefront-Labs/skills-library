---
id: computing-software.devops-ci-cd.flux.gitrepository-ignore-sparse-include
name: gitrepository-ignore-sparse-include
category: computing-software
field: devops-ci-cd
product: flux
tags: [gitrepository, ignore, sourceignore, sparsecheckout, include]
level: sme
status: docs-checked
description: "Shrink and compose GitRepository artifacts with ignore rules, .sourceignore, sparseCheckout, include and submodules."
sources:
  - https://fluxcd.io/flux/components/source/gitrepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Control what ends up in the artifact.

Default exclusions: Git files, image and archive extensions (`.jpg .jpeg .gif .png .wmv .flv .tar.gz .zip`), CI configs (`.github/`, `.circleci/`, `.gitlab-ci.yml` and more), `.goreleaser.yml`, `.sops.yaml` and `.flux.yaml`.

`.spec.ignore` uses `.gitignore` pattern format and overrides the default list. A `.sourceignore` file in the repo also applies, but `.spec.ignore` may overrule it. A common pattern is include-only:

```yaml
spec:
  ignore: |
    # exclude all
    /*
    # include deploy dir
    !/deploy
```

`.spec.sparseCheckout` lists directories to check out; only their contents are in the artifact:

```yaml
spec:
  sparseCheckout:
    - charts
    - kustomize
```

`.spec.include` merges another GitRepository artifact into this one. Compared with submodules, each can use different credentials, changes in the included repo trigger an update, and several GitRepositories can share one included repo, cutting clones.

```yaml
spec:
  include:
    - repository:
        name: other-repository
      fromPath: deploy/kubernetes
      toPath: base/app
```

`toPath` defaults to the repository name. `.spec.recurseSubmodules: true` initialises submodules (default false); deploy keys usually cannot be reused across repositories, so use HTTPS tokens or a bot user SSH key with access to all of them.

## Checked

2026-11-03. Read the GitRepository reference (fluxcd.io/flux/components/source/gitrepositories/): default exclusions, `.spec.ignore` and `.sourceignore` precedence, `sparseCheckout`, `include` benefits and `toPath` default, `recurseSubmodules` default and the deploy-key note. Nothing removed.

Method: documentation only; no commands were run.
