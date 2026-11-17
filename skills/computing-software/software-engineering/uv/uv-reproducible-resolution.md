---
id: computing-software.software-engineering.uv.uv-reproducible-resolution
name: uv-reproducible-resolution
category: computing-software
field: software-engineering
product: uv
tags: [uv, exclude-newer, reproducible, cooldown, resolution, lockfile, upload-time]
level: practitioner
status: docs-checked
description: "Make uv resolutions reproducible or delayed with exclude-newer dates, durations and per-package or per-index cutoffs, plus lockfile schema versioning."
sources: [https://docs.astral.sh/uv/concepts/resolution/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv reproducible resolution and cooldowns

Goal: ignore newer uploads, either at a fixed date or a rolling delay.

## Method

- `--exclude-newer <value>` limits resolution to distributions uploaded before the value. It compares each file's upload time, not the version's release date. Accepts an RFC 3339 timestamp (`2006-12-02T02:07:43Z`) or a local date (`2006-12-02`, system time zone).
- Config: `exclude-newer = "2006-12-02T02:07:43Z"` under `[tool.uv]`. Persistent config cannot use local date times.
- Disable a lower-priority cutoff: `--exclude-newer false`, `UV_EXCLUDE_NEWER=false`, or `exclude-newer = false` in a higher-priority config.
- Per package: `--exclude-newer-package setuptools=2006-12-02`, or `exclude-newer-package = { setuptools = "2006-12-02T02:07:43Z" }`; `setuptools=false` opts it out. Package values beat global and index values.
- Per index:

```toml
[[tool.uv.index]]
name = "internal"
url = "https://internal.example.com/simple"
exclude-newer = "7 days"
```

`exclude-newer = false` disables it for that index.

- Cooldowns: give a duration instead of a date, friendly (`24 hours`, `1 week`, `30 days`) or ISO 8601 (`PT24H`, `P7D`, `P30D`). Months and years are not allowed; a day is always 24 hours. Example: `exclude-newer = "1 week"` plus `exclude-newer-package = { setuptools = "30 days" }`.
- With `uv.lock`, the computed timestamp is stored in the lockfile and not refreshed as time passes; it updates on new resolution such as `--upgrade` or `--refresh`.

## Gotchas

- The index must provide PEP 700 `upload-time`; otherwise files count as unavailable unless opted out (`--exclude-newer-package <package>=false`, or index-level exclude-newer). PyPI provides it.
- Error messages do not mention that files were excluded.
- Applies to registry packages only, not Git. In `uv pip`, installed packages are not downgraded unless `--reinstall`.
- Since 0.12 uv rejects source distributions that violate PEP 625 extensions, except `.zip`.
- Lockfile schema `version`: a uv version reads/writes its own schema and rejects greater ones; bumped only in minor releases. `revision` tracks backward-compatible changes and never causes older uv to error.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/resolution). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
