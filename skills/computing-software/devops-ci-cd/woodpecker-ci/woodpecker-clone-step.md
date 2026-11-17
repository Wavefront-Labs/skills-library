---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-clone-step
name: woodpecker-clone-step
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [clone, submodules, skip-clone]
level: advanced
status: docs-checked
description: "Customize or skip the Woodpecker clone step, including depth and Git submodules."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker clone configuration

Woodpecker adds a default clone step automatically. Override it with a `clone` block:

```yaml
clone:
  - name: git
    image: woodpeckerci/plugin-git
    settings:
      partial: false
      depth: 50
```

Use a custom clone plugin by changing `image`, for example `octocat/custom-git-plugin`.

With the `local` backend the `plugin-git` binary must be in `$PATH` for the default clone step; otherwise write a manual clone step.

Submodules: to reuse the clone credentials, make `.gitmodules` use `https` URLs rather than `git@` ones. If developers need ssh URLs, keep them and add `submodule_override`:

```yaml
clone:
  - name: git
    image: woodpeckerci/plugin-git
    settings:
      recursive: true
      submodule_override:
        my-module: https://github.com/octocat/my-module.git
```

Skip cloning entirely with `skip_clone: true`.

The default clone step runs as root so the workspace directory is `0777` and rootless step containers can write to it. If you skip the clone and use rootless containers, provide a workspace they can access, such as `/tmp`.

Git credentials go only to the default clone step and to trusted clone plugins.

## Checked

2026-11-03. Read the Woodpecker workflow syntax page and confirmed the clone step settings described in the skill. Nothing removed. 

Method: documentation only; no commands were run.
