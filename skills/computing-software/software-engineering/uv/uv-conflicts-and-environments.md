---
id: computing-software.software-engineering.uv.uv-conflicts-and-environments
name: uv-conflicts-and-environments
category: computing-software
field: software-engineering
product: uv
tags: [uv, conflicts, environments, required-environments, markers, extras, dependency-groups, python]
level: practitioner
status: docs-checked
description: "Declare conflicting extras or groups with tool.uv.conflicts and narrow or require platforms with tool.uv.environments and required-environments in uv."
sources: [https://docs.astral.sh/uv/concepts/projects/config/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conflicts and resolution environments

Goal: make the lockfile solve for the platforms you support and allow mutually incompatible extras or groups.

## Method

uv resolves all dependencies, extras and groups together; incompatible sections make resolution fail. Declare known conflicts in `[tool.uv]`:

```toml
[tool.uv]
conflicts = [
    [
      { extra = "extra1" },
      { extra = "extra2" },
    ],
]
```

Use `{ group = "group1" }` and `{ group = "group2" }` for dependency groups.

Limit solved platforms with PEP 508 markers in `environments`:

```toml
[tool.uv]
environments = [
    "sys_platform == 'darwin'",
    "sys_platform == 'linux'",
]
```

This constrains the lockfile to macOS and Linux and excludes Windows.

Require a platform with `required-environments`:

```toml
[tool.uv]
required-environments = [
    "sys_platform == 'darwin' and platform_machine == 'x86_64'",
]
```

This matters for packages that publish no source distribution (such as PyTorch): they install only where pre-built wheels exist, so resolution must cover the required environment. For Linux, use `minimum-libc-version` alongside `required-environments` to choose libc implementations and minimum versions.

## Gotchas

- Without a `conflicts` declaration, conflicting extras or groups fail resolution.
- The project config page links to the resolution docs for the full semantics of these settings.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/config). Removed or changed: removed an invented Verify section; reworded the resolution-docs gotcha to what the page states.

Method: documentation only; no commands were run.
