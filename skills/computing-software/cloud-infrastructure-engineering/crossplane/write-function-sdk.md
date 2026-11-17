---
id: computing-software.cloud-infrastructure-engineering.crossplane.write-function-sdk
name: write-function-sdk
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function-sdk, go, python, xpkg, testing, development]
level: advanced
status: docs-checked
description: "Create, test and run a custom composition function in Go or Python."
sources:
  - https://docs.crossplane.io/latest/guides/write-a-composition-function-in-go/
  - https://docs.crossplane.io/latest/guides/write-a-composition-function-in-python/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scaffold from a template:

```shell
crossplane xpkg init function-xbuckets function-template-go -d function-xbuckets
crossplane xpkg init function-xbuckets https://github.com/crossplane/function-template-python -d function-xbuckets
```

Tools: Docker Engine, plus Go, or Python 3.11 and Hatch.

Go:

- Edit `input/v1beta1/` and run `go generate ./...` to regenerate input types.
- The handler is `RunFunction(ctx, req *fnv1.RunFunctionRequest)`, which returns `response.To(req, response.DefaultTTL)`.
- Unit test with `go test -v -cover .`.
- Run locally with `go run . --insecure --debug`.

Python:

- The handler is `async def RunFunction(self, req, _)` using the function-sdk-python.
- Unit tests use `unittest`; run `hatch run test:unit`.
- Run locally with `hatch run development`, which disables encryption and authentication.

Test end to end: annotate the Function in `functions.yaml` with `render.crossplane.io/runtime: Development`, start the function locally, then run `crossplane composition render xr.yaml composition.yaml functions.yaml` in another terminal.

Package it by building the runtime image for each platform with `docker build . --platform=linux/amd64` and `--platform=linux/arm64`, then `crossplane xpkg build`.

## Checked

Checked against the Crossplane docs repo copies of the Go and Python function guides, read in full: template init commands, tool list, go generate, RunFunction signatures, response.To, go test, go run --insecure, hatch run test:unit and hatch run development, Development runtime annotation, composition render, docker build platforms, xpkg build.

Method: docs-checked 2026-11-09 against the write-a-composition-function-in-go and write-a-composition-function-in-python guides (docs repo raw markdown).
