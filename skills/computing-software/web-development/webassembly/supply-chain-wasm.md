---
id: computing-software.web-development.webassembly.supply-chain-wasm
name: supply-chain-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-signing, warg-registry, oci-wasm, wasm]
level: practitioner
status: docs-checked
description: "Provenance"
sources: ["https://raw.githubusercontent.com/bytecodealliance/wasm-pkg-tools/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Supply chain for Wasm modules

Goal: trust Wasm artifacts.
- `wkg` (from wasm-pkg-tools, a Bytecode Alliance project) fetches and publishes Wasm components to OCI registries. Install with `cargo install wkg` or `cargo binstall wkg`, or download a release binary.
- `wkg get <package>@<version>` downloads a package; `wkg publish <component.wasm>` publishes to the configured registry; `wkg config --default-registry <domain>` sets the registry.
- Pin exact artifacts: `wkg oci pull <registry-ref>@sha256:<digest>` pulls by digest, which the README presents as pinning an exact immutable artifact; `wkg fetch` and `wkg update` use `wkg.toml` and `wkg.lock` to pin WIT dependencies.
- Compare the digest of the module you load with the pinned one.
- Scan source dependencies (Cargo, npm), not just the binary. Signing and SBOM tooling is outside the source read here; consult your signing tool's documentation.
Verify: the hash of the loaded module equals the pinned digest.

## Checked

2026-11-08. Confirmed in the wasm-pkg-tools README (read in full).
Removed as unconfirmed: `oras` and cosign usage, SBOM claims and the warg registry claim.
Method: documentation only; no commands were run.
