---
id: computing-software.devops-ci-cd.kustomize.remote-resource-urls
name: remote-resource-urls
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [remote, git, url, ref, timeout]
level: practitioner
status: docs-checked
description: "Reference a kustomization in a remote git repository from resources using the double-slash repo/path separator and query parameters such as ref and timeout."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/resource/"
  - "https://github.com/kubernetes-sigs/kustomize/blob/master/examples/remoteBuild.md"
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/buildmetadata/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A kustomization can pull a base from a remote git repo by putting a clone URL in `resources`:

```yaml
resources:
- https://github.com/kubernetes-sigs/kustomize//examples/multibases/?timeout=120&ref=v3.3.1
```

Anatomy of that URL:

- HTTPS or SSH git clone URL (`git@github.com:owner/repo` and `ssh://git@github.com/owner/repo` both work), then `//`, then the directory inside the repo that contains a kustomization.yaml. Ports in the URL are not supported.
- Optional query string:
  - `ref`: a `git fetch`-able ref, typically a branch, tag or full commit hash (short hashes are not supported). `version` is an alias that is ignored when `ref` is present.
  - `timeout`: fetch timeout as a number of seconds or a Go duration; the default is `27s`.
  - `submodules`: whether to clone submodules; defaults to `true`.

Kustomize clones the repo to a temporary directory and does a clean checkout of the `ref`. `kustomize build` accepts the same URL as its target. A single remote file can be referenced by its raw GitHub URL.

The legacy hashicorp/go-getter form still works for backward compatibility but is no longer recommended, because kustomize supports different query parameters and go-getter's subdirectory semantics differ:

```yaml
resources:
- github.com/Liujingfang1/mysql?ref=test
```

Practices that follow from the docs:

- Set `ref` to a tag or full commit hash you control. Without `ref`, nothing in the URL says which revision is wanted.
- Remote bases are fetched with a git clone at build time, so the build needs network access to the repo.
- The `buildMetadata: [originAnnotations]` option adds a `config.kubernetes.io/origin` annotation; for resources from a remote base it records the `repo` and `ref`, which helps audit what was pulled.

## Checked

Confirmed against the kustomize `resources` reference, the remoteBuild example and the buildMetadata reference: URL format, `//` separator, `ref`, `version`, `timeout` default and units, `submodules`, SSH forms, clean checkout, raw file URLs, legacy go-getter status, origin annotation fields. Removed: the `kustomize localize` advice (not covered by the pages read) and a copied misspelled legacy example URL, replaced with one from the remoteBuild page.

Method: docs-checked 2026-11-09 against the kustomize resources reference page (raw markdown from kubernetes-sigs/cli-experimental), examples/remoteBuild.md and the buildMetadata reference page (kubernetes-sigs/cli-experimental), read in full.
