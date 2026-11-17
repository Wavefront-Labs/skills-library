---
id: computing-software.software-engineering.java.thread-dump-analysis-with-jstack-and-jcmd
name: thread-dump-analysis-with-jstack-and-jcmd
category: computing-software
field: software-engineering
product: java
tags: [java, jdk-diagnostics, thread-dump-analysis, jstack, jcmd-thread-print, deadlock, blocked-threads, high-cpu]
level: practitioner
status: docs-checked
description: "Capture and read Java thread dumps with jcmd Thread.print and jstack: find blocked threads, lock contention and hot CPU threads."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/jstack.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread dumps with jcmd/jstack

## Capture (take 3 dumps, 5-10 s apart)
```bash
jcmd <pid> Thread.print -l > td1.txt        # -l also prints java.util.concurrent locks
jstack -l <pid> > td2.txt                    # -l: long listing with additional lock information
```
`Thread.print` prints all threads with stack traces; its impact is medium and depends on the number of threads. jcmd must be run as the same effective user as the target JVM. `jstack` is documented as experimental and unsupported, and may be unavailable in future JDK releases, so prefer `jcmd`. In containers run it through your exec tool against the Java process.

## Read it
Each entry shows thread name, state and stack; for each Java frame the class, method and line number appear when available.
- `BLOCKED` threads show which monitor they wait to lock; find the thread that holds it.
- Many identical idle stacks in a pool are normal; many threads blocked on the same lock, pool or connection indicate contention.
- Take several dumps: a thread must be in the same frames each time to matter.

## High CPU per thread
```bash
top -H -p <pid>                  # find hot thread id (decimal)
printf '%x\n' <tid>              # convert to hex, match the native thread id in the dump
```
For sampling, use JFR or async-profiler.

## Gotchas
- A dump is a snapshot of state, not history.
- Don't paste dumps with secrets (headers, SQL parameters, tokens) into public tickets.

## Checked

Method: docs-checked 2026-11-09 against the JDK 21 jcmd and jstack man pages (Thread.print options, -l, same effective user, jstack experimental status). The troubleshooting-hanging-vm page was fetched but did not contain thread dump or deadlock text, so it is dropped as a source. Dropped unconfirmed claims (kill -3, Thread.dump_to_file and virtual thread dumps, deadlock report text, Hikari pool, jdk.tracePinnedThreads, fastThread, TDA, test recipe).
