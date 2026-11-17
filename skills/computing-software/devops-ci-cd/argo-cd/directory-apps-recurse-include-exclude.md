---
id: computing-software.devops-ci-cd.argo-cd.directory-apps-recurse-include-exclude
name: directory-apps-recurse-include-exclude
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, directory-recurse, directory-include, directory-exclude, plain-manifests]
level: intro
status: docs-checked
description: "Deploy plain YAML directories with Argo CD: recurse, include/exclude glob patterns, file ordering and the pitfalls of non-manifest files in the path."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/directory/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory apps: recurse, include, exclude

A source path that Argo CD detects as plain manifest files is a **directory** application
(built-in extensions `.yaml`, `.yml`, `.json` and `.jsonnet`; other files are skipped before `include`/`exclude` are evaluated).

```yaml
spec:
  source:
    repoURL: https://github.com/acme/deploy.git
    path: clusters/prod/addons
    targetRevision: main
    directory:
      recurse: true                     # default false: only top-level files
      include: '{*.yaml,*.yml}'         # glob; braces for several patterns
      exclude: '{tests/*,examples/*,*.values.yaml}'
```

## Rules
- Without `recurse`, subdirectories are ignored (common "why is my resource missing").
- `include` and `exclude` are globs; with both set, the app includes the files that match `include` and do not match `exclude`.
- Every included file must be a manifest: exclude non-manifest YAML such as CI configs or `values.yaml`.
- Files with other extensions (for example `*.yaml.sealed`) are skipped unless you set `directory.disableExtensionFilter: true`, after which `include`/`exclude` are the only filter.
- Order of apply follows sync waves and hooks, not file names.

## When to switch away
Need per-env differences → Kustomize overlays. Need templating → Helm. Plain directories stay
best for generated manifests committed by CI (rendered-manifests pattern).

## Verify
- [ ] `argocd app manifests <app>` lists exactly the resources you expect.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `directory.recurse`, `include`, `exclude` semantics and brace syntax, built-in extension filter and `disableExtensionFilter`, automatic detection of plain-manifest directories. Removed unconfirmed claims (relative path matching, error text, multi-document remark).

Method: documentation only; no commands were run.
