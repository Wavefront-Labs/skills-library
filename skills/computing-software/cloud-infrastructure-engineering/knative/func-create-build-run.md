---
id: computing-software.cloud-infrastructure-engineering.knative.func-create-build-run
name: func-create-build-run
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [func-create, func-build, func-run, func-invoke, oci-image]
level: intro
status: docs-checked
description: "Scaffold a function with func create, build its OCI image, run it locally and test it with func invoke."
sources:
  - https://knative.dev/docs/functions/creating-functions/
  - https://knative.dev/docs/functions/building-functions/
  - https://knative.dev/docs/functions/running-functions/
  - https://knative.dev/docs/functions/invoking-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: take a function project from scaffold to a locally tested container.

Create: after installing Knative Functions, run `func create -l <language> <function-name>`, for example `func create -l go hello`. The expected output is `Created go function in hello`. The `kn func create` form works the same.

Build: `func build` creates an OCI container image for the function without running or deploying it, which is useful when you want an image but no cluster deployment. It uses the project name and the image registry name to build the fully qualified image name. If the project was never built, you are prompted for an image registry. You can set the registry with the `FUNC_REGISTRY` environment variable instead. A Docker daemon is needed for local builds.

Run: `func run [--registry <registry>]`, from inside the project directory, builds the image if required and runs it locally rather than on a cluster.
- `func run --build` forces a rebuild.
- `func run --build=false` disables building.

Invoke: `func invoke` sends a test request to check the function can receive HTTP requests and CloudEvents. If the function runs locally, the request goes to the local instance. The `--data` flag supplies test data, and other options simulate different request types.

Private registries: set `FUNC_USERNAME` and `FUNC_PASSWORD`. They work with the `host`, `s2i` and `pack` builders, and are safer than the `--password` flag, whose value other users can see via `ps`.

## Checked

2026-11-04. Confirmed against the Creating, Building, Running and Invoking functions pages and the snippets they include (knative/docs source): `func create -l <language> <function-name>` and the `Created go function in hello` output, `kn func` equivalents, `func build` producing an OCI image without running or deploying, the registry prompt and `FUNC_REGISTRY`, the Docker daemon prerequisite for local builds, `func run [--registry <registry>]` with `--build` and `--build=false`, `func invoke` with `--data`, and the `FUNC_USERNAME` and `FUNC_PASSWORD` note for the `host`, `s2i` and `pack` builders. Added the three extra pages to sources. Nothing removed.

Method: documentation only; no commands were run.
