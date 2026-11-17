---
id: computing-software.devops-ci-cd.bazel.bazel-module-version-selection-and-overrides
name: bazel-module-version-selection-and-overrides
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bzlmod, module-bazel, minimal-version-selection, single-version-override, multiple-version-override, local-path-override, yanked-versions, inject-module]
level: advanced
status: docs-checked
description: "Understand how Bazel picks module versions (MVS), pin or patch with overrides, and handle yanked versions."
sources: ["https://bazel.build/external/module"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel module version selection and overrides

A module is a Bazel project with a `MODULE.bazel` at its root:

```
module(name = "my-module", version = "1.0")
bazel_dep(name = "rules_cc", version = "0.0.1")
```

Bazel reads the root `MODULE.bazel`, fetches each dependency's `MODULE.bazel` from a registry until the graph is known, then selects one version per module using Minimal Version Selection (from Go modules): the highest version requested by any dependent, never a newer one that nobody asked for. Versions are relaxed SemVer: any number of release segments, letters allowed.

Yanked versions: selecting one is an error. Upgrade, or pass `--allow_yanked_versions` (or env `BZLMOD_ALLOW_YANKED_VERSIONS`).

Overrides only count in the root module; dependencies' overrides are ignored.
- `single_version_override`: pin `version`, force a `registry`, apply `patches`.
- `multiple_version_override`: allow several versions to coexist; each dependent gets the nearest allowed higher version. Allowing a version not present in the graph is an error.
- Non-registry: `archive_override`, `git_override`, `local_path_override` remove the module from resolution and read its `MODULE.bazel` from the source.
- CLI: `--override_module` swaps in a local directory; `--inject_module` adds a module as if via `bazel_dep` plus `local_path_override`, honouring its toolchains and execution platforms. Both may touch `MODULE.bazel.lock`; use `--lockfile_mode=update` if needed.

Strict deps: a module sees only its direct dependencies by apparent name (override with `repo_name`). Canonical names look like `bazel_skylib+1.0.3` and are not an API; use `Label.repo_name`, `$(rlocationpath ...)`, or `bazel mod dump_repo_mapping`.

## Checked

2026-11-04. Read against the Bazel docs page(s): Bazel modules (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line.
Method: documentation only; no commands were run.
