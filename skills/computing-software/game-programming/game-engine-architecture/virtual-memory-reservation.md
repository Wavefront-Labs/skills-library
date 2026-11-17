---
id: computing-software.game-programming.game-engine-architecture.virtual-memory-reservation
name: virtual-memory-reservation
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, virtual-memory, memory-reservation, allocators, game-programming]
level: practitioner
status: docs-checked
description: "Use virtual memory in engines: reserve large address ranges and commit pages on demand, growable arrays without copying, guard pages and platform APIs."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc", "https://man7.org/linux/man-pages/man2/mmap.2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual memory reservation

**Goal:** exploit 64-bit address space: reserve big contiguous ranges up front, back them with
physical pages only as needed.

## APIs
```cpp
// Windows
void* base = VirtualAlloc(nullptr, 64ull << 30, MEM_RESERVE, PAGE_NOACCESS);      // 64 GB address range
VirtualAlloc(base, 1 << 20, MEM_COMMIT, PAGE_READWRITE);                           // commit first 1 MB
VirtualFree(base, 0, MEM_RELEASE);
// POSIX
void* b = mmap(nullptr, size, PROT_NONE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE, -1, 0);
mprotect(b, commitBytes, PROT_READ | PROT_WRITE);     // make the committed prefix accessible
munmap(b, size);
```
Query the page size and the reservation (allocation) granularity at run time with `GetSystemInfo` on
Windows; reserved addresses are rounded down to the allocation granularity, committed ones to a page boundary.

## Uses
- **Growable arena/array that never moves:** reserve max size, commit more as it grows; pointers
  stay valid (no realloc copy). Great for entity arrays and per-level arenas.
- **Guard pages:** leave an uncommitted page after stacks or buffers to catch overruns instantly.
- **Memory debug allocators:** place each allocation at the end of a page with a guard page after
  (like PageHeap) to catch overflows.
- **Decommit** (`MEM_DECOMMIT`, `madvise(MADV_DONTNEED)`) to return memory after a level unload
  while keeping the address range.

## Platform notes
- Consoles have their own memory APIs and limits; check the platform docs.
- Large pages on Windows need the `SeLockMemoryPrivilege` privilege and `MEM_LARGE_PAGES`.
- Linux overcommit behaviour is controlled by `/proc/sys/vm/overcommit_memory` (see proc_sys_vm(5)); check it for your target.

## Verify
- Reserve 64 GB, commit 10 MB; process private bytes show ~10 MB. Write past committed range:
  immediate access violation.

## Checked

- Date: 2026-11-02.
- Confirmed against: Microsoft Learn VirtualAlloc, VirtualFree and large-page support pages (MEM_RESERVE, MEM_COMMIT, MEM_RELEASE, MEM_DECOMMIT, PAGE_NOACCESS, MEM_LARGE_PAGES, SeLockMemoryPrivilege, allocation granularity vs page boundary, GetSystemInfo); mmap(2) and madvise(2) man pages (PROT_NONE, MAP_ANONYMOUS, MAP_NORESERVE, munmap, MADV_DONTNEED, overcommit_memory).
- Removed: the 4 KB / 64 KB / 2 MB page-size figures, the console page-size figures, the TLB claim and the "Linux overcommits by default" claim (not stated in the fetched pages).

Method: documentation only; no commands were run.
