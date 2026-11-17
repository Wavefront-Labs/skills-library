---
id: computing-software.software-engineering.python.calling-c-libraries-with-ctypes
name: calling-c-libraries-with-ctypes
category: computing-software
field: software-engineering
product: python
tags: [python, py-ffi, ctypes-foreign-functions, ctypes, cdll, argtypes, restype, structure, callbacks, ffi]
level: advanced
status: docs-checked
description: "Call shared libraries with ctypes: load, declare argtypes/restype, structures, pointers and buffers, callbacks, errno and memory ownership, with crash-avoidance checks."
sources: ["https://docs.python.org/3/library/ctypes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling C libraries with ctypes

```python
import ctypes, ctypes.util, sys

libname = ctypes.util.find_library("c") if sys.platform != "win32" else "msvcrt"
libc = ctypes.CDLL(libname, use_errno=True)         # cdecl; WinDLL for stdcall on 32-bit Windows

libc.strlen.argtypes = [ctypes.c_char_p]            # declare both: functions are assumed to return C int unless restype says otherwise
libc.strlen.restype = ctypes.c_size_t
libc.strlen(b"hello")                                # 5   (bytes for char*, not str)

class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]      # layout must match the C struct exactly (alignment, packing: _pack_)

lib = ctypes.CDLL("./libgeom.so")
lib.dist.argtypes = [ctypes.POINTER(Point), ctypes.POINTER(Point)]
lib.dist.restype = ctypes.c_double
a, b = Point(0, 0), Point(3, 4)
lib.dist(ctypes.byref(a), ctypes.byref(b))           # pass by reference without copying

buf = ctypes.create_string_buffer(256)               # mutable char buffer for out-parameters
n = lib.fill(buf, ctypes.sizeof(buf))
buf.value[:n]

CMP = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
cmp = CMP(lambda x, y: x[0] - y[0])                   # keep a Python reference alive while C may call it
arr = (ctypes.c_int * 5)(5, 2, 9, 1, 7)
libc.qsort(arr, len(arr), ctypes.sizeof(ctypes.c_int), cmp)
```

## Memory and errors
- With `restype=c_char_p` the result is a Python `bytes` object; keep the raw address (for example as `c_void_p`) if you must pass it back to the library's free function.
- Use `ctypes.get_errno()` after calls with `use_errno=True`; `ctypes.WinError()` for Windows last errors.

## Gotchas
- Wrong `argtypes`/`restype` give wrong values or crashes; there is no compile-time checking.
- `c_long` is only an alias of `c_int` where `sizeof(long) == sizeof(int)`; use fixed-width types such as `c_int64` when the C side does.
- Struct size mismatch: assert `ctypes.sizeof(Point)` against the size the C compiler reports.
- Keep references to `CFUNCTYPE()` objects for as long as C may call them, or they can be garbage collected and crash the program.
- `CDLL` releases the GIL before calling an exported function and reacquires it afterwards; for different behaviour use `PyDLL`, `WinDLL` or `OleDLL`.

## Verify
- [ ] Test every function with boundary values (0, negative, huge).
- [ ] `ctypes.sizeof` assertions for each Structure.

## Checked

2026-11-08. Confirmed on the ctypes page: `cdll` uses cdecl while `windll` uses stdcall, default return type is C int and `restype` overrides it, `argtypes`, `create_string_buffer`, `byref`, `CFUNCTYPE()` with the keep-a-reference warning, `use_errno=True` with `ctypes.get_errno()`, `WinError()`, `_pack_`, `c_long` aliasing `c_int` only where the sizes match, and the GIL being released around calls with `PyDLL`/`WinDLL`/`OleDLL` as the alternatives. Removed: pointer-truncation claim, `string_at` recipe, NumPy `data_as`, `faulthandler`, swallowed-callback-exception claim, the library-alternatives list and `valgrind` advice (not on the cited page).

Method: docs-only read of cited pages, 2026-11-08
