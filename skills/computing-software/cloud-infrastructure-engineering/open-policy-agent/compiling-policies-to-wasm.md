---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.compiling-policies-to-wasm
name: compiling-policies-to-wasm
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [wasm, webassembly, opa-build, entrypoint, abi-version]
level: advanced
status: docs-checked
description: "Compile Rego to a WebAssembly module with opa build -t wasm -e, read the result assignment set, find the ABI version, and handle unsupported built-ins like http.send."
sources:
  - https://www.openpolicyagent.org/docs/wasm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: embed policy evaluation in an application or runtime without a running OPA server.

OPA compiles Rego into an executable Wasm module. This is not the OPA server running in Wasm and not cross-compiled Go; the module is a planned evaluation path for the source policy and query.

Build, with at least one entrypoint given by `-e` or a metadata `entrypoint` annotation:

```
opa build -t wasm -e example/allow example.rego
```

The result is packaged as an OPA bundle.

Output: evaluation yields a set of variable assignments, with the decision bound to a variable named `result`; it can be any JSON value, with at most one assignment. Callers must check whether the assignment set is empty (undefined decision); otherwise read the `"result"` key:

```json
[{"result": <value of data.example.allow>}]
```

Support: the core language is fully supported, but some built-ins are not natively supported and probably will not be, such as `http.send`. Unsupported built-ins can be implemented in the host environment, for example JavaScript.

Using the module: use the npm-opa-wasm SDK for JavaScript; community SDKs exist for other languages. From Go, the `compile` API producing bundles is recommended.

ABI: modules built by OPA 0.27.0 or later export a global `opa_wasm_abi_version` (an i32), plus `opa_wasm_abi_minor_version`. Inspect with `wasm-objdump -x policy.wasm`. ABI 1.1 added the export `memory`, 1.2 added `opa_eval`, and 1.3 added `opa_value_free` and the heap stash functions.

Check: build, load in the SDK, evaluate with sample input, and confirm an empty assignment set for an undefined decision.

## Checked

2026-11-04. Confirmed against the OPA docs WebAssembly page: not the server in Wasm, opa build -t wasm -e with entrypoint flag or metadata annotation, packaged as a bundle, result variable and at-most-one assignment, empty set means undefined, http.send not natively supported, the JavaScript SDK (npm-opa-wasm) and community SDKs, the compile API recommendation for Go, opa_wasm_abi_version and opa_wasm_abi_minor_version (OPA 0.27.0 and later), wasm-objdump -x, and the ABI 1.1/1.2/1.3 notes. Fixed the entrypoint path written in the result example (data.example.allow). Nothing else removed.

Method: documentation only; no commands were run.
