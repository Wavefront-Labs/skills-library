---
id: computing-software.software-engineering.uv.uv-resolver-internals
name: uv-resolver-internals
category: computing-software
field: software-engineering
product: uv
tags: [uv, resolver, pubgrub, forking, markers, requires-python, wheel-tags, prioritization]
level: advanced
status: docs-checked
description: "How uv's PubGrub resolver picks versions, forks on markers, handles requires-python bounds and URL dependencies, and prioritises packages."
sources: [https://docs.astral.sh/uv/reference/internals/resolver/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv resolver internals

Goal: predict and debug uv resolutions from how the resolver works.

## Method

uv uses pubgrub-rs. Loop: take the highest-priority undecided package, pick a version compatible with the partial solution (preferring versions from `uv.lock` or `-o requirements.txt` and from the current environment, checking highest to lowest unless another resolution strategy is set), add its requirements, prefetch their metadata, and backtrack on conflict by recording incompatibilities. Failure produces an error built from incompatibilities including the virtual root package. An extra heuristic swaps the order of two packages that conflict too much.

### Prioritization

Order: root and URL requirements, then singleton `==` requirements, then highly conflicting packages, then the rest; within each, first-seen order (breadth first, so direct and workspace dependencies precede transitive ones). After five conflicts between A and B (B only works with old A), both get highly-conflicting priority with B decided before A.

### Forking

Requirements with different markers split the resolution, for example `numpy>=2,<3 ; python_version >= "3.11"` and `numpy>=1.16,<2 ; python_version < "3.11"`. Overlapping or incomplete markers cause extra forks (`flask` with darwin and win32 markers gives three). Forks nest and identical ones merge. Observe with `uv lock -v`: look for `Splitting resolution on ...`, `Solving split ...`, `Split ... resolution took ...`. The lockfile stores `resolution-markers` so later resolutions stay stable.

### Wheel tags and metadata

Resolution is universal over markers but not wheel tags, so a package such as `torch` with no sdist and no matching wheel fails on unsupported platforms. uv assumes all wheels of one version on an index have identical `METADATA` (and an sdist builds to the same metadata), which avoids one request per wheel and keeps markers and wheel tags from needing two dimensions. For packages built against a specific torch, `tool.uv.extra-build-dependencies` with `match-runtime = true` builds per installed version.

### requires-python

All selected dependency versions must support the project's whole `requires-python` range, so a dependency requiring `>=3.10` is rejected for a project with `>=3.9`. Upper bounds on dependencies are ignored. When a newer-Python-only version is rejected, uv forks on that Python version (control with `--fork-strategy`), giving for numpy `numpy==2.0.0` below 3.10 and `numpy==2.1.0` from 3.10. A project upper bound like `==3.13.*` only prunes out-of-range wheels from the lockfile afterwards.

### URL dependencies

`name @ url` and `git`, `url`, `path`, `workspace` sources pin the package to that URL and its implied version. Conflicting URLs error; multiple URLs need flat indexes. URLs must be declared directly (project, workspace member, constraint, override) or by other URL dependencies; index packages may not declare URLs.

## Gotchas

Bumping a project's upper Python bound makes it compatible with fewer dependency versions and can fail to resolve when no version of a dependency supports the required range; bumping the lower bound only increases the set of supported dependency versions.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (reference/internals/resolver). Removed or changed: rewrote a garbled gotcha about requires-python bounds to the page statement.

Method: documentation only; no commands were run.
