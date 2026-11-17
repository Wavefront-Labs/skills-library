---
id: computing-software.software-engineering.go.package-naming-and-avoiding-util-packages
name: package-naming-and-avoiding-util-packages
category: computing-software
field: software-engineering
product: go
tags: [go, go-design-style, go-package-naming, package-naming, naming-conventions]
level: practitioner
status: docs-checked
description: "Name Go packages and identifiers the idiomatic way: short lower-case nouns, no stutter, no util or common, and what to put where."
sources:
  - https://go.dev/blog/package-names
  - https://go.dev/doc/effective_go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Package naming and avoiding util packages

**Goal:** call sites that read well: `http.Server`, `list.New()`, not `util.NewHTTPClientHelper`.

Rules from the Go blog "Package names" and Effective Go:
- Package names are short and clear: lower case, no under_scores or mixedCaps, often simple nouns (`time`, `list`, `http`). The package name is the base name of its directory (`encoding/base64` has name `base64`).
- Abbreviate only when the abbreviation is familiar (`strconv`, `syscall`, `fmt`); do not steal good names from users (`bufio`, not `buf`).
- Avoid repetition: the HTTP server in package `http` is `Server`, not `HTTPServer`. When a package exports one main type, the constructor can be just `New` (`ring.New`, `list.New()`); with several types use names such as `time.NewTicker` and `time.NewTimer`.
- Types in different packages may share a name (`jpeg.Reader`, `bufio.Reader`, `csv.Reader`).
- Getters do not use a `Get` prefix; setters use `SetX` (Effective Go: `SetOwner`).
- Use MixedCaps or mixedCaps for multiword names, not underscores.
- If you cannot find a package name that is a meaningful prefix for its contents, the abstraction boundary may be wrong: write code as a client would and restructure.
- Bad names: generic packages such as `util`. Fix by pulling related types and functions into a package named for the concept (blog example: `util.NewStringSet`/`util.SortStringSet` becomes `stringset.New` and then a `Set` type with a `Sort` method).
- Avoid package names that collide with popular standard packages such as `io` or `http`, and give packages that are frequently used together distinct names.

## Checked
Date: 2026-11-09. Confirmed against go.dev/blog/package-names and go.dev/doc/effective_go (package names, naming of contents, getters/`SetOwner`, MixedCaps, `util` to `stringset` example). Removed unconfirmed claims: initialism casing, `-er` interface naming, major-version suffix rule, `internal/`/`cmd/` remarks, external test packages, and the linter verification line.
Method: documentation only; no commands were run.
