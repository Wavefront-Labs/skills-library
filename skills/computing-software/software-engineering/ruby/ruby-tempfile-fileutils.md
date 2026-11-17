---
id: computing-software.software-engineering.ruby.ruby-tempfile-fileutils
name: ruby-tempfile-fileutils
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, tempfile-fileutils, filesystem]
level: practitioner
status: docs-checked
description: "Use Tempfile, Dir.mktmpdir and FileUtils for safe scratch space, file replacement, directory creation and cleanup."
sources: ["https://docs.ruby-lang.org/en/master/Tempfile.html", "https://docs.ruby-lang.org/en/master/FileUtils.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tempfile, Dir and FileUtils

```ruby
require "tempfile"; require "tmpdir"; require "fileutils"
Tempfile.create("report") do |f|        # removed when the block ends
  f.write(data); f.flush
  system("tool", f.path) or raise "tool failed"
end
Dir.mktmpdir("build-") { |dir| build_in(dir) }  # directory and contents removed when the block returns

FileUtils.mkdir_p("a/b/c")
FileUtils.rm_rf(path)               # forcible recursive remove; dangerous with a wrong variable

# Replace a file: write a temp file in the SAME directory, then rename it over the target
tmp = Tempfile.create(["cfg", ".json"], File.dirname(target))  # [prefix, suffix], directory
tmp.write(json); tmp.close
File.rename(tmp.path, target)
```
Options such as `verbose: true` and `noop: true` let you preview destructive operations: `FileUtils.rm_rf(dir, noop: true, verbose: true)`.

## Gotchas
- `Tempfile.new` relies on a finalizer to delete the file, which may not run promptly or at all after an abnormal exit; prefer `Tempfile.create` with a block, which returns a plain `File` and removes the file when the block exits.
- Writes are buffered: `flush` or `close` before another process reads `f.path`.
- `FileUtils.mv` across file systems first copies, then removes the source, so keep the temp file beside the target.
- `rm_rf("#{dir}/#{name}")` with an empty `name` removes the whole directory; validate inputs. FileUtils documents `remove_entry_secure` and the `secure: true` option against the TOCTTOU vulnerability.
- Let Tempfile choose the name rather than using a predictable one.

Verify: after the block, `File.exist?(path)` is false; run `rm_rf` with `noop: true` first and read the printed commands.

## Checked
2026-11-03. Confirmed against ruby/ruby `lib/tempfile.rb` (create with block, array basename and directory argument, finalizer caveats, anonymous), `lib/tmpdir.rb` (mktmpdir block removes the directory) and `lib/fileutils.rb` (mkdir_p, rm_rf, noop and verbose, remove_entry_secure, mv across file systems). Removed: the `cp_r("src/.")` trailing-dot claim, the "rename is atomic" claim and the Ruby 2.4 version tag (not stated on those pages).
Method: documentation only; no commands were run.
