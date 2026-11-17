---
id: computing-software.web-development.webassembly.spin-and-wasmcloud
name: spin-and-wasmcloud
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, spin-up, wasmcloud-lattice, wadm, wasm]
level: practitioner
status: docs-checked
description: "Application frameworks"
sources: ["https://spinframework.dev/v3/quickstart", "https://spinframework.dev/v3/cli-reference", "https://wasmcloud.com/docs/v1/concepts/", "https://wasmcloud.com/docs/v1/concepts/lattice/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spin and wasmCloud

Goal: build apps on Wasm platforms.
- Spin: `spin new -t http-rust <name>`, `spin build`, `spin up`; `spin deploy` for the cloud.
- wasmCloud: applications are components plus providers, linked through interfaces, running on hosts clustered on a NATS-based lattice.
- Pick on ecosystem fit.
Verify: app serves requests locally and on the platform.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `spin new -t http-rust`, `spin build`, `spin up`, `spin deploy`, wasmCloud components/providers/lattice.
Removed or reworded as unconfirmed: the `spin new http-rust` form (needs `-t`) and the 'actors' wording (current docs say components).
Method: documentation only; no commands were run.
