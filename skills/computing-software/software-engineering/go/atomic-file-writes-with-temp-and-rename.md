---
id: computing-software.software-engineering.go.atomic-file-writes-with-temp-and-rename
name: atomic-file-writes-with-temp-and-rename
category: computing-software
field: software-engineering
product: go
tags: [go, go-io-files, go-atomic-file-write, atomic-write, rename, fsync]
level: practitioner
status: docs-checked
description: "Write files crash-safely in Go: temp file in the same directory, sync, close, rename, and directory sync."
sources:
  - https://pkg.go.dev/os#Rename
  - https://pkg.go.dev/os#File.Sync
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atomic file writes

**Goal:** readers see either the old file or the new one, never a half-written one.

```go
func WriteFileAtomic(path string, data []byte, perm os.FileMode) error {
    dir := filepath.Dir(path)
    tmp, err := os.CreateTemp(dir, ".tmp-"+filepath.Base(path)+"-*")
    if err != nil { return err }
    defer os.Remove(tmp.Name())              // no-op after successful rename
    if _, err := tmp.Write(data); err != nil { tmp.Close(); return err }
    if err := tmp.Chmod(perm); err != nil { tmp.Close(); return err }
    if err := tmp.Sync(); err != nil { tmp.Close(); return err } // flush data to disk
    if err := tmp.Close(); err != nil { return err }
    if err := os.Rename(tmp.Name(), path); err != nil { return err }
    d, err := os.Open(dir)                    // persist the rename (POSIX)
    if err == nil { d.Sync(); d.Close() }
    return nil
}
```

Keep the temp file in the same directory as the destination so the rename stays within one directory. `os.Rename` replaces an existing non-directory `newpath`, returns an error if `newpath` is a directory, and may have OS-specific restrictions when the paths are in different directories. The docs also say that on non-Unix platforms Rename is not an atomic operation, even within one directory, so the atomic guarantee above holds only where the platform provides it.

`File.Sync` commits the file's current contents to stable storage, typically by flushing the file system's in-memory copy to disk.

## Gotchas
- `os.WriteFile` truncates an existing file before writing and, per its docs, a failure mid-operation can leave the file partially written. It is not atomic.
- Set the mode explicitly with `Chmod` as in the example; on Windows only the 0o200 bit of a mode is used.
- The directory open and `Sync` at the end is a best-effort step in this recipe; ignore its error rather than failing a write that already succeeded.

## Verify
Run the function in a subprocess, interrupt it at random points and assert the target file is always either the old or the new content.

## Checked
2026-11-03. Confirmed on pkg.go.dev/os: `Rename` replacement rules and the non-atomic-on-non-Unix statement, `File.Sync` meaning, `WriteFile` partial-write warning, Windows mode bits. Removed: the claim that Windows `os.Rename` is an atomic replace via MoveFileEx, `EXDEV` wording, the ext4/XFS zero-length-after-power-loss claim, the "directory fsync unsupported on Windows" claim and the CreateTemp 0600 claim (not seen on the fetched page). The `Sync` and directory-sync steps are the author's recipe, not a documented guarantee.
Method: documentation only; no commands were run.

