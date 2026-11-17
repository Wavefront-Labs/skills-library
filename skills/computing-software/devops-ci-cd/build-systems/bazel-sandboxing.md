---
id: computing-software.devops-ci-cd.build-systems.bazel-sandboxing
name: bazel-sandboxing
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [bazel, build-systems, hermetic-builds, bazel-sandbox, linux-sandbox, spawn-strategy, sandbox-debug, undeclared-inputs, sandbox-default-allow-network, sandboxfs, hermetic-toolchains, bazelrc, execution-log]
level: advanced
status: docs-checked
description: "Use Bazel sandboxing to catch undeclared inputs: spawn strategies, linux-sandbox options, blocking network, debugging failures with --sandbox_debug, and performance trade-offs."
sources: ["https://bazel.build/docs/sandboxing", "https://bazel.build/reference/command-line-reference#flag--spawn_strategy", "https://bazel.build/reference/command-line-reference#flag--sandbox_debug", "https://github.com/bazelbuild/bazel/blob/master/src/main/java/com/google/devtools/build/lib/actions/ExecutionRequirements.java"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel sandboxing

Bazel runs each action (spawn) in a sandbox containing only its declared inputs. An
action that reads an undeclared file or tool fails here instead of producing a
non-reproducible, wrongly cached result.

## Strategies
```
# .bazelrc
build --spawn_strategy=linux-sandbox,sandboxed,local     # first strategy that works per action
build --incompatible_strict_action_env                   # static PATH, no LD_LIBRARY_PATH from the host (on by default)
build --sandbox_default_allow_network=false              # no network inside actions
test  --sandbox_default_allow_network=false
build --reuse_sandbox_directories                        # reuse sandbox directories (default true; older name --experimental_reuse_sandbox_directories)
# build --sandbox_base=/dev/shm                          # tmpfs sandboxes (needs RAM)
```
- `linux-sandbox`: builds on `processwrapper-sandbox` and uses Linux namespaces (user, mount, PID, network, IPC); the strongest local isolation on Linux. It does not work "nested" (for example inside a Docker container without extra privileges); Bazel then falls back to `processwrapper-sandbox` (or `local`).
- `processwrapper-sandbox`: no special OS features; the generic sandbox.
- `darwin-sandbox`: macOS equivalent, using Apple's `sandbox-exec`.
- `sandboxed`: generic name that picks the best sandbox available; use `--spawn_strategy=sandboxed` (without `local` in the list) to fail rather than fall back.
- `local` (a.k.a. `standalone`): no sandboxing; for actions that cannot work otherwise.
- `remote`: actions run on remote executors.
- Persistent workers run in a generic sandbox with `--worker_sandboxing` (also scoped per mnemonic).

Per-target escape hatches (use sparingly, they're audit points):
```python
genrule(name = "x", ..., tags = ["no-sandbox"])          # others: "requires-network", "no-remote", "block-network"
```
`requires-network` lets that one action reach the network when the default is blocked.

## Debugging failures
```bash
bazel build //pkg:target --sandbox_debug --verbose_failures
# keeps the sandbox directory and prints the command and its location
bazel aquery //pkg:target            # declared inputs/outputs of the action
```
Typical causes: a tool assumed on the host (`/usr/bin/python3`) -> use hermetic toolchains; a generated header not in `hdrs`/`srcs`; a test reading a data file not in `data = [...]`.

## Finding non-hermeticity
- Build twice from clean states (ideally on two machines) with
  `--execution_log_compact_file=exec1.log` / `exec2.log` and compare them with the execlog parser (`//src/tools/execlog:parser`): actions whose inputs or outputs differ are leaking environment or are non-deterministic.
- A remote cache hit rate that drops between machines signals the same leakage.

## Performance
Sandboxing costs setup time per action. Reusing sandbox directories, a tmpfs `--sandbox_base`, and remote execution reduce it. Don't disable sandboxing for speed in CI: that's where hermeticity matters.

## Verify
`bazel build //... --sandbox_debug` succeeds with network disabled; deliberately reference
an undeclared file in a genrule: the build fails inside the sandbox rather than succeeding.

## Checked
Date: 2026-10-25. Documentation: Bazel sandboxing page (`docs/docs/sandboxing.mdx`), `SandboxOptions.java`, `ExecutionOptions.java`, `ExecutionRequirements.java`, `BazelRuleClassProvider.java` (bazelbuild/bazel, default branch).
Confirmed: strategy names and semantics (`linux-sandbox`, `processwrapper-sandbox`, `darwin-sandbox`, `sandboxed`, `local`/`standalone`) and the nested-sandbox fallback; `--spawn_strategy` fallback lists; `--sandbox_default_allow_network` (default true), `--sandbox_debug`, `--sandbox_base`, `--worker_sandboxing`; `--reuse_sandbox_directories` (default true, old `--experimental_` name kept); execution requirement tags `no-sandbox`, `requires-network`, `no-remote`, `block-network`; `--incompatible_strict_action_env` default true; execution log flags.
Removed: `--incompatible_sandbox_hermetic_tmp` (no such option in the current source), the "(macOS default via darwin-sandbox)" wording on `processwrapper-sandbox`, the "few % to 20%" overhead figure, and the `--execution_log_json_file` diff recipe (replaced by the compact log).
Method: documentation only; no commands were run.
