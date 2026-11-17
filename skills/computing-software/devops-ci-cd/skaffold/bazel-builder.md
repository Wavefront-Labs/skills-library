---
id: computing-software.devops-ci-cd.skaffold.bazel-builder
name: bazel-builder
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [bazel, target, tar, docker-load]
level: advanced
status: docs-checked
description: "Build images with Bazel by naming a target that produces a tar archive loadable with docker load."
sources:
  - "https://skaffold.dev/docs/builders/builder-types/bazel/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `bazel` builder runs a Bazel target locally; once Bazel finishes, the image is loaded into the local Docker daemon. It is available with the local build environment only (not in-cluster or Google Cloud Build).

```yaml
build:
  artifacts:
  - image: my-registry/app
    context: .
    bazel:
      target: //:app.tar
      args: ["--compilation_mode=opt"]
```

Options on the `bazel` block:

- `target` is the `bazel build` target to run. It must produce a `.tar` bundle compatible with `docker load`.
- `args` lists additional arguments passed to `bazel build`.
- `platforms` configures the `--platforms` flag for `bazel build` from the Skaffold target platform.

`context` must be a path that contains the Bazel files (`WORKSPACE` and `BUILD`).

Cross-platform: with `platforms` mapping, for example `linux/amd64` to `//platforms:linux-x86_64`, Skaffold passes the matching `--platforms=` value when its target build platform matches, and passes no `--platforms` otherwise. Skaffold does not pick the most specific variant, so `linux/arm64` and `linux/arm64/v8` entries do not work together; list the exact variants you build for.

If the target does not produce a loadable tar, the build fails when the image is loaded. Test the target on its own first: run Bazel manually, then `docker load` the output.

## Checked

2026-11-04. Read the Skaffold Bazel builder page and the `BazelArtifact` definition in the v4beta14 config schema (fields `target`, `args`, `platforms`). Confirmed: tar/`docker load` requirement, local-only support (builder matrix on the Build page), `WORKSPACE`/`BUILD` context, platform passing and the variant caveat. Removed: the claim that `target` is required (neither page says so), the claim that file-watch dependencies are derived from the Bazel target, and the claims about tag-policy handling specific to Bazel. Replaced the example `--platforms` arg with a neutral one.
Method: documentation only; no commands were run.
