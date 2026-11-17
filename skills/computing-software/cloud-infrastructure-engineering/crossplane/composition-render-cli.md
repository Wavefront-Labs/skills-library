---
id: computing-software.cloud-infrastructure-engineering.crossplane.composition-render-cli
name: composition-render-cli
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [cli, render, docker, testing, development-runtime]
level: practitioner
status: docs-checked
description: "Preview a Composition locally with crossplane composition render and control how functions run via render annotations."
sources:
  - https://docs.crossplane.io/latest/composition/compositions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Render a Composition without a control plane:

```shell
crossplane composition render xr.yaml composition.yaml functions.yaml
```

It needs Docker Engine to run functions. Output is YAML on stdout: the composite resource first, then the resources the functions created.

`functions.yaml` holds the Function objects. Add the `render.crossplane.io/runtime` annotation to change how each runs:

- `Docker` (default) pulls and runs the function runtime.
- `Development` ignores `spec.package` and connects to a function you started yourself on localhost port 9443, without gRPC transport security. Most SDKs accept `--insecure`, for example `go run . --insecure`.

Other annotations:

- `render.crossplane.io/runtime-docker-cleanup`: `Stop` or `Orphan`.
- `render.crossplane.io/runtime-docker-pull-policy`: `Always`, `Never` or `IfNotPresent`.
- `render.crossplane.io/runtime-development-target`: a gRPC target to connect to.

Render runs `crossplane internal render` from the Crossplane controller image. Pick another version with `--crossplane-version`, an image with `--crossplane-image`, or a local binary with `--crossplane-binary`.

Use the Development runtime to test a function you are writing end to end.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Compositions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: nothing.

Method: documentation only; no commands were run.
