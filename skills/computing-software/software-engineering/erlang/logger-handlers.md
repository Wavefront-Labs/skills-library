---
id: computing-software.software-engineering.erlang.logger-handlers
name: logger-handlers
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-logging, logger-handlers]
level: advanced
status: docs-checked
description: "Erlang logger handlers: logger_std_h file output and rotation, logger_formatter templates, kernel logger config and custom handler callbacks."
sources:
  - https://www.erlang.org/doc/apps/kernel/logger_chapter.html
  - https://www.erlang.org/doc/apps/kernel/logger_std_h.html
  - https://www.erlang.org/doc/apps/kernel/logger_formatter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handlers, formatters and files
**Goal:** send logs to the right place with the right format.

```erlang
%% sys.config
[{kernel, [
  {logger_level, info},
  {logger, [
    {handler, default, logger_std_h,
      #{level => info,
        config => #{file => "log/app.log", max_no_bytes => 10485760, max_no_files => 5},
        formatter => {logger_formatter, #{template => [time, " ", level, " ", pid, " ", msg, "\n"],
                                          single_line => true}}}}]}]}].
```
- `logger_std_h` prints to `standard_io`, `standard_error` or a file; the type defaults to `standard_io` unless `file` is given. The Kernel default handler logs to `standard_io`.
- `max_no_bytes` is the size at which the file rotates (`infinity` never rotates); `max_no_files` is the number of rotated archives kept, named `FileName.0` (newest) upward, and only matters when `max_no_bytes` is an integer.
- Add handlers at runtime with `logger:add_handler(Id, Module, Config)`. A handler module must export `log/2`; `adding_handler/1`, `changing_config/3`, `filter_config/1` and `removing_handler/1` are optional.
- Overload protection options include `sync_mode_qlen`, `drop_mode_qlen` and `flush_qlen`, with `sync_mode_qlen =< drop_mode_qlen =< flush_qlen`.
- `{handler, default, undefined}` in the kernel `logger` parameter disables the default handler.

## Gotchas
- A file handler without `max_no_bytes` grows indefinitely.

## Self-check
Switch the default formatter to `single_line` and check the output.

## Checked

2026-11-03. Confirmed in the Logger chapter, `logger_std_h` and `logger_formatter` pages. Fixed: the config key for a log file is `file => FileName` (the old example used `type => {file, ...}`, which is not a valid type) and the sys.config term now ends as a list. Removed: the container-specific advice and the claim that JSON output needs a custom formatter.
Method: documentation only; no commands were run.
