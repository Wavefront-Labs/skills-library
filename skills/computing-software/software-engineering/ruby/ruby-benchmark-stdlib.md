---
id: computing-software.software-engineering.ruby.ruby-benchmark-stdlib
name: ruby-benchmark-stdlib
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, benchmark-stdlib, benchmarking]
level: practitioner
status: docs-checked
description: "Compare Ruby code with benchmark-ips: warmup and time, compare!, error margins, GC control, hold!, JSON output and iterations."
sources: ["https://github.com/evanphx/benchmark-ips"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmarking with benchmark-ips

benchmark-ips is an iterations-per-second enhancement to Benchmark (`gem install benchmark-ips`, no other requirements). For short snippets it works out how many times to run the code, so you do not guess iteration counts.

```ruby
require 'benchmark/ips'

Benchmark.ips do |x|
  x.config(warmup: 2, time: 5)        # seconds; defaults are 2 (warmup) and 5 (calculation)
  x.report("addition") { 1 + 2 }      # typical mode
  x.report("addition2") do |times|    # block receives the iteration count; you loop yourself
    i = 0
    while i < times
      i += 1
      1 + 2
    end
  end
  x.report("addition3", "1 + 2")      # string form, grafted into the loop (rarely needed)
  x.compare!                          # compare iterations per second across reports
end

Benchmark.ips_quick(:upcase, :downcase, on: "hello")   # shortcut comparison
```
- Reading the report: each line shows iterations per second with a percent standard deviation (how spread out the measurements are around the average); a high value means too much variability. `compare!` prints "same-ish: difference falls within error" when two results overlap within the error.
- `ips_quick` adds a very small overhead that can understate differences when the code runs more than 1 million iterations per second; use the full format for such microbenchmarks. The `|times|` form reduces overhead for very small workloads.
- GC control: pass a custom suite with `x.config(suite: suite)` whose `warming` and `running` hooks run `GC.enable; GC.start; GC.disable` to disable garbage collection during measurement (the README gives a `GCSuite` class).
- `x.hold! 'filename'` runs one benchmark per Ruby invocation, storing results in the file, so implementations are measured independently; the file is deleted once all results are gathered. `save!` is an alternative.
- `x.config(iterations: 3)` repeats warmup and calculation and keeps the last result, useful for Ruby implementations that optimise with tracing or on-stack replacement. Total time is `iterations * warmup + iterations * time` seconds.
- Statistics: the default margin of error is plus or minus one standard deviation. `x.config(stats: :bootstrap, confidence: 95)` uses a bootstrap confidence interval (median based), which needs `gem install kalibera` and a warmed-up, steady benchmark.
- `x.json! 'filename.json'` writes JSON; to write to STDOUT set `x.quiet = true` before `x.json! STDOUT`.
- `SHARE=1 ruby my_benchmark.rb` sends the result to a sharing service (benchmark.fyi) and prints a link, so avoid it with private code.

## Gotchas
- Treat gaps inside the reported error margin as noise; compare runs on the same Ruby version and settings.

## Checked

Date: 2026-11-08. Read in full: the benchmark-ips README on GitHub. Removed: all stdlib `Benchmark.bm`, `bmbm`, `realtime` and `measure` claims (the Benchmark class page is a stub at docs.ruby-lang.org), YJIT dead-code and constant-folding claims, `GC.stat` and benchmark-memory allocation advice, and the Benchmark.html source.

Method: documentation only; no commands were run.
