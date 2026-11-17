---
id: computing-software.software-engineering.ruby.ruby-debug-gem
name: ruby-debug-gem
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, debug-gem, debugging]
level: practitioner
status: docs-checked
description: "Debug Ruby with the debug gem (rdbg): binding.break, breakpoints, stepping, catch, trace and remote attach."
sources: ["https://github.com/ruby/debug"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with the debug gem

debug.rb supports Ruby (MRI) 2.7 and later and replaces the old `lib/debug.rb`. It has no performance penalty when not stepping or at breakpoints, supports remote debugging, and handles threads (Ractors are a TODO).

```sh
gem install debug                       # in a Gemfile: gem "debug", ">= 1.0.0"
rdbg target.rb                          # run like `ruby target.rb`, stopped at the start
rdbg -c -- bundle exec rake test        # -c: the first argument is an executable in PATH
ruby -r debug/start target.rb           # or require "debug/start" at the very start
```
The version constraint matters: `debug < 1.0.0` is an older, abandoned, different gem. Using `bundle exec` requires `gem 'debug'` in the Gemfile. `--` separates rdbg options from the program: `rdbg -c -- rake -T`.

In code, `require 'debug'` and add `binding.break` (aliases `binding.b` and `debugger`). `require 'debug'` equals `rdbg --nonstop --no-sigint-hook`; `debug/start` equals `rdbg`; `debug/open` equals `rdbg --open`; `debug/open_nonstop` equals `rdbg --open --nonstop`. `binding.break do: 'info ;; watch @a'` runs commands and continues; `pre: 'p bar()'` runs a command and stays stopped.

At the `(rdbg)` prompt:
- Flow: `s[tep]`, `n[ext]`, `fin[ish]`, `u[ntil]`, `c`/`continue`, `q[uit]`, `kill`.
- Breakpoints: `b[reak] 42`, `b file:42`, `b Class#method`, `b ... if: expr`, `pre:`, `do:`, `path:` options, `catch ArgumentError` (stop on raise), `watch @ivar` (slow), `del[ete] [n]`.
- Information: `bt`, `list`, `whereami`, `info` (locals, `info ivars`, `info consts`, `info globals`), `outline` or `ls obj`, `display expr`, `undisplay`.
- Frames: `frame n`, `up`, `down`. Evaluate: `p`, `pp`, `eval`, `irb`.
- Trace: `trace line|call|exception|object expr`, `trace off`; `record on`, `step back` to replay.
- `config set no_color true`, `config` lists settings; `~/.rdbgrc` is loaded at start.

An input line that is not a debug command is evaluated as `pp expr`. Single-letter locals such as `i`, `b`, `n`, `c` clash with commands, so use `p i`. `Enter` repeats the last command for some commands.

## Remote debugging
- `rdbg --open target.rb` (`-O`) opens a UNIX domain socket and waits; attach with `rdbg --attach` (`-A`). For TCP use `--port 12345` (binds `localhost:12345`; `--host` to choose the host; `--port_range` tries a range) and attach with `rdbg --attach 12345`. `RUBY_DEBUG_PORT` sets the TCP port for `require 'debug/open'`.
- `quit` in the remote console leaves the debuggee running and reattachable; `kill` ends it.
- Use `--open=vscode` or `--open=chrome` for those frontends; `rdbg -c` is how the vscode-rdbg extension launches commands.

## Gotchas
- Messages between debugger and debuggee are not encrypted; `debug/open_nonstop` can become a backdoor and another vulnerability.
- `RUBY_DEBUG_ENABLE=0` disables the gem; `RUBY_DEBUG_FORK_MODE` (both/parent/child) controls which process activates after fork.
- With `Ctrl-C` under `rdbg` you can suspend a running program and enter the console.
- Remove `binding.break` calls before committing; the README does not provide a CI check, so add your own.

## Checked

Date: 2026-11-08. Read in full: the ruby/debug README on GitHub. Removed: the claim that debug is a bundled gem since Ruby 3.1 or replaces byebug (the README only links a migration guide), the Gemfile platforms line, Puma worker and request timeout advice, `rdbg --open --port 12345 server.rb` usage specifics beyond the README forms, and the generic docs.ruby-lang.org source (a stub).

Method: documentation only; no commands were run.
