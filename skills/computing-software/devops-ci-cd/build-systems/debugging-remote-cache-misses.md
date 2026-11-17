---
id: computing-software.devops-ci-cd.build-systems.debugging-remote-cache-misses
name: debugging-remote-cache-misses
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, cache-miss-debugging, remote-cache, bazel-remote-cache]
level: advanced
status: docs-checked
description: "Find why remote build cache hit rates are low: Bazel execution log diffing, Gradle build scans and cache key inputs, non-hermetic inputs, absolute paths and env leakage."
sources: ["https://bazel.build/remote/caching", "https://github.com/bazelbuild/bazel/tree/master/src/tools/execlog", "https://docs.gradle.org/current/userguide/build_cache_debugging.html", "https://docs.gradle.org/current/userguide/common_caching_problems.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging remote cache misses

## Bazel
```bash
bazel build //... --execution_log_compact_file=/tmp/exec1.log      # run A (e.g. CI)
bazel build //... --execution_log_compact_file=/tmp/exec2.log      # run B (e.g. local)
# the execlog parser in the bazel repo (src/tools/execlog) reads the compact, binary and JSON formats;
# giving it two logs reorders the second to match the first so a text diff is meaningful
bazel run //src/tools/execlog:parser -- \
  --log_path=/tmp/exec1.log --log_path=/tmp/exec2.log \
  --output_path=/tmp/1.txt --output_path=/tmp/2.txt
diff /tmp/1.txt /tmp/2.txt
```
The first differing action shows the input or environment variable that changed the key.
A Build Event Protocol UI (BuildBuddy, EngFlow) lists uncached actions per invocation (`--bes_backend`, `--bes_results_url`), which can be quicker for a first look.

Typical causes: environment variables passed with `--action_env` that differ between machines (`--incompatible_strict_action_env` is on by default in current Bazel and gives a static `PATH`), different toolchain paths, timestamps or absolute paths embedded in outputs.

## Gradle
- A Build Scan (`--scan`) has a timeline view of cache hits and misses per task and a task-inputs comparison between two builds.
- `-Dorg.gradle.caching.debug=true` logs the build cache key and the hash of each input property.
Causes: absolute paths in task inputs (declare path sensitivity with `@PathSensitive`), volatile inputs such as timestamps, different Java major versions (or vendor and implementation when toolchains are used), line endings converted by `core.autocrlf` on Windows checkouts (set `autocrlf=false` or normalise with `.gitattributes`), symbolic links in inputs (not cached between Windows and Linux).

## General checklist
1. Compare CI-to-CI first (same machine type), then CI-to-local.
2. Hunt environment leakage, absolute paths, timestamps, unpinned toolchains.
3. Make CI the only writer; dev machines read-only, so poisoned or odd entries are not uploaded.

## Verify
- [ ] Two consecutive CI builds of the same commit show (almost) all actions served from the remote cache.

## Checked
Date: 2026-10-25. Documentation: Bazel sources and docs (bazelbuild/bazel: `ExecutionOptions.java`, `src/tools/execlog` `ParserOptions.java` and `ExecLogParser.java`, `BazelRuleClassProvider.java`, `docs/remote/caching.mdx`); Gradle user guide pages "Build cache debugging" and "Common caching problems" (gradle/gradle).
Confirmed: `--execution_log_compact_file` (older name `--experimental_execution_log_compact_file`); the `//src/tools/execlog:parser` target with `--log_path` and `--output_path`, repeatable for two logs with reordering; compact format handled by the parser; `--incompatible_strict_action_env` default true; `--bes_backend` and `--bes_results_url`; Gradle `-Dorg.gradle.caching.debug=true`, Build Scan timeline, line-ending and symlink notes, Java major version tracking and toolchains.
Removed: "local `--host_javabase`" and "annotation processors not declared" as causes (not in the pages read) and the exact Build Scan menu path.
Method: documentation only; no commands were run.
