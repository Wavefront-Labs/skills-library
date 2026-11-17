---
id: computing-software.software-engineering.python.tempfile-and-shutil-file-operations
name: tempfile-and-shutil-file-operations
category: computing-software
field: software-engineering
product: python
tags: [python, tempfile, shutil, atomic-write, copytree, rmtree, python-stdlib]
level: practitioner
status: verified
description: "Handle temp files and bulk file operations safely: TemporaryDirectory and NamedTemporaryFile pitfalls, atomic writes with os.replace, shutil copy/move/rmtree and disk usage."
sources: ["https://docs.python.org/3/library/tempfile.html", "https://docs.python.org/3/library/shutil.html", "https://docs.python.org/3/library/os.html#os.replace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tempfile and shutil file operations

**Goal:** scratch files that always get cleaned up, writes that never leave a
half-written file, and tree operations that behave the same on Linux and Windows.

## Temporary files and directories
```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory(prefix="build-") as tmp:     # removed on exit, even on error
    work = Path(tmp)
    (work / "out.txt").write_text("...")

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    f.write(payload); path = f.name
# ...use path, then os.unlink(path)
```
- Never build names like `/tmp/myapp.txt` yourself (races, symlink attacks, collisions);
  `mkstemp`/`NamedTemporaryFile` create files atomically (mode 0600 on POSIX; Windows has no such bits).
- Windows: a `NamedTemporaryFile(delete=True)` cannot be reopened by name while open. On 3.12+
  use `delete_on_close=False` (file deleted at context exit, not on close).
- `SpooledTemporaryFile(max_size=10_000_000)` keeps small data in memory, spills to disk.
- `TMPDIR` env var (or `tempfile.tempdir`) controls location; containers may mount a small tmpfs.

## Atomic writes
```python
import os
def atomic_write(path: Path, data: bytes):
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)          # atomic on same filesystem, overwrites on Windows too
    except BaseException:
        os.unlink(tmp); raise
```
Temp file must be in the same directory (same filesystem) for the rename to be atomic.
`os.rename` fails on Windows if the target exists; `os.replace` doesn't.

## shutil essentials
```python
import shutil
shutil.copy2(src, dst)                         # data + metadata (mtime)
shutil.copytree(src, dst, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".git"))
shutil.move(src, dst)                          # rename or copy+delete across filesystems
shutil.rmtree(path, onexc=handler)             # 3.12+: onexc replaces onerror
shutil.make_archive("dist/site", "zip", root_dir="build/site")
shutil.disk_usage("/").free
shutil.which("ffmpeg")                         # locate executables on PATH
```
Read-only files (Windows, `.git` objects) make rmtree fail:
```python
import stat
def handler(func, p, exc):
    os.chmod(p, stat.S_IWRITE); func(p)
```

## Gotchas
- `copytree` follows symlinks into copies unless `symlinks=True`.
- `shutil.move` into an existing directory moves *inside* it.
- `rmtree` on a user-supplied path: resolve and check it is under an expected root first.

## Verify
- [ ] No hand-built temp paths; grep for `"/tmp/` in code.
- [ ] Killing the process mid-write leaves either the old or the new file, never a truncated one.

## Checked
- Python 3.14.0 on Windows: `TemporaryDirectory` is removed even when the body raises; `NamedTemporaryFile(delete=False)` leaves the file; reopening a `delete=True` file by name while open raises `PermissionError`, and `delete_on_close=False` allows reopening after `close()` then deletes at exit; `SpooledTemporaryFile` rolls to disk past `max_size`; the `atomic_write` helper replaces the file and leaves no `.tmp`; `os.rename` onto an existing file raises `FileExistsError` where `os.replace` succeeds; `copytree(dirs_exist_ok=True, ignore=...)` merged and skipped `*.pyc`, `__pycache__`, `.git`, a plain second `copytree` raises `FileExistsError`; `copy2` kept the mtime; `move` into an existing directory moved inside it; `rmtree` on a read-only file fails with `PermissionError` and the `onexc` handler fixes it; `make_archive`, `disk_usage`, `which`. `mkstemp` showed mode `0o666` because Windows ignores POSIX permission bits (the 0600 guarantee applies on POSIX). `copytree(symlinks=...)` needs symlink privileges and was not run.
