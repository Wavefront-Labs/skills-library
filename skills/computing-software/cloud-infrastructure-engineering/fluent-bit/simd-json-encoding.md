---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.simd-json-encoding
name: simd-json-encoding
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, simd, json-encoding, yyjson, performance, build-flags]
level: advanced
status: docs-checked
description: "Check for SIMD JSON encoding in Fluent Bit at startup and build with FLB_SIMD when it is missing."
sources: ["https://docs.fluentbit.io/manual/administration/performance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SIMD JSON encoding

Fluent Bit v4.1.0 introduced SIMD (Single Instruction, Multiple Data) JSON encoding, powered by the `yyjson` project. Plugins that convert logs from the internal binary representation to JSON can do so 2.5 times faster, according to the docs. It is available on x86_64, amd64, aarch64 and arm64.

The binary must be built with SIMD support. The docs say SIMD is enabled by default only in Fluent Bit container images.

**Check.** Look for a `simd` line in the startup log:

```text
[ info] [simd    ] SSE2
```

The value shows the support type, such as `SSE2`, `NEON` or `none`.

**Enable.** If your binary was not built with SIMD and you are on a supported platform, build from source with the CMake option:

```shell
cmake -DFLB_SIMD=On ..
```

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs performance tips page (raw markdown, read in full).
