---
id: computing-software.software-engineering.crystal.dir-path-fileutils
name: dir-path-fileutils
category: computing-software
field: software-engineering
product: crystal
tags: [dir-path-fileutils, stdlib-io-files, dir, glob, path, fileutils, mkdir-p, rm-rf, cp-r, directory-listing, each-child, cwd, crystal]
level: practitioner
status: draft
description: "List and glob directories, build cross-platform paths with Path, and use FileUtils for mkdir_p, rm_rf, cp_r and mv."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dir, Path and FileUtils

Goal: manage directories.

- List: `Dir.children(path)`, `Dir.each_child(path) { |n| }`, `Dir.entries` (includes . and ..), `Dir.glob("src/**/*.cr")`, `Dir.exists?`.
- Create/remove: `Dir.mkdir(path)`, `Dir.mkdir_p`, `Dir.delete`; `require "file_utils"` for `FileUtils.mkdir_p`, `rm_rf`, `cp_r`, `mv`, `touch`, `cd`.
- `Dir.cd(path) { }` temporarily changes cwd (process-wide, not fiber-safe), `Dir.current`, `Dir.tempdir`.
- `Path["a", "b.txt"]`, `p.parent`, `p.basename`, `p.extension`, `p.join("x")`, `p.normalize`, `p.relative_to(base)`, `Path.posix`/`Path.windows`.

Gotchas:
- Glob does not sort portably; call `.sort`.
- Validate user paths: normalise and check the prefix to avoid traversal.
- cwd is global, so avoid `Dir.cd` in multi-fiber programs.

Verify: glob returns expected files in a tempdir spec.
