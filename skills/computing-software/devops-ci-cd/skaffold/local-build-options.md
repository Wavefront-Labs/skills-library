---
id: computing-software.devops-ci-cd.skaffold.local-build-options
name: local-build-options
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [local, push, concurrency, trymportmissing, usedockercli]
level: practitioner
status: docs-checked
description: "Tune local builds: whether images are pushed, how many build in parallel, and which Docker client is used."
sources:
  - "https://skaffold.dev/docs/builders/build-environments/local/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Local build is the default execution context: Skaffold uses your locally installed build tools (Docker, Bazel, Maven or Gradle). To configure it explicitly, use `build.local`:

```yaml
build:
  local:
    push: false
    tryImportMissing: false
    useDockerCLI: false
    useBuildkit: true
    concurrency: 1
```

Options (schema `LocalBuild`, marked beta):

- `push`: whether to push images to a registry. If unset, images are pushed only if the current Kubernetes context connects to a remote cluster. With a local cluster Skaffold defaults it to `false` to speed up builds. The command line equivalent is `--push`.
- `concurrency`: how many artifacts build in parallel; default 1, `0` means no limit. Concurrency is off by default because some builders (`custom`, `jib`) may change files on disk and cause side-effects; full parallelism can use a lot of resources. Command line: `--build-concurrency`. Logs still print in sequence.
- `tryImportMissing`: default false. The page says `true` makes Skaffold avoid building an image when the tagged image already exists in the destination, which suits expensive images. The schema describes it as trying to import artifacts from Docker (local or remote registry) when not in the cache. It is off by default to avoid importing a stale image; pair it with a tagging policy computed from content, such as `imageDigest` or `gitCommit` with the `TreeSha` or `AbbrevTreeSha` variants.
- `useDockerCLI`: default false; use the `docker` command-line interface instead of the Docker Engine APIs.
- `useBuildkit`: use BuildKit for Docker builds; if unspecified, uses the Docker default.

## Checked

2026-11-04. Read the whole Skaffold Local build page and the `LocalBuild` definition in the v4beta14 schema. Confirmed options, defaults, flags and the stale-image warning. Removed: the claim that images are loaded into minikube or kind clusters, that local clusters are detected from the context name, the `--default-repo` advice and the `skaffold build --dry-run` tip (none on these pages). Changed the example `useBuildkit` note: it has no schema default. Conflict: the page and the schema describe `tryImportMissing` differently, as noted above.
Method: documentation only; no commands were run.
