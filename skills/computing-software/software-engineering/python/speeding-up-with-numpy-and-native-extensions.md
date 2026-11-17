---
id: computing-software.software-engineering.python.speeding-up-with-numpy-and-native-extensions
name: speeding-up-with-numpy-and-native-extensions
category: computing-software
field: software-engineering
product: python
tags: [python, python-performance, numpy-vectorization, cython, native-extensions, numba, pyo3, optimization]
level: practitioner
status: gated
description: "Make hot Python loops fast: vectorise with NumPy, JIT with Numba, compile with Cython or Rust/PyO3, and measure which option is worth its build cost."
sources:
  - https://numpy.org/doc/stable/user/basics.broadcasting.html
  - https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html
  - https://numba.readthedocs.io/en/stable/user/5minguide.html
  - https://pyo3.rs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Speeding up Python with NumPy vectorisation and native extensions

**Goal:** 10-100x speedups on numeric or tight-loop code, after profiling proves the loop is the bottleneck.

## 0. Before anything
Profile (`py-spy`, `cProfile`) and confirm the time is in Python bytecode, not I/O or a database. Try algorithmic fixes (a set instead of a list scan, caching) first.

## 1. NumPy vectorisation
```python
# loop: ~0.75 s for 10M elements (measured, Python 3.14, lists)
total = 0.0
for p, q in zip(prices, qty):
    if q > 0: total += p * q
# vectorised: ~90 ms (measured, same data; the mask and temporary arrays cost memory bandwidth)
prices, qty = np.asarray(prices), np.asarray(qty)
total = float((prices * qty)[qty > 0].sum())
```
Techniques: boolean masks instead of `if`, broadcasting (`a[:, None] - b[None, :]` for pairwise), `np.where`, `np.cumsum`, `np.searchsorted`, `np.add.at` for scatter-add, `np.einsum`.
- Avoid `np.vectorize` (a Python loop in disguise) and building arrays element by element.
- Watch memory: broadcasting a 100k x 100k pairwise matrix is 80 GB; chunk it.
- Specify dtypes (`float32`, `int64`) and use in-place ops (`out=`) for large arrays.

## 2. Numba: JIT for loops NumPy cannot express
```python
from numba import njit
@njit(cache=True)
def running_max_drawdown(x):
    peak, worst = x[0], 0.0
    for v in x:
        peak = max(peak, v); worst = min(worst, v / peak - 1)
    return worst
```
Works on NumPy arrays and scalars in nopython mode; first call compiles. `parallel=True` + `prange` for multi-core.

## 3. Cython: compiled Python with C types (gated: unconfirmed, source is paywalled or blocked)
```cython
# fast.pyx
def dot(double[:] a, double[:] b):
    cdef Py_ssize_t i
    cdef double s = 0
    for i in range(a.shape[0]):
        s += a[i] * b[i]
    return s
```
Build via `setuptools` + `cythonize` or meson-python; `cython -a fast.pyx` produces an HTML report where yellow lines still call into Python.

## 4. Rust with PyO3 / maturin
For larger native components (parsers, algorithms with complex data structures), `maturin new --bindings pyo3`, write `#[pyfunction]`s, release the GIL with `py.detach` for parallelism (named `allow_threads` before PyO3 0.26; check the PyO3 changelog for your version) (gated: unconfirmed, source is paywalled or blocked). The Rust and Cython snippets were not built here because no C compiler or Rust toolchain was available, ship wheels with `maturin build --release` / cibuildwheel.

## Choosing
| Option | Best for | Cost |
|---|---|---|
| NumPy | array math | none, a rewrite of the loop |
| Numba | numeric loops, quick wins | heavy dependency, numeric types only |
| Cython | gradual typing of existing code, C libs | build step, C compiler per platform |
| PyO3/C++ (nanobind) | big native modules | separate language, wheel builds |

## Gotchas
- Calling a native function per element from Python loses most gains; move the whole loop across the boundary.
- Platform wheels: compiled extensions need builds for every OS/arch/Python (cibuildwheel).
- Check correctness against the original implementation with property tests; float summation order changes results slightly.

## Verify
- A `pytest-benchmark` or `timeit` comparison shows the speedup on realistic data sizes, and outputs match the pure-Python reference within tolerance.
