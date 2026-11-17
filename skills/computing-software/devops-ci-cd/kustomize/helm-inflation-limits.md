---
id: computing-software.devops-ci-cd.kustomize.helm-inflation-limits
name: helm-inflation-limits
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [helm, limits, krm-function, security]
level: advanced
status: docs-checked
description: "Know what the helmCharts generator will and will not support so you can decide between it and running helm directly."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/helmcharts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The reference states that kustomize has limited support for Helm chart inflation through the `helmCharts` field. It is intended as a limited subset of Helm features to help with getting started with kustomize, and the project cannot support the entire Helm feature set.

Future enhancements to the current builtin are limited to:

- bug fixes,
- critical security issues,
- additional fields analogous to flags passed to `helm template`, except flags such as a post-renderer that allow arbitrary commands to be executed.

Not planned: private repository or registry authentication, and other large features that increase complexity or have significant security implications.

The next iteration is planned as a KRM function without those restrictions, per the "Helm support long term plan" the page links to. A page revision note says OCI-based Helm repositories are now supported.

Enable the generator with:

```bash
kustomize build --enable-helm
```

Decision rule (judgement, derived from the limits above):

1. Public chart, a few values, then patches: `helmCharts` is a fit.
2. Private chart repositories or custom post-render logic: the generator will not add these, so run `helm template` yourself in CI and patch the output with kustomize.

## Checked

2026-11-08: read the helmCharts reference page in full; confirmed the limited-support statement, the allowed and excluded enhancement lists, the future KRM function and the `--enable-helm` flag. Removed the claims about `skipHooks` and rendering all templates by default, which this page does not state.

Method: documentation only; no commands were run.
