---
id: computing-software.data-engineering.apache-flink.memory-configuration
name: memory-configuration
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-deployment, flink-memory-configuration, taskmanager-memory, managed-memory, network-buffers, rocksdb-memory, oom-troubleshooting, jobmanager-memory]
level: practitioner
status: docs-checked
description: "Size Flink TaskManager and JobManager memory: process vs flink size, managed memory for RocksDB, network buffers, metaspace and overhead, and mapping each OOM error to the right knob."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/memory/mem_setup/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/memory/mem_setup_tm/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/memory/mem_tuning/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/memory/mem_trouble/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink memory configuration

**Goal:** TaskManagers that use their container memory fully without being OOM-killed, with the right share for state and network.

## 1. Set one top-level size
- Containers (Kubernetes, YARN): set `taskmanager.memory.process.size` (= container memory request). Flink derives the rest.
- Standalone/bare metal: `taskmanager.memory.flink.size` (excludes JVM metaspace and overhead).
- Explicitly configuring both total process memory and total Flink memory is not recommended and can cause deployment failures from memory configuration conflicts; set one total plus only the components you deliberately change. One of the documented option subsets must be configured or startup fails (except for local execution).
Same for JobManager: `jobmanager.memory.process.size` (no default value).

## 2. TaskManager components
| Component | Option | Default | Used by |
|---|---|---|---|
| Framework heap / off-heap | `taskmanager.memory.framework.*` | 128 MB each | Flink runtime — rarely change |
| Task heap | `taskmanager.memory.task.heap.size` | derived from the other components | your operators, heap state backend |
| Task off-heap | `taskmanager.memory.task.off-heap.size` | 0 | native libs / direct buffers in user code |
| Managed memory | `taskmanager.memory.managed.fraction` | 0.4 of total Flink memory | RocksDB, batch operators, Python UDF processes |
| Network | `taskmanager.memory.network.fraction` / `min` / `max` | 0.1, 64 MB, infinite | shuffle buffers |
| JVM metaspace | `taskmanager.memory.jvm-metaspace.size` | 256 MB | loaded classes |
| JVM overhead | `taskmanager.memory.jvm-overhead.fraction` / `min` / `max` | 0.1, 192 MB-1 GB | thread stacks, GC, native |

## 3. Tune by state backend
- **RocksDB**: memory control is on by default (`state.backend.rocksdb.memory.managed: true`), so RocksDB uses managed memory; raise `managed.fraction` if RocksDB needs more.
- **HashMap (heap) or stateless jobs**: the managed memory is unused unless batch operators or Python UDFs need it; the memory tuning page recommends setting it to zero so the heap gets the memory.

## 4. Error → knob
| Symptom | Raise |
|---|---|
| `java.lang.OutOfMemoryError: Java heap space` | task heap (or switch large state to RocksDB) |
| `OutOfMemoryError: Direct buffer memory` | direct off-heap memory (task off-heap); also check for a direct memory leak in user code or dependencies |
| `OutOfMemoryError: Metaspace` | `jvm-metaspace.size` |
| Container killed by Kubernetes/YARN for exceeding its requested memory | native memory is under-reserved: with RocksDB and memory control off, raise managed memory; with it on and non-heap memory growing during savepoints or full checkpoints, set `MALLOC_ARENA_MAX=1` for TaskManagers or raise JVM overhead |
| `IOException: Insufficient number of network buffers` | `taskmanager.memory.network.min` / `max` / `fraction` |

## 5. Read what Flink computed
Check the memory breakdown Flink computed after every change (TaskManager startup log and the Web UI TaskManager pages).

## 6. Slots
`taskmanager.numberOfTaskSlots` (default 1) sets how many parallel operator or user function instances a TaskManager runs.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the memory setup, TaskManager setup, memory tuning and memory troubleshooting pages and the generated configuration tables (defaults for framework heap/off-heap 128 mb, task off-heap 0, managed fraction 0.4, network fraction 0.1 / min 64 mb / max infinite, metaspace 256 mb, JVM overhead 0.1 / 192 mb / 1 gb, `jobmanager.memory.process.size` none, `state.backend.rocksdb.memory.managed` true, `taskmanager.numberOfTaskSlots` 1). Corrected the network maximum (infinite, not 1 GB); removed unconfirmed JobManager default, tuning ratios, exit code and slot-sharing claims.

Method: documentation only; no commands were run.

## Verify
- [ ] No container kills over a week at peak load.
- [ ] Managed memory used ≈ configured for RocksDB jobs; 0 configured where unused.
- [ ] GC time is monitored (TM metrics) and stable.
