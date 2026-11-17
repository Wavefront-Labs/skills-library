---
id: computing-software.web-development.webassembly.emcc-compile-flags
name: emcc-compile-flags
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, emcc-optimization, emcc-exported-functions, modularize, emscripten, emcc, emscripten-fs, wasm]
level: practitioner
status: docs-checked
description: "Compiling C/C++"
sources: ["https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/tools_reference/emcc.rst", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/tools_reference/settings_reference.rst", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/porting/connecting_cpp_and_javascript/Interacting-with-code.rst", "https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/porting/Debugging.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# emcc build flags

Goal: build C/C++ to Wasm.
- `emcc main.c -O2 -o out.js -sEXPORTED_FUNCTIONS=_main,_add -sEXPORTED_RUNTIME_METHODS=ccall,cwrap -sMODULARIZE`.
- `-sALLOW_MEMORY_GROWTH`, `-sINITIAL_MEMORY`, `-sSTACK_SIZE`.
- `-O3`/`-Oz` and `--closure 1` for size; `-g` plus source maps for debugging.
Verify: the built module runs and the exported function returns the expected value.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `EXPORTED_FUNCTIONS`, `EXPORTED_RUNTIME_METHODS`, `MODULARIZE`, `ALLOW_MEMORY_GROWTH`, `INITIAL_MEMORY`, `STACK_SIZE`, `--closure`, `-gsource-map`.
Removed or reworded as unconfirmed: the `node out.js` verification command.
Method: documentation only; no commands were run.
