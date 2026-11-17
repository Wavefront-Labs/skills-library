---
id: computing-software.web-development.webassembly.emscripten-virtual-fs-and-ports
name: emscripten-virtual-fs-and-ports
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, emscripten-preload-file, embind, emscripten-ports, wasm]
level: practitioner
status: docs-checked
description: "Runtime features"
sources: ["https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/porting/files/packaging_files.rst", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/api_reference/Filesystem-API.rst", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/porting/connecting_cpp_and_javascript/embind.rst", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/tools_reference/emcc.rst", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/tools/ports/sdl2.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual filesystem, ports and embind

Goal: handle files and C++ bindings.
- `--preload-file assets`, `--embed-file`, MEMFS/IDBFS/NODEFS mounts, `FS.syncfs` for persistence.
- Embind: an `EMSCRIPTEN_BINDINGS(my_module) { function("lerp", &lerp); }` block, linked with `--bind` (or `-lembind`).
- Ports are enabled with settings such as `-sUSE_SDL=2`.
Verify: file reads and bound functions work in the browser.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `--preload-file`, `--embed-file`, MEMFS/IDBFS/NODEFS, `FS.syncfs`, `EMSCRIPTEN_BINDINGS`, `--bind`, `-sUSE_SDL=2`.
Removed or reworded as unconfirmed: the 'confirm current port names' hedge.
Method: documentation only; no commands were run.
