---
id: computing-software.software-engineering.ruby.ruby-threads-mutex-gvl
name: ruby-threads-mutex-gvl
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-concurrency, threads-mutex-gvl]
level: advanced
status: docs-checked
description: "Use Thread, Mutex and Queue knowing the GVL limits CPU parallelism but not blocking IO."
sources: ["https://docs.ruby-lang.org/en/master/Thread.html", "https://docs.ruby-lang.org/en/master/Thread/Mutex.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threads and Mutex
- `Thread::Mutex#synchronize { }` guards shared resources between threads.
- `Thread.report_on_exception` and `Thread.abort_on_exception` control what happens when a thread dies from an exception (abort_on_exception defaults to false).
- Read-modify-write on shared state is not atomic; guard it.
Verify: stress test with many threads and assertions.

## Checked
2026-11-02. Confirmed against: Thread and Mutex pages. Removed or softened (not stated on those pages): GVL release rules, Queue/SizedQueue, ||= atomicity.
Method: documentation only; no commands were run.
