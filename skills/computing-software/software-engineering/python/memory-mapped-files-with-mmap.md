---
id: computing-software.software-engineering.python.memory-mapped-files-with-mmap
name: memory-mapped-files-with-mmap
category: computing-software
field: software-engineering
product: python
tags: [python, py-io, mmap-files, mmap, memory-mapping, random-access, large-files, ipc]
level: practitioner
status: docs-checked
description: "Search, slice and patch large files without loading them using mmap: access modes, find/regex, flush, resizing and the trackfd option."
sources: ["https://docs.python.org/3/library/mmap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory-mapped files with mmap

```python
import mmap, re

with open("big.log", "rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
    i = mm.find(b"ERROR")                    # fast byte search, no copy of the file
    line_end = mm.find(b"\n", i)
    print(mm[i:line_end].decode("utf-8", "replace"))
    for m in re.finditer(rb"user=(\w+)", mm):    # regex runs straight over the map
        ...
    mm.seek(0); mm.readline()

with open("data.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)            # Unix default: shared, read/write
    mm[0:4] = b"\xde\xad\xbe\xef"            # slice assignment
    mm.flush()                               # msync to disk
    mm.close()
```

## Modes
- `ACCESS_READ`, `ACCESS_WRITE` (write-through to file), `ACCESS_COPY` (private copy-on-write; not saved).
- `length=0` maps the whole file; `offset` must be a multiple of `mmap.ALLOCATIONGRANULARITY`.
- `mm.resize(n)` is available on Windows and systems with `mremap()`; it raises `TypeError` for `ACCESS_READ`/`ACCESS_COPY` maps and `ValueError` when `trackfd=False`.
- Pass `-1` as the file descriptor (with a length) to map anonymous memory; on Windows `tagname` names the map.

## Why use it
Random access into a multi-GB file, repeated scans with page-cache reuse, or `bytes`-like search with no read loop. Sequential one-pass processing is often just as fast with buffered reads.

## Gotchas
- On Windows you cannot create an empty mapping (an empty file raises an exception).
- If you map a writable, buffered file, `flush()` the file object first so local buffered changes are visible to the mapping.
- `mm.flush()` flushes changes to disk; `ACCESS_COPY` changes never reach the file.
- `trackfd=False` limits the number of open file descriptors (added in 3.13 on Unix, 3.15 on Windows), but then `size()` and `resize()` do not work.
- `mmap.set_name()` (3.15, Linux 5.17+ with `-X dev` or a debug build) names a map in `/proc/<pid>/maps`.

## Verify
- [ ] Open the mapped file in another process and check writes are visible after `flush()`.

## Checked

- 2026-11-03: checked against the CPython docs `library/mmap.rst`: access modes, `length=0`, `offset` and `ALLOCATIONGRANULARITY`, anonymous maps (`-1`), `tagname`, `resize` availability and errors, `flush`, `trackfd` versions, `set_name` (3.15), Windows empty-map limitation, buffered-file flush note.
- Removed: SIGBUS/truncation, 32-bit limit, memoryview/BufferError, fsync and psutil RSS claims, the exact ValueError text (not in the docs read).

Method: documentation only; no commands were run.
