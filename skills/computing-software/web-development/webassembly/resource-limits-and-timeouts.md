---
id: computing-software.web-development.webassembly.resource-limits-and-timeouts
name: resource-limits-and-timeouts
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, fuel-metering, epoch-interruption, memory-limits, wasm]
level: practitioner
status: docs-checked
description: "Denial of service"
sources: ["https://raw.githubusercontent.com/bytecodealliance/wasmtime/main/docs/examples-interrupting-wasm.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource limits and timeouts

Goal: bound untrusted modules.
- Wasmtime offers two ways to interrupt execution, for example an infinite loop in the guest: deterministic fuel and non-deterministic epochs.
- Fuel is deterministic (same program and fuel are interrupted at the same place) but adds more overhead than epochs. APIs: `Config::consume_fuel`, `Store::set_fuel`, `Store::fuel_async_yield_interval`.
- Epochs are wall-time based, so the interrupt point varies between runs; the page quotes a measured slowdown of around 10%. APIs: `Config::epoch_interruption`, `Store::epoch_deadline_trap`, `Store::epoch_deadline_callback`, `Store::epoch_deadline_async_yield_and_update`.
- On interruption you can raise a trap (not resumable) or async-yield, which hands control back to the host to resume later.
- Test with infinite loops and memory-hungry modules; this page does not cover memory or table growth limits, so read the Wasmtime API docs for those.
Verify: a hostile module is stopped within the limits.

## Checked

2026-11-08. Confirmed in the Wasmtime "Interrupting Wasm Execution" page (read in full).
Removed as unconfirmed: `ResourceLimiter`, instance and stack caps (not on the page).
Method: documentation only; no commands were run.
