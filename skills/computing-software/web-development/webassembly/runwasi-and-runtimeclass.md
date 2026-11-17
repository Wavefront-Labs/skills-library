---
id: computing-software.web-development.webassembly.runwasi-and-runtimeclass
name: runwasi-and-runtimeclass
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, containerd-shim-wasmtime, runtimeclass-wasm, wasm-pods, runwasi, containerd-wasm, wasm-kubernetes, wasm]
level: practitioner
status: docs-checked
description: "Orchestration"
sources: ["https://raw.githubusercontent.com/containerd/runwasi/main/README.md", "https://kubernetes.io/docs/concepts/containers/runtime-class/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runwasi and RuntimeClass

Goal: schedule Wasm workloads.
- runwasi provides the `containerd-shim-wasm` crate for building containerd shims; its README runs a demo with `--runtime=io.containerd.wasmtime.v1` and links Spin shims (spinkube/containerd-shim-spin).
- A Pod selects the runtime through `runtimeClassName` pointing at a RuntimeClass.
Verify: pod runs and reports ready.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `containerd-shim-wasm`, the wasmtime runtime name, Spin shim link, `runtimeClassName`.
Removed or reworded as unconfirmed: claims about OCI artefact layers and unsupported Kubernetes features.
Method: documentation only; no commands were run.
