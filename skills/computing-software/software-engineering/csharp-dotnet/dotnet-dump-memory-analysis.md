---
id: computing-software.software-engineering.csharp-dotnet.dotnet-dump-memory-analysis
name: dotnet-dump-memory-analysis
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, dotnet-diagnostics, dotnet-dump, memory-leak, gc-roots, sos, heap-analysis, dotnet-memory-management]
level: practitioner
status: docs-checked
description: "Capture and analyse .NET memory dumps with dotnet-dump and SOS: heap statistics, finding leaks via gcroot, async state machines, threads and deadlocks, and dump hygiene."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-dump
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-gcdump
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-memory-leak
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/sos-debugging-extension
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/collect-dumps-crash
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dotnet-dump memory analysis

**Goal:** find what is holding memory (or deadlocking threads) in a .NET process from a dump, on any OS.

## 1. Capture
```bash
dotnet tool install -g dotnet-dump
dotnet-dump collect -p <pid> --type Heap -o app.dmp        # Full (default) is largest; Heap omits mapped images
dotnet-gcdump collect -p <pid> -o app.gcdump               # GC heap graph only, collected through EventPipe
```
Crash dumps automatically:
```bash
DOTNET_DbgEnableMiniDump=1 DOTNET_DbgMiniDumpType=2 DOTNET_DbgMiniDumpName=/dumps/core.%p   # type 2 = Heap (default); %p = PID
```
Take two or three dumps minutes apart during growth to compare.

## 2. Analyse
```bash
dotnet-dump analyze app.dmp
> dumpheap -stat                         # types by total size; bottom = biggest
> dumpheap -stat -min <size>            # only objects of at least <size> bytes
> dumpheap -mt <MethodTable>             # instances of one type
> gcroot <object address>                # reference chain keeping it alive
> eeheap -gc                             # heap generations/segments
> dumpobj <addr>  /  dumparray <addr>
```
Typical leak roots to look for in `gcroot` chains: static collections and caches without eviction, event handlers where the publisher outlives the subscriber, timers holding closures, and scopes never disposed.

## 3. Threads, async and deadlocks
```
> clrthreads                 # managed threads, lock counts
> clrstack                  # managed stack of the current thread
> pe                         # exception on current thread
> syncblk                    # monitors held and waiters (lock deadlocks)
> dumpasync                  # async state machines on the heap (-type, -waiting, -roots filters)
> threadpool                 # thread pool info (starvation)
> threadpoolqueue            # queued thread pool work items
```
Many threads blocked in `Task.Wait`/`.Result` with a large thread pool queue = sync-over-async starvation.

## 4. Elsewhere

## Gotchas
- Dumps contain whatever was in process memory (connection strings, tokens, personal data); treat them as sensitive data and delete them after analysis.
- Collecting a full or heap dump may make the OS page in substantial virtual memory for the target process, which can matter in a container with a memory limit; consider removing the instance from rotation first.
- High memory without a managed leak: `eeheap` shows runtime-internal memory; check GC settings too.

## Verify
- After the fix, two dumps taken an hour apart show stable counts for the previously growing type, and the working set plateaus under the same load.

## Checked

Checked 2026-10-25 against dotnet/docs (core/diagnostics/dotnet-dump, dotnet-gcdump, collect-dumps-crash, sos-debugging-extension) on main.
Confirmed: `dotnet-dump collect --type Full|Heap|Mini` with Full the default; `DOTNET_DbgEnableMiniDump`, `DOTNET_DbgMiniDumpType` (default 2 = Heap) and `DOTNET_DbgMiniDumpName` with `%p`; SOS `dumpheap` (`-stat`, `-min`, `-mt`), `gcroot`, `eeheap -gc`, `dumpobj`, `dumparray`, `clrthreads`, `clrstack`, `pe`, `syncblk`, `dumpasync`, `threadpool`, `threadpoolqueue`; memory warning when collecting full or heap dumps in a limited container.
Removed as unconfirmed: `dumpasync --stats`, `setthread`, `maddress`, the `-min 85000` large-object-heap threshold, GC settings advice, third-party tool mentions, cross-OS analysis note.

Method: documentation only; no commands were run.
