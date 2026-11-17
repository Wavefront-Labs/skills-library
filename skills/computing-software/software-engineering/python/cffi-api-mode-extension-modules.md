---
id: computing-software.software-engineering.python.cffi-api-mode-extension-modules
name: cffi-api-mode-extension-modules
category: computing-software
field: software-engineering
product: python
tags: [python, py-ffi, py-ffi-cffi, cffi-extension-api, cffi, api-mode, abi-mode, ffibuilder, native-bindings]
level: advanced
status: draft
description: "Bind C libraries with cffi in API mode (compiled, checked against headers) versus ABI mode, build with set_source, manage memory and callbacks, and package it."
sources: ["https://cffi.readthedocs.io/en/stable/overview.html", "https://cffi.readthedocs.io/en/stable/cdef.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cffi: API mode extension modules

cffi offers two modes. **ABI mode** (`ffi.dlopen`) loads a shared library at run time and trusts your declarations (like ctypes; fragile). **API mode** (`set_source`) compiles a small C extension against the real header, so the compiler checks types and macros: prefer it.

```python
# build_example.py
from cffi import FFI
ffibuilder = FFI()
ffibuilder.cdef("""
    typedef struct { double x, y; } point_t;
    double point_dist(const point_t *a, const point_t *b);
    int    read_into(char *buf, size_t n);
""")
ffibuilder.set_source("_example",                # module name
    '#include "example.h"',                      # real C source/prelude, compiled with your compiler
    libraries=["example"], include_dirs=["include"], library_dirs=["lib"])
if __name__ == "__main__":
    ffibuilder.compile(verbose=True)             # produces _example.<abi>.so / .pyd
```
```python
from _example import ffi, lib
a = ffi.new("point_t *", {"x": 0, "y": 0})       # owned memory freed when the Python object dies
b = ffi.new("point_t *", [3, 4])
lib.point_dist(a, b)
buf = ffi.new("char[]", 256)
n = lib.read_into(buf, 256)
ffi.string(buf, n); ffi.buffer(buf, n)[:]        # bytes copy
ffi.from_buffer(bytearray(16))                   # zero-copy view of a Python buffer (keep the object alive)

@ffi.callback("int(int, int)")                   # or "extern Python" with ffi.def_extern for stable callbacks
def cmp(a, b): return a - b
```

## Packaging
In `pyproject.toml`/`setup.py` use `cffi_modules=["build_example.py:ffibuilder"]` (setuptools) with `cffi` in build requirements, so wheels contain the compiled module; build wheels per platform with cibuildwheel.

## Gotchas
- `cdef` accepts only a C-like subset (no `#include`, no macros except `#define X ...` constants with `...`); use `...;` placeholders for partially known structs and let the compiler fill sizes.
- `ffi.new` memory is owned by the returned cdata object; keep it alive for as long as C holds the pointer (`ffi.gc` for custom destructors).
- Callbacks created with `ffi.callback` are fragile on some security-hardened systems (writable-executable memory); prefer `def_extern`.
- Thread safety: cffi releases the GIL around calls; callbacks reacquire it.
- Compare with ctypes (no compile step), Cython, pybind11/nanobind (C++), PyO3 (Rust).

## Verify
- [ ] Import the built module in a clean venv from the wheel and call every function with edge values.
- [ ] Mismatched declaration (wrong arg type) fails at compile time in API mode.
