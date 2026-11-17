---
id: computing-software.devops-ci-cd.skaffold.ko-builder
name: ko-builder
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [ko, go, daemonless, ldflags]
level: practitioner
status: docs-checked
description: "Build Go images without Docker using the embedded ko builder and its fromImage, platforms, flags and ldflags options."
sources:
  - "https://skaffold.dev/docs/builders/builder-types/ko/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `ko` builder embeds ko as a library, so you do not need to install ko or run a Docker daemon. The default configuration suits many Go apps; use an empty map:

```yaml
build:
  artifacts:
  - image: my-simple-go-app
    ko: {}
```

A fuller example:

```yaml
build:
  artifacts:
  - image: my-registry/go-app
    ko:
      fromImage: cgr.dev/chainguard/glibc-dynamic
      platforms: ["linux/amd64", "linux/arm64"]
      env: ["GOPRIVATE=git.internal.example.com"]
      flags: ["-mod=vendor"]
      ldflags: ["-s", "-w"]
      dir: .
      main: ./cmd/app
```

Options and defaults from the page:

- Base image: default `cgr.dev/chainguard/static` (no shell, no `glibc`). Override with `fromImage`.
- `platforms`: default `linux/amd64`. Give a list, or `["all"]` for every platform the base image supports.
- `labels`, `env`, `flags` and `ldflags` support templating from environment variables, for example `"{{.GITHUB_SHA}}"`. Skaffold evaluates these templates, so there is no `.Env` prefix (unlike ko's own templates).
- `dependencies` (what `skaffold dev` watches): `paths` and `ignore`. Default `paths: ["**/*.go"]`, `ignore: []`. `ignore` is used only when `paths` is not empty.
- `dir`: Go source and `go.mod` location relative to `context`. `main`: path or target of `package main`, and `./...` works if only one main package exists. Both default to `.`.

Existing ko users:

- The builder does not read `KO_DOCKER_REPO`; use Skaffold's `default-repo`.
- Manifest placeholders are `ko://` followed by the Go import path of the main package. Skaffold removes the `ko://` prefix before naming the image, and only replaces references in fields named `image`. If you use `ko://` references and push, you must set the default repo.
- Base images are read from `.ko.yaml`, and build config is read from `.ko.yaml` when `skaffold.yaml` sets none of `dir`, `main`, `env`, `flags` or `ldflags`.
- For several binaries, give each its own artifact with its own `main`. (Inference from the options above; the page does not state this.)
- The ko builder does not generate or upload an SBOM, unlike the ko CLI.

Debugging: `skaffold debug` identifies ko images as Go apps by the `KO_DATA_PATH` environment variable and builds with `-gcflags='all=-N -l'`.

File sync works only for static assets bundled with the image (`kodata`). Use `infer` patterns relative to `context`, for example `kodata/**/*`. Sync needs `tar` in the container, which the default base image lacks, so set `fromImage` to one that has it (the page suggests `gcr.io/distroless/base-debian11:debug`), optionally via a profile activated by `command: dev`.

If the builder does not fit, use the `custom` builder with a script that runs ko.

## Checked

2026-11-04. Read the whole Skaffold ko page. Confirmed defaults, templating, dependencies, dir and main, `.ko.yaml` rules, `KO_DOCKER_REPO`, `ko://` handling, debug, file sync and SBOM notes. Removed: the claim that file sync deletes files (not on this page) and the wording that the image name must match an import path. Conflict: the Debugging section says ko "currently only supports local builds", while the Remote builds section says ko supports builds on Google Cloud Build.
Method: documentation only; no commands were run.
