---
id: computing-software.software-engineering.groovy.process-execute
name: process-execute
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, process-execute]
level: practitioner
status: docs-checked
description: "Run external commands with String and List execute, read output with text and consumeProcessOutput, bound the wait with waitForOrKill."
sources:
  - https://groovy-lang.org/groovy-dev-kit.html
  - https://github.com/apache/groovy/blob/master/src/main/java/org/codehaus/groovy/runtime/ProcessGroovyMethods.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running external processes
- `"ls -l".execute()` runs a command line and returns a `java.lang.Process`; `process.text` reads its output. `ProcessGroovyMethods` also has `execute` on `List` and `String[]`, so `['git', '--version'].execute()` passes the arguments separately.
- Environment and working directory: `execute(List envp, File dir)` (the guide shows `"rm -f foo.tmp".execute([], tmpDir)`), also available for `List` and `String[]` commands.
- Some platforms give the subprocess only a limited buffer for standard input and output, so failing to promptly write its input or read its output can block it or even deadlock it. Call `consumeProcessOutput()` (or the `Appendable` and stream variants) or `waitForProcessOutput`, which drain the streams for you.
- `waitForOrKill(long numberOfMillis)` waits for the process and destroys it when the time is up.
- Shell commands such as `dir` are not programs on Windows: the guide runs `"cmd /c dir".execute()`.
- `ProcessBuilder` is the underlying Java API, and the GDK documents it in the same class.
- Several `execute()` processes can be piped together (the guide chains `ls` and several `tr` commands).

## Checked

2026-11-03. Confirmed against the Groovy Development Kit page (executing external processes, `cmd /c dir`, buffer and deadlock warning, pipe example) and the `ProcessGroovyMethods` source (`execute` overloads, `getText(Process)`, `consumeProcessOutput`, `waitForProcessOutput`, `waitForOrKill`). Removed: the code snippet and self-check, the claim that a single string is split on whitespace without a shell, the shell-injection advice for `sh -c`, and `exitValue` usage.

Method: documentation only; no commands were run.
