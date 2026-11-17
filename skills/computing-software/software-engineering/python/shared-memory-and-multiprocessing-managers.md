---
id: computing-software.software-engineering.python.shared-memory-and-multiprocessing-managers
name: shared-memory-and-multiprocessing-managers
category: computing-software
field: software-engineering
product: python
tags: [python, py-multiproc, shared-memory-manager, shared-memory, sharedmemory, multiprocessing-manager, numpy, zero-copy]
level: practitioner
status: docs-checked
description: "Share large arrays between processes with multiprocessing.shared_memory, handle unlink and resource tracking, and choose Manager proxies, Value/Array or queues instead."
sources: ["https://docs.python.org/3/library/multiprocessing.shared_memory.html", "https://docs.python.org/3/library/multiprocessing.html#managers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared memory and multiprocessing managers

## shared_memory (3.8+): zero-copy blocks
```python
import numpy as np
from multiprocessing import shared_memory, Process

def worker(name, shape, dtype):
    shm = shared_memory.SharedMemory(name=name)          # attach by name
    arr = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
    arr[:] *= 2
    del arr                                              # drop views before close
    shm.close()

if __name__ == "__main__":
    a = np.arange(10, dtype=np.int64)
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
    view = np.ndarray(a.shape, a.dtype, buffer=shm.buf); view[:] = a
    p = Process(target=worker, args=(shm.name, a.shape, a.dtype)); p.start(); p.join()
    print(view)                                          # doubled
    del view; shm.close(); shm.unlink()                  # creator unlinks exactly once
```
`multiprocessing.shared_memory.SharedMemoryManager` automates unlink on context exit and also provides `ShareableList`.

## Alternatives
- `Value`/`Array` (ctypes in shared memory) for tiny counters.
- `Manager()`: a server process holds the objects and other processes use proxies; flexible, but not zero-copy, so prefer `shared_memory` for bulk data.
- Queues/Pipes for message passing (objects are pickled).

## Gotchas
- `close()` in every process, `unlink()` only once per block; `unlink()` has no effect on Windows, where the block is freed when all handles are closed. Without `unlink()` the block can outlive the processes on other platforms.
- Delete NumPy views before `close()`, since they export the buffer.
- With `track=True` (default) a standalone process that attaches is given its own resource tracker, and the block can be deleted when the first such process terminates; 3.13 added `track=False` for that case (ignored on Windows).
- The block size may be larger than requested (platform page size), and is ignored when attaching; keep your own length.
- No synchronisation is provided: guard writes with a `Lock` or partition the array so writers touch disjoint slices.
- Under `spawn` (Windows/macOS default) guard the entry point with `if __name__ == "__main__":`.

## Verify
- [ ] After the run, no stale shared memory block from your name prefix remains.
- [ ] Test with `spawn` start method explicitly (`mp.set_start_method("spawn")`).

## Checked

2026-11-08. Confirmed on the multiprocessing.shared_memory page and the multiprocessing page: `SharedMemory(name, create, size, *, track=True)` added in 3.8 with `track` in 3.13, `close()` per instance and `unlink()` once per block, `unlink()` no effect on Windows, size possibly larger than requested and ignored when attaching, `SharedMemoryManager` and `ShareableList`, `Manager()` server process, spawn as the default start method on Windows and macOS and the `if __name__ == '__main__'` guard. Removed: `Value/Array get_lock()`, the `/dev/shm` leak and `ls` check, the exact BufferError text and the "leaked shared_memory objects" warning wording, and the per-access IPC round-trip claim (not on the cited pages).

Method: docs-only read of cited pages, 2026-11-08
