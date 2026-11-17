---
id: computing-software.web-development.webassembly.devtools-wasm-debugging
name: devtools-wasm-debugging
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, chrome-wasm-dwarf, source-map-wasm, wasm-breakpoints, wasm-debugging, dwarf-wasm, source-maps, wasm]
level: practitioner
status: docs-checked
description: "Stepping through source"
sources: ["https://raw.githubusercontent.com/emscripten-core/emscripten/main/site/source/docs/porting/Debugging.rst", "https://raw.githubusercontent.com/GoogleChrome/developer.chrome.com/main/site/en/blog/wasm-debugging-2020/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser debugging with DWARF

Goal: debug Wasm in the browser.
- Emscripten: DWARF gives the best debugging experience and is supported in Chrome through a helper extension. Compile and link with `-g` (integer levels such as `-g3` exist); DWARF is only kept after linking if `-g` is also passed at link time.
- Source maps are the lighter alternative: `-gsource-map` is a link-time flag that writes a `.wasm.map`; the linked objects must still carry DWARF.
- DWARF can be large; `-gseparate-dwarf` splits it into a separate file so the shipped binary stays small. Chrome needs the debug file's location (the `SEPARATE_DWARF_URL` setting in the Chrome article) to find it.
- Binaryen optimisation degrades DWARF quality, so debug builds should use low optimisation.
- Chrome: install the C/C++ DevTools Support (DWARF) extension and enable the DevTools experiment "WebAssembly Debugging: Enable DWARF support" (as described in the 2020 article; menu names may have changed since).
Verify: a breakpoint hits in source and locals display.

## Checked

2026-11-08. Confirmed in the Emscripten Debugging page and the Chrome article by search of the relevant passages (line ranges 19-165 of the Emscripten page and the extension and breakpoint passages of the Chrome article), not read end to end.
Removed as unconfirmed: the exact name of the extension in current Chrome (article is from 2020) is flagged as possibly stale rather than asserted.
Method: documentation only; no commands were run.
