---
id: computing-software.devops-ci-cd.bazel.bazel-output-directories-and-base-flags
name: bazel-output-directories-and-base-flags
category: computing-software
field: devops-ci-cd
product: bazel
tags: [output-base, output-user-root, bazel-bin, bazel-out, bazel-testlogs, execroot, xdg-cache-home, output-directory]
level: practitioner
status: docs-checked
description: "Locate Bazel output_base, execroot and convenience symlinks, and relocate them with --output_base or --output_user_root."
sources: ["https://bazel.build/remote/output-directories"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel output directory layout

`outputRoot` defaults to `~/.cache/bazel` on Linux, `~/Library/Caches/bazel` on macOS with Bazel 9 and newer (Bazel 8 and earlier used `/private/var/tmp` and ignored `$XDG_CACHE_HOME`), and `%HOME%` / `%USERPROFILE%` on Windows. `$XDG_CACHE_HOME`, when set, overrides it to `${XDG_CACHE_HOME}/bazel`.

Under it:
- `_bazel_$USER/` is the outputUserRoot.
- `install/<md5 of install manifest>/` is the installBase (server jar, `linux-sandbox`, `process-wrapper`, embedded tools).
- `<md5 of workspace path>/` is the outputBase. Reproduce the hash with `echo -n $(pwd) | md5sum` at the workspace root.
- Within outputBase: `action_cache/`, `command.log` (last command's output), `external/` (fetched repos), `server/` (PID, port, `jvm.out`), `execroot/` (the actions' working directory).

Workspace convenience symlinks, created only if the workspace root is writable (Bazel itself does not use them): `bazel-<workspace>` (execroot), `bazel-out`, `bazel-bin`, `bazel-testlogs`.

Move things with startup options:

```bash
bazel --output_base=/tmp/bazel/output build x/y:z
bazel --output_user_root=/tmp/bazel build x/y:z
```

`--output_user_root` relocates both the install base and output base.

Bazel must be invoked inside a repository (a directory with a repository boundary file, or a subdirectory of one); otherwise it reports an error.

## Checked

2026-11-04. Read against the Bazel docs page(s): Output Directory Layout (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the .gitignore advice, the MODULE.bazel boundary-file example, the bazel info advice and the closing Verify line.
Method: documentation only; no commands were run.
