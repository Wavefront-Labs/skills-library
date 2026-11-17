---
id: computing-software.software-engineering.rust.python-and-wasm-bindings-pyo3-wasm-bindgen
name: python-and-wasm-bindings-pyo3-wasm-bindgen
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-python-bindings, pyo3, maturin, wasm-bindgen, wasm-pack, webassembly, ffi, gil, rust-wasm, rust-wasm-bindgen]
level: advanced
status: docs-checked
description: "Expose Rust to Python with PyO3 and maturin (modules, classes, errors, GIL release, abi3 wheels) and to JavaScript with wasm-bindgen and wasm-pack."
sources:
  - https://pyo3.rs/
  - https://www.maturin.rs/
  - https://wasm-bindgen.github.io/wasm-bindgen/
  - https://wasm-bindgen.github.io/wasm-pack/book/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Python and WASM bindings (PyO3 / wasm-bindgen)

**Goal:** ship a Rust core as a Python package or an npm/browser module with idiomatic APIs on the
other side.

## Python with PyO3 + maturin
```bash
pip install maturin
maturin new --bindings pyo3 fastparse && cd fastparse
maturin develop --release        # build and install into the active virtualenv
maturin build --release          # wheels in target/wheels
```
```rust
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

#[pyfunction]
fn parse(py: Python<'_>, data: &[u8]) -> PyResult<Vec<u32>> {
    py.detach(|| core_parse(data))                   // detach from the interpreter for CPU-heavy work
        .map_err(|e| PyValueError::new_err(e.to_string()))
}

#[pyclass]
struct Counter { n: u64 }
#[pymethods]
impl Counter {
    #[new] fn new() -> Self { Counter { n: 0 } }
    fn inc(&mut self) -> u64 { self.n += 1; self.n }
}

#[pymodule]
mod fastparse {
    #[pymodule_export]
    use super::parse;
    #[pymodule_export]
    use super::Counter;
}
```
- The `Bound<'py, T>` API arrived in PyO3 0.21 and the older `&PyAny` GIL-refs API was removed in 0.23, so older tutorials are outdated. The current guide builds modules with `#[pymodule] mod name { #[pymodule_export] use ...; }`.
- Map Rust errors to Python exceptions explicitly (`impl From<MyError> for PyErr`). A Rust panic
  becomes `PanicException`; do not rely on it.
- Detach from the interpreter (`Python::detach`, named `allow_threads` before PyO3 0.26) around long Rust computations so
  other Python threads run. PyO3 has supported free-threaded CPython builds since 0.23.
- **abi3**: `pyo3 = { features = ["abi3-py39"] }` builds one wheel per platform that works on
  Python 3.9+, instead of one per Python version.
- `maturin generate-ci github` generates a GitHub Actions workflow that builds wheels (manylinux and musllinux for Linux); publish to PyPI with `uv publish` as the maturin tutorial recommends.
- Type hints: add a `fastparse.pyi` stub and `py.typed` in the package.
- Convert at the boundary: copying a big Python list into `Vec` costs time; accept `&[u8]`, buffer
  protocol, or numpy arrays (`numpy` crate) for bulk data.

## JavaScript/WASM with wasm-bindgen
```toml
[lib]
crate-type = ["cdylib", "rlib"]
[dependencies]
wasm-bindgen = "0.2"
```
```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn slugify(s: &str) -> String { core_slugify(s) }

#[wasm_bindgen]
pub struct Doc { inner: core::Doc }
#[wasm_bindgen]
impl Doc {
    #[wasm_bindgen(constructor)] pub fn new(text: &str) -> Doc { Doc { inner: core::Doc::parse(text) } }
    pub fn word_count(&self) -> usize { self.inner.words() }
}
```
```bash
cargo install wasm-pack
wasm-pack build --target web        # or bundler (webpack/vite), nodejs
wasm-pack test --headless --firefox
```
- Errors: return `Result<T, E>` where `E: Into<JsValue>` (for example `JsError`) to throw in JS.
- Passing strings/arrays copies across the boundary; batch work per call rather than calling per item.
- `serde-wasm-bindgen` for complex objects; `js-sys` / `web-sys` for JS and DOM APIs;
  `wasm-bindgen-futures` for async/Promise interop.
- JS owns Rust structs via handles: call `.free()`; where weak references are supported wasm-bindgen also uses `FinalizationRegistry` to clean up.
- Size: `lto = true`, `opt-level = "s"` or `"z"` (measure both) and the `wasm-opt` tool.
- The rustwasm organisation's book is archived (August 2025); wasm-bindgen and wasm-pack now live under the `wasm-bindgen` GitHub organisation, and wasm-pack's README names a current maintainer.

## Verify
- [ ] Python: `pip install` the built wheel in a clean venv and run tests (`pytest`).
- [ ] GIL released for long calls (other Python threads progress during a call).
- [ ] WASM: `wasm-pack test` passes; bundle size measured.

## Checked

2026-10-25. Checked against the PyO3 repository (CHANGELOG: Bound API in 0.21, GIL refs removed in 0.23, `allow_threads` renamed to `detach` in 0.26 and absent from current `Python`, Python 3.8 dropped in 0.30; guide: declarative `#[pymodule]` with `#[pymodule_export]`, `abi3-py39` feature, free-threading support since 0.23), the maturin guide (`maturin new -b pyo3`, `develop`/`build --release`, wheels in `target/wheels`, `generate-ci github`, `py.typed` and `.pyi` stubs, `uv publish`), wasm-pack docs (`--target bundler|nodejs|web|no-modules`, `wasm-pack test --headless --firefox`) and the wasm-bindgen guide (`Result` error types, `.free()` and weak references, size optimisation advice). Wrong in the draft and fixed: `py.allow_threads` no longer exists (use `py.detach`); the function-style `#[pymodule]` example replaced by the documented module style; the wasm-pack maintenance note was stale. Removed unconfirmed items (`maturin publish`, wheel platform list, `console_error_panic_hook`, `-Oz`).

Method: documentation only; no commands were run.
