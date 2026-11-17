---
id: computing-software.software-engineering.ruby.ruby-stringio-testing
name: ruby-stringio-testing
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, stringio-testing, testing]
level: practitioner
status: docs-checked
description: "Test IO-heavy Ruby with StringIO: injected streams, capturing stdout/stderr, stdin fakes and rewind pitfalls."
sources: ["https://docs.ruby-lang.org/en/master/StringIO.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StringIO for testing IO code

Design code to take an IO argument instead of hard-coding `$stdout` or `File.open`:
```ruby
def report(items, out: $stdout) = items.each { |i| out.puts i }

io = StringIO.new
report(%w[a b], out: io)
io.string            # "a\nb\n"

input = StringIO.new("yes\n")
answer = input.gets.chomp          # works as stdin replacement

def capture
  old = $stdout; $stdout = StringIO.new
  yield; $stdout.string
ensure
  $stdout = old
end
```
For reading: `StringIO.new(text).each_line`, `readlines`, `read(n)`, `ungetc`, `rewind`, `pos=`.

## Gotchas
- After writing then reading from the same StringIO you must `rewind` (or set `pos=`); a StringIO has a single position.
- `StringIO.new(string)` with a frozen string defaults to mode `'r'`; a write then raises `IOError` ("not opened for writing"). Use `+""` or `String.new`, or leave the string off.
- Reassigning `$stdout` is global state: restore in `ensure`, and prefer injecting the stream.
- `StringIO#fileno` returns nil because there is no file descriptor, so code that needs a real descriptor will not work with it. Use a Tempfile for those cases.
- Close a StringIO when you are done with it.

Verify: write, read without rewind (empty), then rewind and read again to see the data.

## Checked
2026-11-03. Confirmed against ruby/ruby `ext/stringio/stringio.c` rdoc and method table (`StringIO.new` default mode, frozen string mode `'r'`, "not opened for writing", `fileno` nil, `string`, `gets`, `read`, `readlines`, `each_line`, `ungetc`, `rewind`, `pos=`, `puts`). Removed: Minitest `capture_io`/`assert_output` and RSpec `output` matcher lines (gems not in the documentation read), `system(out: io)`/`IO.select`/Open3 and subprocess-capture claims.
Method: documentation only; no commands were run.
