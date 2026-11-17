---
id: computing-software.software-engineering.ruby.ruby-processes-ractors
name: ruby-processes-ractors
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-concurrency, processes-ractors]
level: advanced
status: docs-checked
description: "Parallelise CPU-bound work with fork/Process.wait or experimental Ractors."
sources: ["https://docs.ruby-lang.org/en/master/Process.html", "https://docs.ruby-lang.org/en/master/Ractor.html", "https://docs.ruby-lang.org/en/master/IO.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Processes and Ractors
- `Process.fork`, `Process.spawn`, `Process.wait`/`waitpid`, `Process.detach` create and manage child processes; `IO.pipe` creates a connected reader and writer pair.
- `Ractor.new` creates a Ractor that can run in parallel with other ractors; the Ractor API is flagged experimental (a warning is emitted on use).
Verify: wall-clock time scales with the number of workers.

## Checked
2026-11-02. Confirmed against: Process, IO.pipe, Ractor pages. Removed or softened (not stated on those pages): copy-on-write note, gem safety, parallel gem, nprocessors.
Method: documentation only; no commands were run.
