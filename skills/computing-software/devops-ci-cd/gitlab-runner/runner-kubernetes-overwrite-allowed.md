---
id: computing-software.devops-ci-cd.gitlab-runner.runner-kubernetes-overwrite-allowed
name: runner-kubernetes-overwrite-allowed
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [kubernetes, overwrite, regex, namespace-overwrite, node-selector]
level: advanced
status: docs-checked
description: "Let jobs override Kubernetes settings safely using anchored regexes."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Allow job-level overrides

Jobs can override some pod settings through variables such as `KUBERNETES_NAMESPACE_OVERWRITE` and `KUBERNETES_NODE_SELECTOR_*`. A variable is honoured only when the matching `*_overwrite_allowed` setting in `config.toml` is a Go regular expression that its value matches.

Examples: `namespace_overwrite_allowed` and `node_selector_overwrite_allowed`. When empty, the overwrite feature is disabled.

The regex matches any part of the value unless you anchor it with `^` and `$`. For example `^ci-.*$` allows every namespace starting with `ci-`, and `^(ci-builds|ci-review)$` allows only those two.

To run each job in a namespace of its own instead, use `namespace_per_job`.

## Checked

2026-11-03. Confirmed against regex semantics and the ci- example on the Kubernetes executor page. Removed an unsourced closing tip.

Method: documentation only; no commands were run.
