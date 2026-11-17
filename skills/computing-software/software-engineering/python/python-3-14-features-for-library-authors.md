---
id: computing-software.software-engineering.python.python-3-14-features-for-library-authors
name: python-3-14-features-for-library-authors
category: computing-software
field: software-engineering
product: python
tags: [python, py-versions, python-314-features, t-strings, deferred-annotations, free-threading, zstd, pep-750, migration]
level: practitioner
status: docs-checked
description: "What Python 3.14 changes that affect library code: t-strings, deferred annotations, compression.zstd, free-threaded support, remote pdb attach and syntax changes."
sources: ["https://docs.python.org/3.14/whatsnew/3.14.html", "https://peps.python.org/pep-0750/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python 3.14 features for library authors

Confirm against the official What's New page for your exact patch release. Main items:

| Feature | PEP / docs | What to do |
|---|---|---|
| **Template strings** `t'Try some {variety} cheese!'` | PEP 750, `string.templatelib` | A t-string evaluates to a `string.templatelib.Template`, not a `str`; iterating it yields static strings and `Interpolation` objects, so libraries can process interpolations before combining. |
| **Deferred annotation evaluation** | PEP 649/749, `annotationlib` | Use `annotationlib.get_annotations(obj, format=Format.VALUE / FORWARDREF / STRING)`. `FORWARDREF` replaces undefined names with markers; `VALUE` raises `NameError` for them. See the What's New porting section. |
| **Free-threaded Python officially supported** | PEP 779 | The free-threaded mode got significant improvements. On Windows, extension modules for the free-threaded build now need `Py_GIL_DISABLED` defined by the build backend. |
| **Multiple interpreters** | PEP 734, `concurrent.interpreters` | New stdlib module. |
| **`compression.zstd`** | PEP 784 | Zstandard via `from compression import zstd` (`zstd.compress`). Zstandard support was added to `tarfile`, `zipfile` and `shutil`. The `compression` package also re-exports `lzma`, `bz2`, `gzip`, `zlib` as `compression.*`; the old names are not deprecated. |
| **Safe external debugger interface** | PEP 768, `sys.remote_exec()`, `python -m pdb -p PID` | Attach to a running process. Disable with the `PYTHON_DISABLE_REMOTE_DEBUG` environment variable, `-X disable-remote-debug`, or build with `--without-remote-debug`. |
| **`except` without brackets** | PEP 758 | `except TimeoutError, ConnectionRefusedError:` is allowed when there is no `as` clause. |
| **Control flow in `finally`** | PEP 765 | A `return`, `break` or `continue` that leaves a `finally` block now emits `SyntaxWarning`. |
| **pickle** | docs | Default pickle protocol is now 5. |
| **Garbage collector** | docs | An incremental GC shipped in 3.14.0 to 3.14.4 but was reverted to the 3.13 generational GC from 3.14.5 onward. |
| **`uuid`, `functools.Placeholder`** | docs | `uuid6()`, `uuid7()`, `uuid8()` (RFC 9562); `functools.Placeholder` for `partial()`. |
| **`tarfile`** | docs | `data_filter()` now normalizes symlink targets; extraction filters are re-applied when links are replaced by copies, which can raise the new `LinkFallbackError`. |

## Support strategy
1. Add 3.14 (and the free-threaded build) to the test matrix before declaring support.
2. Rebuild native extensions for 3.14; free-threaded builds are a separate build.
3. Do not rely on features while they are described as changing; check the What's New page and PEPs.

## Verify
- [ ] The test suite passes on 3.14 with no new warnings.

## Checked
Date: 2026-11-03. Confirmed against "What's New in Python 3.14": t-strings, `annotationlib` formats, free-threaded notes, `compression`/`compression.zstd`, PEP 768 options and `pdb -p`, PEP 758, PEP 765, pickle protocol 5, the GC revert note, uuid, `functools.Placeholder`, tarfile changes. Removed as unconfirmed or wrong: incremental GC as a current feature, `cp314t` wheel tag and `Py_mod_gil` advice, `PYTHON_GIL=0`, `tarfile` default filter claim, argparse and strptime items, CI tooling advice (cibuildwheel, abi3), classifier advice, PEP 810/686 (3.15) claims and tool-lag remarks.
Method: documentation only; no commands were run.
