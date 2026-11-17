---
id: computing-software.web-development.webassembly.emscripten-side-modules
name: emscripten-side-modules
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, emscripten-dynamic-linking, main-module, side-module, wasm]
level: practitioner
status: docs-checked
description: "Runtime plugins"
sources: ["https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/compiling/Dynamic-Linking.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAIN_MODULE and SIDE_MODULE

Goal: load code at runtime.
- `-sMAIN_MODULE=2` and `-sSIDE_MODULE=1`; `dlopen` loads side modules from the virtual FS.
- Dynamic linking can add overhead; static linking should be preferred for best performance.
- Prefer static linking unless plugins are needed.
Verify: a side module function is callable after dlopen.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `MAIN_MODULE=2`, `SIDE_MODULE=1`, `dlopen` and the overhead note.
Removed or reworded as unconfirmed: the 'larger' claim.
Method: documentation only; no commands were run.
