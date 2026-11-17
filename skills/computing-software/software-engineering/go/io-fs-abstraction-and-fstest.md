---
id: computing-software.software-engineering.go.io-fs-abstraction-and-fstest
name: io-fs-abstraction-and-fstest
category: computing-software
field: software-engineering
product: go
tags: [go, go-io-files, go-io-fs, io-fs, fstest, mapfs]
level: practitioner
status: docs-checked
description: "Write filesystem-agnostic Go code against io/fs and test it with testing/fstest.MapFS, embed.FS and os.DirFS."
sources:
  - https://pkg.go.dev/io/fs
  - https://pkg.go.dev/testing/fstest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# io/fs abstraction and fstest

**Goal:** code that reads files works on disk, embedded assets, zips and in-memory fixtures.

```go
func LoadTemplates(fsys fs.FS) (*template.Template, error) {
    return template.ParseFS(fsys, "templates/*.html")
}

//go:embed templates
var assets embed.FS
t, _ := LoadTemplates(assets)                    // production
t, _ := LoadTemplates(os.DirFS("./testdata"))    // dev
t, _ := LoadTemplates(fstest.MapFS{              // unit test
    "templates/a.html": {Data: []byte("{{.}}")},
})

err := fs.WalkDir(fsys, ".", func(p string, d fs.DirEntry, err error) error { ... })
matches, _ := fs.Glob(fsys, "*.json")
sub, _ := fs.Sub(fsys, "static")                 // re-root
```

Paths are UTF-8, unrooted and slash-separated, on all systems including Windows, checked by `fs.ValidPath`: no `.` or `..` or empty element (except `.` for the root), and no leading or trailing `/`.
Optional interfaces (`fs.ReadFileFS`, `fs.StatFS`, `fs.ReadDirFS`) let an implementation provide optimised versions; the `fs` helper functions use them when present.

## Gotchas
- `os.DirFS` does not check symbolic links that point outside the directory, and `fs.Sub` does not change that: it is not a chroot-style security mechanism. Use `os.Root` to constrain access to a directory tree.
- `fstest.MapFS` reads directly from the map: do not run file system operations concurrently with edits to the map, and keep it to a few hundred entries or directory reads. Parent directories are synthesised.

## Checked
2026-11-09. Confirmed on pkg.go.dev/io/fs: path name rules, `ValidPath`, `WalkDir`, `Glob`, `Sub`, `ReadDirFS`/`ReadFileFS`/`StatFS`, the `os.DirFS`/`os.Root` warning, and that `fstest.TestFS` tests FS implementations.
Confirmed on pkg.go.dev/testing/fstest: `MapFS`/`MapFile.Data`, parent synthesis and the concurrency and size notes. Removed claims not on those pages: `http.FS`, "fs.FS is read-only",
the `filepath.Join` vs `path.Join` advice, `os.Root` version number, and embed.FS read-only/zero-modification-time behaviour (the `embed` and `template` lines in the example are illustrative and not covered by the cited pages).
Method: documentation only; no commands were run.

## Verify
`fstest.TestFS(fsys, "templates/a.html")` tests that a custom `fs.FS` implementation correctly implements the interface and contains the expected files.
