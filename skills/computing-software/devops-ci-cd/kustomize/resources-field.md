---
id: computing-software.devops-ci-cd.kustomize.resources-field
name: resources-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [resources, kustomization, files, directories]
level: intro
status: docs-checked
description: "List the files, directories and URLs a kustomization pulls in with the resources field, and the path rules that apply to each entry."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/resource/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Each entry in `resources` must be a path to a file, or a path or URL referring to another kustomization directory.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
# Local files
- myNamespace.yaml
- deployment.yaml
- sub-dir/some-deployment.yaml
# Local directories
- ../../commonbase
# Remote URLs
- https://github.com/kubernetes-sigs/kustomize//examples/multibases/?timeout=120&ref=v3.3.1
```

Rules from the reference page:

- Resources are read and processed in depth-first order.
- Files must contain Kubernetes resources in YAML form; one file may hold several resources separated by the `---` document marker.
- File paths are relative to the directory holding the kustomization file that contains the `resources` field.
- A directory entry can be relative, absolute or part of a URL.
- A URL is an HTTPS or SSH git clone URL with an optional directory and query-string parameters. The older modified hashicorp/go-getter format (for example `github.com/org/repo/path?ref=branch`) is still supported for compatibility but no longer recommended.

Because `resources` is an ordered list, it replaces the deprecated `bases` field: bases and plain files can now be ordered relative to each other.

## Checked

2026-11-03. Confirmed against: the resources reference page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
