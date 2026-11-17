---
id: computing-software.software-engineering.zig.wasm-freestanding
name: wasm-freestanding
category: computing-software
field: software-engineering
product: zig
tags: [zig, wasm-freestanding, zig-embedded-wasm, wasm32-freestanding, wasi, wasm-export, rdynamic, wasm-allocator]
level: advanced
status: docs-checked
description: "Build Zig for WebAssembly with wasm32-freestanding or wasi, export functions to JS, set the entry point and allocate memory."
sources:
  - https://ziglang.org/documentation/0.15.1/#WebAssembly
  - https://github.com/ziglang/zig/blob/0.15.1/src/main.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Step/Compile.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiling to WebAssembly (wasm32-freestanding)
**Goal:** run Zig in the browser or WASI runtimes.

```zig
// math.zig (from the language reference)
extern fn print(i32) void;

export fn add(a: i32, b: i32) void {
    print(a + b);
}
```
```bash
zig build-exe math.zig -target wasm32-freestanding -fno-entry --export=add
```
```js
WebAssembly.instantiate(typedArray, { env: { print: (result) => { console.log(`The result is ${result}`); } } })
  .then(result => { result.instance.exports.add(1, 2); });
```
- The reference says Zig supports WebAssembly out of the box; for browsers and nodejs build an executable for the freestanding OS target. The reference example prints `The result is 3`.
- CLI flags for wasm: `-fno-entry` (no entry point), `-rdynamic` (all symbols in the dynamic table), `--export=[value]` (force a symbol to be exported), `--import-memory`, `--export-memory`, `--import-symbols`, `--import-table`, `--export-table`, `--initial-memory=[bytes]`, `--max-memory=[bytes]`, `--shared-memory`, `--global-base=[addr]`, and `-mexec-model=[value]` for WASI.
- In `build.zig`, `Step.Compile` has `entry: Entry` (`.disabled` for no entry point) and `rdynamic: bool`.
- WASI support is "under active development"; the reference runs a WASI build with `wasmtime wasi_args.wasm 123 hello`, using `std.process` arguments and `std.fs.wasi.Preopens` for preopened directories.
- `std.heap.wasm_allocator` is a WebAssembly-specific allocator ("fast, small"); on wasm targets `std.heap.page_allocator` is backed by the same WasmAllocator.

## Self-check
Call `add` from Node as in the example and see `The result is 3`.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (WebAssembly, Freestanding, WASI), its `math.zig` test directives (`-fno-entry`, `--export=add`), `src/main.zig` help text, `lib/std/heap.zig` and `lib/std/Build/Step/Compile.zig`.
Removed: `-O ReleaseSmall` guidance as a requirement, the `alloc` export example, "no std.fs/stdout on freestanding", custom panic handler advice, wasm-objdump/wasm-opt advice, "-fno-entry older flags" hedge.
Method: documentation only; no commands were run.
