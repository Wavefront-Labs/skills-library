---
id: computing-software.devops-ci-cd.kustomize.kustomize-localize
name: kustomize-localize
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [localize, remote, offline, alpha]
level: advanced
status: docs-checked
description: "Copy a kustomization root and download every remote URL into it so kustomize build works without network access (alpha command)."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/cmd/localize/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`kustomize localize` is an alpha command. It makes a copy of a kustomization root in which referenced URLs are replaced by local paths to their downloaded content. The goal: `kustomize build` on the copy produces the same output as on the original without a network connection, such as in a CI/CD pipeline that only has internal network access.

Usage:

```bash
kustomize localize [target [newDir]] [--scope scope]
```

- `target`: kustomization root to localize; a local path or remote root. Default: current working directory.
- `newDir`: destination; it must not already exist. The command creates it but not any of its parents. Default: a directory in the current working directory named `localized-{target}` for a local target or `localized-{target}-{ref}` for a remote target.
- `scope`: the bounding directory; the command may copy only files inside it. Default is `{target}`. It cannot be specified for a remote target, whose scope is implicitly the repo.

Structure: downloaded content goes in a `localized-files` directory beside the referencing kustomization. Remote roots are written under `host/path/to/repo/ref/path/in/repo`; single remote files under `host/path`. The alpha version throws an error for absolute paths and requires remote roots to have a `ref` query parameter.

Example from the docs:

```bash
kustomize localize "https://github.com/kubernetes-sigs/kustomize//api/krusty/testdata/localize/remote?submodules=0&ref=kustomize/v5.0.0&timeout=300"
```

This creates `localized-remote-kustomize-v5.0.0` containing the rewritten kustomization.yaml and a `localized-files` tree. Because it is alpha, check the command proposal before relying on it.

## Checked

2026-11-08: confirmed against the kustomize localize reference page, read in full (usage, defaults, structure, example, notes). Added the absolute-path and ref notes from that page.

Method: documentation only; no commands were run.
