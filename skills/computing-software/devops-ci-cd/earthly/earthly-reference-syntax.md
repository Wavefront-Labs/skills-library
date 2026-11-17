---
id: computing-software.devops-ci-cd.earthly.earthly-reference-syntax
name: earthly-reference-syntax
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, target-reference, artifact-reference, function-reference, canonical-form, base-target, import, earthfile]
level: practitioner
status: docs-checked
description: "Earthly reference syntax: target, artifact, image and function refs; local, remote and import Earthfile refs; the implicit base target and how the canonical form is inferred."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/importing.md
  - https://github.com/earthly/earthly/blob/main/docs/guides/target-ref.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly reference syntax

Goal: write and read the `+` references used by `BUILD`, `COPY` and `FROM`.

## Kinds of reference

| Kind | Form | Distinguishing rule |
| --- | --- | --- |
| Target | `<earthfile-ref>+<target>` | lower-case kebab-case name, e.g. `+my-target` |
| Artifact | `<target-ref>/<artifact-path>` | e.g. `+build/some/artifact/deep/in/a/dir` |
| Image | same as target | one image per target; `FROM` takes an image ref, `BUILD` a target ref |
| Function | `<earthfile-ref>+<function>` | ALL_CAPS snake_case, e.g. `+MY_FUNCTION` |

## Earthfile reference forms

- Local, internal: the empty string, e.g. `+build`, `+build/out.bin`, `+COMPILE`.
- Local, external: a path starting with `./`, `../` or `/`, e.g. `./js+build`, `./js+COMPILE`. Prefer relative paths; checkouts differ per user.
- Remote: `<vendor>/<namespace>/<project>/path/in/project[:some-tag]`, e.g. `github.com/earthly/earthly:v0.8.13+earthly` or `github.com/earthly/earthly/buildkitd+build`.
- Import: an alias defined by `IMPORT <full-earthfile-ref> AS <import-alias>`, then `<import-alias>+<target-name>`. Without `AS`, `IMPORT github.com/earthly/earthly/buildkitd` gives `buildkitd` and `IMPORT github.com/earthly/earthly:v0.8.13` gives `earthly`.

```Dockerfile
IMPORT github.com/earthly/earthly/buildkitd

BUILD buildkitd+buildkitd
```

## Implicit base target

Every Earthfile starts with a base recipe whose name is implied: `base`. All other targets implicitly start with `FROM +base`:

```
# base recipe
FROM golang:1.15-alpine3.13
WORKDIR /go-example

build:
    # implicit FROM +base
    RUN echo "Hello World"
```

## Canonical form

A target usually has a canonical form: the remote form with repo and tag inferred, e.g. `github.com/some-user/some-project/some/deep/dir:master+build`. The repo comes from the Git remote `origin`. The tag is chosen by:

1. if HEAD has at least one Git tag, the first tag Git lists;
2. otherwise the current branch, if not in detached HEAD mode;
3. otherwise the current Git hash.

With no Git context detected, the target has no canonical form.

## Checked

2026-11-07. Read docs/guides/importing.md and docs/guides/target-ref.md in full. Reference kinds, forms, base target and canonical-form algorithm match. Corrected: removed DO from the Goal line (the pages name BUILD, COPY and FROM only) and presented the default import alias as the page's two examples.
Method: documentation only; no commands were run.
