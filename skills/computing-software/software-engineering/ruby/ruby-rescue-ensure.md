---
id: computing-software.software-engineering.ruby.ruby-rescue-ensure
name: ruby-rescue-ensure
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-errors, rescue-ensure]
level: practitioner
status: docs-checked
description: "Rescue specific errors, use ensure/else/retry properly and avoid rescuing Exception."
sources: ["https://raw.githubusercontent.com/ruby/ruby/master/doc/syntax/exceptions.rdoc", "https://docs.ruby-lang.org/en/master/Exception.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rescue ensure retry and exception hierarchy
- Rescue in `begin ... rescue ... else ... ensure ... end`: `else` runs only when nothing was raised, `ensure` always runs, and `retry` in a rescue re-runs the begin block.
- The built-in hierarchy puts SystemExit, NoMemoryError, SignalException/Interrupt and StandardError as siblings under Exception, so a bare `rescue` (StandardError) leaves the others alone; do not rescue Exception.
- An exception can carry an optional `cause` (see `Exception#cause`).
Verify: specs asserting error class and cause.

## Checked
2026-11-02. Confirmed against: exceptions syntax doc and Exception hierarchy. Removed or softened (not stated on those pages): block-level rescue and retry-cap advice, bare-rescue wording.
Method: documentation only; no commands were run.
