---
id: computing-software.data-science-and-analytics.pandas-numpy.structured-arrays-and-memmap
name: structured-arrays-and-memmap
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [structured-arrays, np-memmap]
level: advanced
status: docs-checked
description: "Handle record-like data with structured dtypes and large binary files with np.memmap, including modes and flush."
sources:
  - https://numpy.org/doc/stable/user/basics.rec.html
  - https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured arrays, memmap, I/O
```python
dt = np.dtype([("id", "i4"), ("x", "f8"), ("tag", "U8")])
r = np.zeros(3, dtype=dt); r["x"] = [1.0, 2.0, 3.0]
mm = np.memmap("big.dat", dtype="f4", mode="r", shape=(10_000_000,))
```
## Gotchas
- A memmap reads small segments of a large file on disk without loading the whole file into memory.
- `mode` is `"r+"` by default (read and write); `"r"` is read-only, `"w+"` creates or overwrites and needs `shape`, and `"c"` is copy-on-write so changes are not saved.
- Call `flush()` to write memmap changes to the file; there is no API to close the underlying mmap.
- The memmap class has documented awkward interactions with some operations because it is an ndarray subclass.
## Verify
- [ ] Data reopened with `mode="r"` matches what was written.

## Checked

Method: docs-checked 2026-11-09 against the numpy.memmap reference and the NumPy structured arrays guide (np.dtype field-list form), read via text conversion. Dropped the .npy/.npz save and load lines and the allow_pickle advice, which neither page covers.
