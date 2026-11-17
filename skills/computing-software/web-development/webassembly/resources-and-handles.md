---
id: computing-software.web-development.webassembly.resources-and-handles
name: resources-and-handles
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wit-resource, own-borrow, handle-tables, wasm]
level: practitioner
status: docs-checked
description: "Lifecycle"
sources: ["https://raw.githubusercontent.com/WebAssembly/component-model/main/design/mvp/Explainer.md", "https://raw.githubusercontent.com/WebAssembly/WASI/main/docs/Capabilities.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resources and handles

Goal: pass objects safely.
- `own` is a unique, opaque address of a resource that is destroyed when the value is dropped; `borrow` is an opaque address that must be dropped before the current export call returns.
- Both are handle types, lifted and lowered as `i32` indices into a per-component-instance table, like file descriptors; handles avoid copying the resource across component boundaries.
- A `resource` type declares a core representation (`i32` or `i64`) and an optional destructor of type `($T) -> ()`, called when the last handle is dropped. The built-ins include `resource.new`, `resource.drop` and `resource.rep`.
- In WASI, handles are runtime capabilities: first-class and unforgeable, so access to one resource can be passed on without exposing others.
- Test with many iterations and check that live-resource counts return to the baseline.
Verify: resource count returns to zero after the test.

## Checked

2026-11-08. Confirmed in the Component Model Explainer (partial read: the value-type table, handle types section lines 750-770, resource type section lines 884-897, canon built-ins list) and WASI Capabilities.md (read in full).
Removed as unconfirmed: the claim that leaked owned handles leak host objects (not stated in the pages read).
Method: documentation only; no commands were run.
