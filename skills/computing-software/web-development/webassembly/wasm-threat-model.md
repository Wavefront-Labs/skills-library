---
id: computing-software.web-development.webassembly.wasm-threat-model
name: wasm-threat-model
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-memory-safety, control-flow-integrity, wasm-capabilities, wasm-security, wasm-sandbox-escape, spectre-wasm, wasm]
level: practitioner
status: docs-checked
description: "Defensive view"
sources: ["https://raw.githubusercontent.com/WebAssembly/design/main/Security.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threat model and hardening

Goal: understand what the sandbox does and does not do.
- Each module runs sandboxed from the host runtime; it cannot escape except through the APIs it is given. In a browser it is also subject to the same-origin policy.
- Control-flow integrity is implicit: calls use declared function indices, indirect calls check the type signature at runtime, and the call stack is protected from buffer overflows in the module heap. Direct code injection and conventional ROP gadgets are not possible.
- Not prevented: overflows inside linear memory can overwrite adjacent objects (bounds checks are per memory region), code-reuse attacks against indirect calls at function granularity, TOCTOU races, and side channels such as timing attacks.
- Stack-smashing protection and data execution prevention are described as not needed by Wasm programs; fine-grained CFI is available with `-fsanitize=cfi` in Emscripten at a small cost per indirect call.
- Traps (for example out-of-bounds access, bad indirect call signature, division by zero) end execution; in a browser a trap surfaces as a JavaScript exception.
- Keep the host-import surface small, since imports are the only way out of the sandbox.
Verify: host-import surface reviewed and minimised.

## Checked

2026-11-08. Confirmed in the WebAssembly design Security.md (read in full): every bullet above.
Removed as unconfirmed: the Spectre mitigation list (site isolation, cross-origin isolation), which the page does not discuss, and the advice to compile with stack protectors.
Method: documentation only; no commands were run.
