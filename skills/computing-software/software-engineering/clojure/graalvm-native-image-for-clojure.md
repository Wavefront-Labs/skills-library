---
id: computing-software.software-engineering.clojure.graalvm-native-image-for-clojure
name: graalvm-native-image-for-clojure
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, graalvm, native-image, reflection-config, aot, babashka, startup-time, clj-easy, deployment, deploy-graalvm-native]
level: advanced
status: draft
description: "Compile Clojure to a native executable with GraalVM native-image from an AOT uberjar, using direct linking, reflection config, and the graal-build-time helper."
sources: ["https://github.com/clj-easy/graalvm-clojure", "https://www.graalvm.org/latest/reference-manual/native-image/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GraalVM native-image

**Goal:** a fast-starting standalone binary for CLIs and small services.

Steps:
1. Build an AOT uberjar with direct linking: `-Dclojure.compiler.direct-linking=true` (JVM option in the build) and
   `(:gen-class)` on the main namespace.
2. Run `native-image -jar target/app.jar --no-fallback --initialize-at-build-time --enable-url-protocols=https app`.
   (Flags vary by GraalVM version; consult the docs.)
3. Add `com.github.clj-easy/graal-build-time` to the dependencies; it registers Clojure classes for build-time
   initialisation.
4. Provide reflection configuration (`reflect-config.json`) for any reflective interop, or remove reflection with
   type hints; run with the tracing agent: `java -agentlib:native-image-agent=config-output-dir=cfg -jar app.jar`.

- Dynamic features (`eval`, `require` at runtime, `load-string`, runtime classloading) do not work unless
  included at build time.
- Reflection warnings (`*warn-on-reflection*`) are the first thing to fix.
- Libraries must be graal-compatible; check clj-easy/graalvm-clojure for known-good setups.
- Build in CI for each target OS/arch: binaries are not portable. Static or mostly-static linking is available
  on Linux (`--static`, `--libc=musl`).
- Babashka and clj-kondo are examples of Clojure compiled to native binaries.

## Failure modes
- `ClassNotFoundException` or `NoSuchMethodException` at runtime in the native binary: missing reflect-config.
- "Classes that should be initialized at run time got initialized during image building".

## Self-check
Compare startup time of `java -jar` and the native binary for a hello-world with `time`.
