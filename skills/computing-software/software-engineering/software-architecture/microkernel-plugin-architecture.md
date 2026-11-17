---
id: computing-software.software-engineering.software-architecture.microkernel-plugin-architecture
name: microkernel-plugin-architecture
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-styles, microkernel-architecture, plugin-architecture, extension-points, plugin-registry]
level: practitioner
status: draft
description: "Design a microkernel (plugin) architecture: minimal core, stable extension contracts, plugin discovery and lifecycle, isolation and versioning of the plugin API."
sources: ["https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/", "https://code.visualstudio.com/api/references/extension-manifest", "https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Microkernel / plugin architecture

**Shape:** a small core system (workflow, registry, shared services) plus independently built
plug-ins that add features through defined extension points. Examples: VS Code, Eclipse, browsers,
pytest, Jenkins, insurance claims engines with per-jurisdiction rule plug-ins.

## When it fits
- Product with a stable core and many variant features (per customer, region, file format).
- Third parties must extend it without forking.
- Not for high-scale distributed systems by itself; it's usually a monolith-level style (Richards &
  Ford rate it low on scalability, high on extensibility and simplicity).

## Design steps
1. **Define extension points** as narrow interfaces/contracts: `Exporter { id, mime_types, export(doc, stream) }`.
   Keep the core's domain model out of them; pass DTOs so plug-ins don't couple to internals.
2. **Discovery/registry**: manifest files (VS Code `package.json` `contributes`), entry points
   (`[project.entry-points."myapp.exporters"]` in Python, Java `ServiceLoader` with
   `META-INF/services`), or a config list. Core loads lazily on activation events.
3. **Lifecycle**: load -> validate manifest and API version -> activate -> deactivate/unload. A failing
   plug-in is disabled with a visible error, not a core crash.
4. **Versioning**: the plug-in API is a public API. Semver it, declare compatibility
   (`engines: {"vscode": "^1.90.0"}`), deprecate with overlap.
5. **Isolation**: in-process is fast but a bad plug-in can crash or slow everything; out-of-process
   (VS Code extension host, LSP servers, WASM sandboxes) costs IPC but contains faults and
   permissions.
6. **Inter-plug-in communication** through the core (events, service registry), never direct imports.

## Pitfalls
- Core grows to accommodate one plug-in's special case: push it into a new extension point.
- Extension points that expose mutable core state end up freezing the core's internals.
- No contract tests: ship a plug-in test kit that runs each plug-in against the API.
