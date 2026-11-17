---
id: computing-software.software-engineering.python.files-and-paths-with-pathlib
name: files-and-paths-with-pathlib
category: computing-software
field: software-engineering
product: python
tags: [python, python-stdlib, pathlib, file-io, encoding, glob, atomic-write]
level: practitioner
status: verified
description: "Handle files and paths with pathlib: joining, globbing, reading/writing with explicit encodings, atomic replace, temp dirs and cross-platform pitfalls."
sources:
  - https://docs.python.org/3/library/pathlib.html
  - https://docs.python.org/3/library/os.html#os.replace
  - https://docs.python.org/3/library/tempfile.html
  - https://peps.python.org/pep-0686/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Files and paths with pathlib

**Goal:** path code that works on Windows, macOS and Linux and never corrupts files on crash.

## 1. Building and inspecting paths
```python
from pathlib import Path
root = Path(__file__).resolve().parent        # directory of this module
cfg = root / "config" / "app.toml"
cfg.name, cfg.stem, cfg.suffix, cfg.parent    # 'app.toml', 'app', '.toml', .../config
cfg.with_suffix(".bak"), cfg.with_name("x.toml")
cfg.relative_to(root)                          # ValueError if not under root
Path.home() / ".cache" / "myapp"
```
Never build paths with string concatenation or `"\\"`; `/` handles separators.

## 2. Reading and writing
```python
text = cfg.read_text(encoding="utf-8")
cfg.write_text(data, encoding="utf-8", newline="\n")    # newline= added in 3.10; the default writes CRLF on Windows
raw = img.read_bytes()
with cfg.open("a", encoding="utf-8") as f: f.write(line)
```
Always pass `encoding="utf-8"`: the default is the locale encoding (cp1252 on many Windows machines) until UTF-8 mode becomes default (PEP 686, 3.15). `python -X warn_default_encoding` finds missing ones.

## 3. Directories and globbing
```python
out = Path("build/reports"); out.mkdir(parents=True, exist_ok=True)
for p in Path("src").rglob("*.py"): ...          # recursive
sorted(Path("logs").glob("*.log"), key=lambda p: p.stat().st_mtime)
for dirpath, dirnames, filenames in Path("data").walk():   # 3.12+
    dirnames[:] = [d for d in dirnames if d != ".git"]     # prune in place
```

## 4. Atomic writes
```python
import os, tempfile
def atomic_write(path: Path, data: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)        # atomic on the same filesystem, overwrites on Windows too
    except BaseException:
        os.unlink(tmp); raise
```
Temp file must be in the same directory (same filesystem) for `replace` to be atomic.

## 5. Deleting and copying
`p.unlink(missing_ok=True)`, `p.rmdir()` (empty only), `shutil.rmtree(p)`, `shutil.copy2(src, dst)` (keeps metadata), `shutil.move`. `tempfile.TemporaryDirectory()` as a context manager for scratch space.

## Gotchas
- `Path("a") / "/b"` gives `/b`: an absolute right-hand side discards the left. Validate user-supplied names (`Path(name).name == name`) to prevent traversal; check `resolved.is_relative_to(base)` after `resolve()`.
- `exists()` then `open()` is racy; just open and handle `FileNotFoundError`/`FileExistsError` (`open(p, "x")` for create-only).
- Windows: max path 260 unless long paths enabled; reserved names (`CON`, `NUL`); case-insensitive comparisons.
- `glob` ordering is arbitrary; sort for reproducibility.

## Verify
- Tests run on Windows and Linux CI; kill the process mid-write (or inject an exception) and confirm the target file is either old or new, never truncated.

## Checked
- Python 3.14.0 on Windows: name/stem/suffix/with_suffix/with_name, relative_to raising ValueError, Path.walk() with in-place pruning (3.12+), rglob, write_text with newline set to LF writing LF and the default writing CRLF, the default encoding being cp1252 (one byte for e-acute) versus UTF-8, open(p, "x") raising FileExistsError, unlink(missing_ok=True), rmdir on a non-empty directory failing, the atomic_write helper replacing the file and leaving no .tmp, an absolute right-hand side replacing the left in PurePosixPath; PEP 686 targets 3.15 for UTF-8 by default. The 260-character and reserved-name notes are Windows documentation, not re-tested.
