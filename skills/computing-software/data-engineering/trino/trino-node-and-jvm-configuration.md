---
id: computing-software.data-engineering.trino.trino-node-and-jvm-configuration
name: trino-node-and-jvm-configuration
category: computing-software
field: data-engineering
product: trino
tags: [node-properties, jvm-config, heap-size, node-environment, tmpdir]
level: practitioner
status: docs-checked
description: "Write Trino etc/node.properties and etc/jvm.config: required node identity fields, starter JVM flags, heap sizing rule and the noexec temp directory trap."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/installation/deployment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino node and jvm configuration

Create an `etc` directory in the installation directory; it holds node properties, JVM config, config properties and catalog properties.

`etc/node.properties` is per node:

```text
node.environment=production
node.id=ffffffff-ffff-ffff-ffff-ffffffffffff
node.data-dir=/var/trino/data
```

- `node.environment`: identical on all nodes in a cluster; starts with a lowercase alphanumeric, then lowercase alphanumerics or `_`.
- `node.id`: unique per node and stable across reboots and upgrades; alphanumerics, `-` or `_`. Several installations on one machine each need their own.
- `node.data-dir`: where logs and other data go.

`etc/jvm.config` lists JVM options one per line, unquoted. The docs' starting point includes `-server`, `-Xmx16G`, `-XX:InitialRAMPercentage=80`, `-XX:MaxRAMPercentage=80`, `-XX:G1HeapRegionSize=32M`, `-XX:+ExplicitGCInvokesConcurrent`, `-XX:+ExitOnOutOfMemoryError`, `-XX:+HeapDumpOnOutOfMemoryError`, `-XX:-OmitStackTraceInFastThrow`, `-XX:ReservedCodeCacheSize=512M`, `-XX:PerMethodRecompilationCutoff=10000`, `-XX:PerBytecodeRecompilationCutoff=10000`, `-Djdk.attach.allowAttachSelf=true`, `-Djdk.nio.maxCachedBufferSize=2000000` and `--add-modules=jdk.incubator.vector`.

Sizing: set `-Xmx` to 70 to 85 percent of node memory (for 64GB RAM, `-Xmx54G`), leaving room for the OS, other services and off-heap native memory. Larger nodes can use a lower percentage. Giving all memory to the JVM or using swap is unsupported; disable swap. Over 32GB is recommended in production. An OutOfMemoryError leaves the JVM inconsistent, hence the heap dump and forced exit.

Temp directory trap: the JVM temp directory must allow execution because Trino loads native libraries (for compression). If `/tmp` is mounted `noexec`, Trino will not start; add `-Djava.io.tmpdir=/path/to/other/tmpdir`.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Added two JVM flags the page lists but the skill omitted; rest matches.
