---
id: computing-software.game-programming.game-engine-architecture.worker-thread-pools-and-affinity
name: worker-thread-pools-and-affinity
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, thread-affinity, thread-pool, multithreading, game-programming]
level: practitioner
status: draft
description: "Configure engine worker threads: worker count from core topology, affinity and priorities, P-core vs E-core hybrids, SMT, and console core reservations."
sources: ["https://learn.microsoft.com/en-us/windows/win32/procthread/multiple-processors", "https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getlogicalprocessorinformationex"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Worker thread pools and affinity

**Goal:** the right number of worker threads, placed on the right cores, without starving the main
and render threads or the OS.

## Worker count
- Start from physical cores, not logical: `GetLogicalProcessorInformationEx(RelationProcessorCore)`
  on Windows, `/sys/devices/system/cpu/*/topology` or `hwloc` on Linux.
  `std::thread::hardware_concurrency()` returns logical processors.
- Typical: workers = cores - 1 (main) - 1 (render) or cores - 2 with the main thread also executing jobs.
- Leave headroom for audio, streaming I/O, and the OS/driver threads.

## Affinity
- Consoles: pin one worker per core; cores are fixed and some are reserved for the OS.
- PC: hard affinity often hurts (OS can't move threads off busy cores, other apps compete). Prefer
  soft hints: `SetThreadIdealProcessor`, or leave affinity unset and only set priorities.
- **Hybrid CPUs (Intel P/E cores):** latency-critical threads (main, render) on P-cores. Windows
  uses Thread Director with QoS: `SetThreadInformation(ThreadPowerThrottling)` marks threads
  efficiency-oriented (EcoQoS -> E-cores). Background streaming/compilation threads can be EcoQoS.
- **SMT:** two hyperthreads share a core; heavy SIMD workers on both siblings may run slower than
  one; benchmark using physical-core-only pools.

## Priorities
- Audio mixing thread high priority (`THREAD_PRIORITY_TIME_CRITICAL` or MMCSS "Pro Audio"/"Games"
  via `AvSetMmThreadCharacteristics`).
- Asset loading below normal.
- Workers normal; a worker blocked waiting for a low-priority thread causes priority inversion;
  avoid locks shared across priority levels.

## Verify
- Profile (Tracy, PIX, VTune) on 4-, 8- and 16-core plus hybrid machines; check workers are busy
  and main/render threads aren't preempted at frame-critical times.
