---
id: computing-software.software-engineering.python.safe-zipfile-and-tarfile-extraction
name: safe-zipfile-and-tarfile-extraction
category: computing-software
field: software-engineering
product: python
tags: [python, py-archives-crypto, zipfile-tarfile-safety, zipfile, tarfile, zip-slip, zip-bomb, extraction-filter, path-traversal]
level: practitioner
status: docs-checked
description: "Read and extract zip and tar archives defensively: extraction filters, path traversal checks, size and ratio limits, symlink handling and streaming reads."
sources: ["https://docs.python.org/3/library/tarfile.html#extraction-filters", "https://docs.python.org/3/library/zipfile.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe zipfile and tarfile extraction

## tarfile with filters
```python
import tarfile
with tarfile.open("upload.tar.gz") as tf:
    tf.extractall("work/", filter="data")      # refuses links to absolute or outside paths and device files, strips unsafe permissions
```
Filter availability: added in 3.12, and may be backported to older versions as security updates, so test `hasattr(tarfile, "data_filter")` rather than the version number. **Python 3.14 makes `"data"` the default**; before that the default behaved like `"fully_trusted"`. The docs recommend passing `filter="data"` explicitly to support versions with the less secure default.
No filter blocks every dangerous feature: the docs say never to extract archives from untrusted sources without prior inspection, and the destination directory must not be modified by an attacker during extraction.
Custom filter: a callable taking `(member, path)` and returning the (possibly modified) member; `raise` to abort.

## zipfile
```python
import zipfile, pathlib
MAX_TOTAL, MAX_RATIO = 500 * 2**20, 100
dest = pathlib.Path("work").resolve()
with zipfile.ZipFile("upload.zip") as zf:
    total = 0
    for info in zf.infolist():
        total += info.file_size
        if total > MAX_TOTAL or (info.compress_size and info.file_size / info.compress_size > MAX_RATIO):
            raise ValueError("zip bomb suspected")
        target = (dest / info.filename).resolve()
        if not target.is_relative_to(dest):          # zip-slip check
            raise ValueError(f"unsafe path {info.filename}")
    zf.extractall(dest)
```
`ZipFile.extract` strips drive/UNC parts, leading slashes and `..` components from member names, but explicit checks keep behaviour clear and testable. Declared sizes can lie: also enforce limits while streaming (`zf.open(info)` and count bytes read).

## Rules
- Extract into a new empty temp directory, not into a live tree; validate, then move.
- Do not trust names: reject NUL bytes, drive letters (`C:`), backslashes meant as traversal on Windows, and duplicate entries.
- Limit entry count (millions of tiny files exhaust inodes).
- `zipfile` can decrypt encrypted members (`pwd=`) but cannot create encrypted files, and decryption is very slow (pure Python).

## Gotchas
- Symlinks in tar can point outside; the `data` filter refuses links to absolute paths or outside the destination (`tar` does not limit link targets).
- Reading a member with `.read()` loads it all in memory; stream in chunks.
- Compressed tar archives can also expand hugely; the tarfile docs do not give a limit, so wrap reads with a byte counter.

## Verify
- [ ] Test archives containing `../evil`, an absolute path, a symlink to `/etc`, and a 1000:1 compressed file are all rejected.

## Checked

- 2026-11-03: checked against the CPython docs `library/tarfile.rst` (extraction filters, 3.12 and 3.14 changes, `hasattr(tarfile, 'data_filter')`, data filter behaviour, untrusted-source warning) and `library/zipfile.rst` (`ZipFile.extract` name sanitising, decryption only and slow).
- Removed: backport version list, the DeprecationWarning claim for 3.12-3.13, the weak-ZipCrypto claim. The size and ratio limits in the example are illustrative thresholds, not documented values; the Rules section is defensive advice, not documented behaviour.

Method: documentation only; no commands were run.
