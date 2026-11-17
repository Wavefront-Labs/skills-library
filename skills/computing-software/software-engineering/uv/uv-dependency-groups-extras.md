---
id: computing-software.software-engineering.uv.uv-dependency-groups-extras
name: uv-dependency-groups-extras
category: computing-software
field: software-engineering
product: uv
tags: [uv, dependency-groups, extras, optional-dependencies, dev-dependencies, default-groups, pep-735, python]
level: practitioner
status: docs-checked
description: "Use optional extras and PEP 735 dependency groups in uv: add with flags, nest with include-group, set default groups, give groups their own requires-python."
sources: [https://docs.astral.sh/uv/concepts/projects/dependencies/, https://docs.astral.sh/uv/concepts/projects/sync/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extras and dependency groups

Goal: separate published optional features (extras) from local-only development groups.

## Method

Extras live in `[project.optional-dependencies]` and are published; request them as `pandas[plot, excel]`. Add one: `uv add httpx --optional network`. Sources can be tied to an extra with `extra = "cpu"` in `tool.uv.sources`. Sync them with `uv sync --extra foo` or `--all-extras` (not synced by default).

Groups live in `[dependency-groups]` (PEP 735), are local-only and not in the published requirements.

- `uv add --dev pytest` creates group `dev`; `uv add --group lint ruff` creates `lint`.
- `dev` is special: flags `--dev`, `--only-dev`, `--no-dev` equal `--group dev`, `--only-group dev`, `--no-group dev`.
- General flags: `--all-groups`, `--no-default-groups`, `--group`, `--only-group`, `--no-group`. `--only-group` omits the project itself and the default groups. Exclusion beats inclusion: `uv sync --no-group foo --group foo` skips `foo`.
- Nest groups:

```toml
[dependency-groups]
dev = [{include-group = "lint"}, {include-group = "test"}]
lint = ["ruff"]
test = ["pytest"]
```

- Default groups: `dev` is synced by default (`uv run`, `uv sync`). Change with `[tool.uv] default-groups = ["dev", "foo"]` or `default-groups = "all"`.
- Per-group Python range:

```toml
[tool.uv.dependency-groups]
dev = {requires-python = ">=3.12"}
```

## Gotchas

- All groups are resolved together into the lockfile and must be mutually compatible; conflicting extras also fail resolution. Genuinely conflicting extras or groups must be declared as conflicting (see the project config docs) or resolution fails.
- Groups must fit the project `requires-python` unless overridden as above. Included groups cannot conflict with others in the group.
- Legacy `tool.uv.dev-dependencies` is merged with `dependency-groups.dev`; if it exists, `uv add --dev` writes there.
- Groups are a recent standard; not all tools support them.

## Verify

After `uv add --group lint ruff`, `[dependency-groups]` contains `lint = ["ruff"]`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/dependencies; concepts/projects/sync). Removed or changed: reworded the conflicting extras/groups sentence to match the page.

Method: documentation only; no commands were run.
