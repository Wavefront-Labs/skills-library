---
id: computing-software.software-engineering.python.archives-with-shutil-make-archive-and-unpack
name: archives-with-shutil-make-archive-and-unpack
category: computing-software
field: software-engineering
product: python
tags: [python, py-os, shutil-archives, shutil, make-archive, unpack-archive, zip, tar, extraction-filter]
level: practitioner
status: docs-checked
description: "Create and extract zip and tar archives with shutil.make_archive and unpack_archive, apply tar extraction filters and set root_dir and base_dir."
sources: ["https://docs.python.org/3/library/shutil.html#archiving-operations", "https://docs.python.org/3/library/shutil.html#shutil.unpack_archive"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Archives with shutil

```python
import shutil

# Create dist/app-1.0.zip containing app-1.0/...
shutil.make_archive("dist/app-1.0", "zip", root_dir="build", base_dir="app-1.0")
shutil.make_archive("dist/app", "gztar", root_dir="build")        # also "tar", "bztar", "xztar", "zip" ("zstdtar" in newer versions)
shutil.get_archive_formats(); shutil.get_unpack_formats()

# Extract; format guessed from the extension
shutil.unpack_archive("dist/app.tar.gz", extract_dir="out", filter="data")
```

## Safe extraction (important)
Archives can carry `../../etc/x` paths, absolute paths, symlinks and device files.
- The `filter` argument for tar files was added in 3.12 (and may be backported to older versions as security updates); `"data"` is the default since **3.14**. The docs recommend `filter="data"` unless you need tar/UNIX-specific features, and say to pass it explicitly to support versions with the less secure default (3.13 and lower). `"data"` refuses links to absolute paths or outside the destination and device files, and strips unsafe permission bits. `"tar"` honours most tar features but does not limit symlink targets; `"fully_trusted"` honours all metadata.
- No filter blocks every dangerous feature: the tarfile docs say never to extract archives from untrusted sources without prior inspection.
- For zip files `filter` is not accepted. `ZipFile.extract` strips leading slashes, drive/UNC parts and `..` components from member names, but nothing limits expanded size (zip bombs): check `ZipInfo.file_size` totals before extracting.
- Extract into a fresh temp directory, then move.

## Details
- `root_dir` is the directory you chdir to for the archive; `base_dir` is the top-level folder inside the archive (relative to `root_dir`). Mixing them up creates archives with absolute-looking trees.
- `make_archive` was made thread-safe for the standard zip and tar formats in 3.10.6; a custom archiver registered with `register_archive_format` that lacks `supports_root_dir = True` still makes it change the process working directory, so it is not thread-safe then.
- Since 3.8 `format="tar"` uses the pax (POSIX.1-2001) format.
- Custom formats: `shutil.register_archive_format`.

## Gotchas
- Return value of `make_archive` is the archive path, including the extension it adds; do not append `.zip` yourself.

## Verify
- [ ] Round-trip: unpack into a temp dir and compare tree listing/hashes with the source.
- [ ] A malicious test archive containing `../evil.txt` is rejected (`tarfile.OutsideDestinationError`).

## Checked

- 2026-11-03: checked against the CPython docs `library/shutil.rst` and `library/tarfile.rst`: make_archive formats, root_dir/base_dir, thread-safety note (3.10.6), pax tar format (3.8), unpack_archive `filter` (not accepted for zip), tar filter names and 3.12/3.14 history, `ZipFile.extract` name sanitising (zipfile.rst).
- Removed: the backport version list (3.8.17 etc.) and the 3.11 thread-safety claim (not in the docs), the claim that make_archive embeds timestamps and the reproducible-archive recipe, and the zip-versus-tar symlink claim.

Method: documentation only; no commands were run.
