---
id: computing-software.devops-ci-cd.helm.chart-versioning-and-kubeversion
name: chart-versioning-and-kubeversion
category: computing-software
field: devops-ci-cd
product: helm
tags: [version, semver, kubeversion, constraints, chart-version, app-version, compatibility]
level: practitioner
status: docs-checked
description: "Chart version rules and the kubeVersion constraint syntax: ranges, tilde, caret, wildcards, hyphen ranges and OR."
sources:
  - "https://helm.sh/docs/topics/charts/"
  - "https://helm.sh/docs/chart_best_practices/conventions/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Every chart needs a `version`. It should follow SemVer 2 but it is not strictly enforced; non-SemVer names are disallowed except `x` or `x.y` forms. A leading `v` or a missing part (such as `v1.2`) is coerced into a valid version (`v1.2.0`). Packages are identified by name plus version, so `version: 1.2.3` in `nginx` gives `nginx-1.2.3.tgz`. Pre-release and build forms such as `1.2.3-alpha.1+ef365` are supported. In Kubernetes labels, the convention is to replace `+` with `_`.

`kubeVersion` is a SemVer range of supported Kubernetes versions. Helm validates it at install and fails on an unsupported cluster.

- Space-separated AND: `>= 1.13.0 < 1.15.0`.
- OR with `||`: `>= 1.13.0 < 1.14.0 || >= 1.14.1 < 1.15.0` (this excludes 1.14.0).
- Operators: `=`, `!=`, `>`, `<`, `>=`, `<=`.
- Hyphen range: `1.1 - 2.3.4` means `>= 1.1 <= 2.3.4`.
- Wildcards `x`, `X`, `*`: `1.2.x` means `>= 1.2.0 < 1.3.0`.
- Tilde: `~1.2.3` means `>= 1.2.3 < 1.3.0`.
- Caret: `^1.2.3` means `>= 1.2.3 < 2.0.0`.

The syntax comes from Masterminds/semver. For rendering tests, `helm template --kube-version` sets `Capabilities.KubeVersion`.

Dependency version constraints use the same syntax. Constraints like `~1.2.3` do not match pre-releases such as `~1.2.3-1`.

## Checked

2026-11-08. Read the Charts topic, General Conventions, helm template and helm lint pages in full. Version coercion, kubeVersion operators and ranges, the + to _ label convention, pre-release behaviour and helm template --kube-version all confirmed. No changes.

Method: documentation only; no commands were run.
