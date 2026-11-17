---
id: computing-software.software-engineering.nim.os-file-and-directory-operations
name: os-file-and-directory-operations
category: computing-software
field: software-engineering
product: nim
tags: [os-file-and-directory-operations, stdlib-os-and-paths, os, walkdir, walkdirrec, createdir, copyfile, removefile, fileexists, getenv, getcurrentdir, nim]
level: practitioner
status: docs-checked
description: "List, create, copy, move and delete files and dirs, walk trees, inspect info, and read environment variables."
sources:
  - https://nim-lang.org/docs/os.html
  - https://nim-lang.org/docs/paths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File and directory operations with os

Goal: manipulate the filesystem portably.

- Paths: `joinPath(a, b)` or `a / b`, `splitFile(p)` -> (dir, name, ext), `extractFilename`, `parentDir`, `changeFileExt`, `absolutePath`, `normalizedPath`, `relativePath`.
- Queries: `fileExists`, `dirExists`, `getFileSize`, `getLastModificationTime`, `getFilePermissions`.
- Ops: `createDir` (creates the full path, does not fail if it exists), `copyFile`, `copyDir`, `moveFile`, `removeFile`, `removeDir`, `setCurrentDir`.
- Walk: `for kind, p in walkDir(dir)`, `walkDirRec(dir, {pcFile})`, `walkPattern("*.nim")`.
- Env/args: `getEnv("HOME")`, `putEnv`, `paramCount()`, `paramStr(i)`, `getAppDir()`, `getHomeDir()`, `getTempDir()`.
- `std/paths` (with `std/dirs`, `std/files`, `std/envvars`, `std/cmdline`, `std/appdirs`) is the typed-`Path` API in the standard library source.

Gotchas:
- Failures raise `OSError` (for example `createDir`).
- `walkDirRec` yields files by default (`yieldFilter = {pcFile}`) and follows directories (`followFilter = {pcDir}`).

Verify: walkDirRec lists files and `removeDir` cleans the temp tree.

## Checked

2026-11-02. Confirmed against lib/pure/os.nim and lib/std/private/ospaths2.nim, osfiles.nim, osdirs.nim, osappdirs.nim, oscommon.nim (every listed proc exists; `createDir`, `walkDirRec` signatures), lib/std/envvars.nim and cmdline.nim (`getEnv`, `paramStr`, `paramCount`). Removed: the DirSep gotcha. Not checked: `getAppDir`/`getHomeDir`/`getTempDir` platform behaviour.
Method: documentation only; no commands were run.
