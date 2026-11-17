---
id: computing-software.software-engineering.ruby.ruby-logger-stdlib
name: ruby-logger-stdlib
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, logger-stdlib, logging]
level: practitioner
status: docs-checked
description: "Configure Ruby's Logger: levels, rotation, custom formatters, JSON lines, progname and thread-safe use."
sources: ["https://docs.ruby-lang.org/en/master/Logger.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logger stdlib

```ruby
require "logger"; require "json"; require "time"
log = Logger.new($stdout, progname: "billing", level: Logger::INFO)
log.formatter = proc do |sev, time, prog, msg|
  msg = "#{msg.message} (#{msg.class})" if msg.is_a?(Exception)   # custom formatters get the raw object
  JSON.generate(ts: time.utc.iso8601(3), level: sev, app: prog, msg: msg) + "\n"
end
log.info("started")
log.debug { "expensive #{obj.inspect}" }   # block only runs if DEBUG enabled
Logger.new("app.log", 5, 10 * 1024 * 1024)   # keep 5 files of 10 MB
Logger.new("app.log", "daily")               # age-based rotation
```
Levels, low to high: DEBUG (0), INFO, WARN, ERROR, FATAL, UNKNOWN (5). `log.level =` accepts an integer, string or symbol (`:warn`, `"warn"`); anything else raises `ArgumentError`. `log.with_level(:debug) { ... }` changes the level for the block, for the current Fiber only.

## Gotchas
- File output goes through `LogDevice`, which serialises writes with a monitor (thread-safe) and takes a file lock (`flock`) while rotating, so several processes sharing one file can rotate it.
- Use the block form for costly messages; the block is not evaluated unless the level is enabled. String interpolation in a plain argument is always evaluated.
- Integer `shift_age` (default 7) with `shift_size` (default 1048576 bytes) rotates by size; `"daily"`, `"weekly"` or `"monthly"` rotates by period, and the rotated file name gets a date suffix (`shift_period_suffix`, default `%Y%m%d`).
- The default formatter handles an Exception message by printing its message, class and backtrace; a custom formatter receives the object unchanged, so format it yourself (as above).
- Never log secrets, tokens or full request bodies; add a redaction step in the formatter.
- A failed write or rotation is reported with `warn`, not raised, unless the class is listed in `reraise_write_errors:`.

Verify: set level to WARN, call `info`, and confirm nothing is printed; call `log.error(StandardError.new("x"))` with the default formatter and confirm the output contains "x (StandardError)".

## Checked
2026-11-03. Confirmed against ruby/logger `lib/logger.rb` (rdoc: block form, progname, `level=` coercion, `with_level`, rotation examples, `initialize` defaults), `lib/logger/log_device.rb` (monitor, `flock` rotation, defaults 7 and 1048576, `%Y%m%d`, write error handling), `lib/logger/formatter.rb` (Exception output) and `lib/logger/severity.rb`. Fixed: the old gotcha said processes sharing a file cannot rotate safely, but rotation takes an inter-process lock. Removed: the `$stdout` pipe buffering claim (not in the docs; file logs are opened with sync on) and the "log to stdout" advice.
Method: documentation only; no commands were run.
