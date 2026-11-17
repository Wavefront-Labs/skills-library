---
id: computing-software.devops-ci-cd.bazel.bazelrc-named-configs-and-platform-configs
name: bazelrc-named-configs-and-platform-configs
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazelrc, config-flag, build-config, enable-platform-specific-config, named-config, startup-options]
level: practitioner
status: docs-checked
description: "Group flags under build:name lines in .bazelrc, invoke them with --config, and auto-enable per-OS configs."
sources: ["https://bazel.build/run/bazelrc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Named configs in .bazelrc

Add a `:name` suffix to a command to make a config that is ignored until requested with `--config=name` (on the command line or inside another config, recursively):

```
build:memcheck --strip=never --test_timeout=3600
```

`--config=ci` expands in place, so the config's options get the same precedence the `--config` flag had. A `command:name` line is only expanded for applicable commands, and all `command:name` lines across every rc file are merged. To avoid name clashes, begin configs in personal rc files with an underscore (`_mine`).

Startup options cannot be set this way: `startup:name --opt` is ignored.

Per-OS configs: pass `--enable_platform_specific_config` and `build:linux`, `build:macos`, `build:windows`, `build:freebsd`, `build:openbsd` are applied automatically for the host OS, as if you had passed `--config=linux` and so on. Platform-specific `startup:linux` lines always apply, without the flag.

```
common --enable_platform_specific_config
build:linux --cxxopt=-std=c++17
build:windows --cxxopt=/std:c++17
```

Related files: `.bazelignore` at the workspace root lists directories to skip (one per line, no globs). Bazel 8 adds `REPO.bazel` with `ignore_directories()` that does accept globs.

## Checked

2026-11-04. Read against the Bazel docs page(s): Write bazelrc configuration files (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the invented ci config examples and the claim about undefined config names (not on the page), and the closing Verify line.
Method: documentation only; no commands were run.
