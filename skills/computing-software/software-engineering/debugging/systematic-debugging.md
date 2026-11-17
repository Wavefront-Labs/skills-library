---
id: computing-software.software-engineering.debugging.systematic-debugging
name: systematic-debugging
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, systematic-debugging, reproduce, minimal-reproduction, delta-debugging, hypothesis, scientific-method, git-bisect, bisection, gdb, lldb, pdb, debugpy, delve, rr, record-replay, breakpoints, conditional-breakpoints, watchpoints, structured-logging, tracing, heisenbug, race-condition, sanitizers, asan, tsan, rubber-duck, software-engineering]
level: practitioner
status: draft
description: "Find root causes methodically: reproduce reliably, minimise the case, test one hypothesis at a time, bisect history, use debuggers and logs well, and corner heisenbugs."
sources: ["Zeller, Why Programs Fail (2nd ed.)", "Agans, Debugging: The 9 Indispensable Rules", "Git documentation - git-bisect", "rr project documentation (rr-project.org)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Systematic debugging — from symptom to root cause without guessing

**Goal:** turn "it's broken" into a confirmed root cause and a regression test, in
bounded time, by narrowing the search space deliberately instead of poking at code.

## 1. Reproduce it reliably
- Capture the exact failure: full error text, stack trace, input, versions (`git rev-parse
  HEAD`, dependency lockfile, OS, runtime), config and environment variables.
- Get a reproduction you can run in one command, ideally as a failing automated test.
  If it fails intermittently, wrap it in a loop and measure the rate:
  `for i in $(seq 200); do ./repro || echo FAIL $i; done | grep -c FAIL`.
- Can't reproduce locally? Diff the environments (data, flags, timezone, locale,
  CPU count, network) and move toward production conditions one variable at a time.

## 2. Minimise the failing case
Shrink input and code until removing anything makes the bug vanish.
- Halve the input repeatedly (delta debugging); tools: `creduce`/`cvise` for compiler
  inputs, property-based testers (Hypothesis, fast-check, QuickCheck) that shrink
  failing examples automatically.
- Stub out subsystems; delete code paths in a scratch branch.
- The minimal case often *is* the explanation, and it becomes the regression test.

## 3. Hypothesise, predict, test — one variable at a time
Keep a running log (a text file is fine): observation → hypothesis → experiment →
result. For each hypothesis write the prediction first ("if the cache is stale, then
clearing it makes the second call pass"). Change one thing per experiment and revert it
if it disproves the hypothesis. Read the error and stack trace fully — the first
exception in the log, not the last, is usually the cause. Explaining the code aloud
line by line (rubber duck) surfaces wrong assumptions fast.

## 4. Bisect when it used to work
```
git bisect start
git bisect bad HEAD
git bisect good v2.3.0
git bisect run ./repro.sh      # exit 0 good, 1-124/126-127 bad, 125 skip
git bisect reset
```
~log2(N) steps: 1,000 commits take about 10 runs. Use exit 125 for commits that don't
build. Bisection also works on non-code variables: dependency versions, config keys,
input records, feature flags.

## 5. Use a debugger, not just prints
- Python: `breakpoint()` (honours `PYTHONBREAKPOINT`), `python -m pdb -c continue app.py`
  for post-mortem; `debugpy` for remote/IDE attach.
- Native: `gdb -p <pid>`, `lldb`; `bt` for backtrace, `thread apply all bt` for every thread
  (essential for hangs). Build with `-g -O0` (or `-Og`) when stepping.
- Go: `dlv debug` / `dlv attach <pid>`. JVM: `jdb` or IDE remote debug via
  `-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005`; `jstack <pid>`
  for thread dumps. Node: `node --inspect-brk app.js` then Chrome DevTools.
- Conditional breakpoints (`break foo.c:42 if id == 1234`) and **watchpoints**
  (`watch obj->state`) find "who changed this?" instantly.
- **Record and replay** (`rr record ./app`, then `rr replay` with reverse-continue) on
  Linux turns an intermittent failure into a deterministic one you can step backwards
  through. Time-travel debugging exists in WinDbg and some IDEs too.

## 6. Logging that helps
- Structured (JSON) logs with a correlation/trace id across services; log inputs and
  decisions at boundaries, not every line.
- Temporarily raise one logger's level rather than the whole app.
- In distributed systems, start from a trace (OpenTelemetry).

## 7. Heisenbugs: when observing changes the bug
Timing-sensitive bugs disappear under the debugger or extra logging.
- Suspect concurrency, uninitialised memory, undefined behaviour, GC/finaliser timing,
  or reliance on hash/iteration order.
- Use sanitizers: `-fsanitize=address,undefined`, `-fsanitize=thread` (C/C++/Rust
  nightly), Go `go test -race`, Valgrind/Helgrind.
- Make it *more* likely: stress with many iterations, more threads than cores,
  `stress-ng` load, `rr record --chaos`, injected sleeps at suspected race points.

## 8. Close the loop
Fix the root cause, not the symptom; keep the minimal reproduction as a test that
failed before and passes after; search for the same pattern elsewhere (`git grep`);
write two lines in the commit message on cause and why the fix is correct.

## Gotchas
- Debug builds and optimised builds can behave differently (UB, inlining, timing);
  confirm the fix in the build that actually failed.
- Stale artefacts — cached builds, old containers, a different binary on `PATH` —
  make you debug code that isn't running. Print a version/build id on startup.
- "It's a compiler/library bug" is almost always wrong; prove it with a minimal case.
- Fixing several things at once leaves you unsure which change mattered.

## Verify
- [ ] A one-command reproduction exists and fails before the fix.
- [ ] The failing case was minimised and kept as a regression test.
- [ ] The root cause is written down and explains every observed symptom.
- [ ] The fix was confirmed in the same build type and environment that failed.
- [ ] Intermittent bugs were run enough times (e.g. hundreds of iterations) to show the
      failure rate dropped to zero.

Related: computing-software.software-engineering.concurrency.profiling-before-optimising
