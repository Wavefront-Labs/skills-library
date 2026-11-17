---
id: computing-software.software-engineering.ruby.ruby-system-commands-safely
name: ruby-system-commands-safely
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-io-security, system-commands-safely]
level: practitioner
status: docs-checked
description: "Run subprocesses with array arguments, Open3 and exit status checks, avoiding shell injection."
sources: ["https://docs.ruby-lang.org/en/master/Open3.html", "https://docs.ruby-lang.org/en/master/Shellwords.html", "https://docs.ruby-lang.org/en/master/Process/Status.html", "https://docs.ruby-lang.org/en/master/Kernel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running external commands safely
- `Open3.capture3` runs a command and returns stdout, stderr and status; `Process::Status#success?` reports success.
- `Shellwords.escape` (alias `String#shellescape`) escapes shell metacharacters for a command line; use it only when you must build a shell string.
- Pass the command and its arguments separately rather than interpolating untrusted input into one string.
Verify: input such as `; echo x` is treated as data.

## Checked
2026-11-02. Confirmed against: Open3, Shellwords, Process::Status, Process pages. Removed or softened (not stated on those pages): array-form-bypasses-shell claim stated as fact, chdir/env options, kill-on-timeout.
Method: documentation only; no commands were run.
