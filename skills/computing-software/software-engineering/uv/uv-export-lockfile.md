---
id: computing-software.software-engineering.uv.uv-export-lockfile
name: uv-export-lockfile
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-export, requirements-export, pylock, cyclonedx, sbom, lockfile, python]
level: practitioner
status: docs-checked
description: "Export uv.lock to requirements.txt, pylock.toml or a CycloneDX 1.5 SBOM with uv export --format and --output-file, and know the path and preview caveats."
sources: [https://docs.astral.sh/uv/concepts/projects/export/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting a lockfile

Goal: hand the locked dependency set to tools that cannot read `uv.lock`.

## Method

Pick the format with `--format`:

```console
$ uv export --format requirements.txt
$ uv export --format pylock.toml
$ uv export --format cyclonedx1.5
```

- Output goes to stdout by default. Write a file with `--output-file`:

```console
$ uv export --format requirements.txt --output-file requirements.txt
$ uv export --format pylock.toml --output-file pylock.toml
$ uv export --format cyclonedx1.5 --output-file sbom.json
```

- `requirements.txt`: pip-compatible, installable via `uv pip install` or `pip`.
- `pylock.toml`: the PEP 751 standard lock format. Relative local paths are written relative to the output file's directory; on stdout they are relative to the current working directory. Use `--output-file` when writing into another directory.
- `cyclonedx1.5`: a JSON CycloneDX v1.5 SBOM of the project and all dependencies, for security auditing and compliance. uv adds custom component properties `uv:package:marker` (environment markers) and `uv:workspace:path` (relative path of workspace members).

## Gotchas

- CycloneDX export is in preview and may change in any release.
- uv recommends not keeping both `uv.lock` and `requirements.txt`: `uv.lock` expresses features that `requirements.txt` cannot.

## Verify

`uv export --format cyclonedx1.5 --output-file sbom.json` writes a JSON document.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/export). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
