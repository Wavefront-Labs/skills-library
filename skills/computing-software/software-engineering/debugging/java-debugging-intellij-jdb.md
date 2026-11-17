---
id: computing-software.software-engineering.debugging.java-debugging-intellij-jdb
name: java-debugging-intellij-jdb
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, java, java-debugging, hot-swap, jdwp, intellij-debugger, jdb]
level: practitioner
status: docs-checked
description: "Debug JVM applications: JDWP agent options, jdb attach and breakpoint commands, and IntelliJ logpoints, force return, throw exception and class reload."
sources: ["https://www.jetbrains.com/help/idea/debugging-code.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/jpda/conninv.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/jdb.html", "https://www.jetbrains.com/help/idea/altering-the-program-s-execution-flow.html#reload_classes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java debugging (IntelliJ / jdb / hot swap)

## Start the JVM with a debug agent
```
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 -jar app.jar
```
- `server=y` listens for a debugger to attach. `suspend=y` (the default) suspends the VM
  before the main class loads and waits; `suspend=n` lets it run.
- Socket addresses are `<host>:<port>`. An empty host means the loopback address only;
  `*` listens on all network interfaces. The `allow=` option restricts which addresses may
  connect. Prefer loopback plus a tunnel for remote hosts.
- In IntelliJ attach with a Remote JVM Debug run configuration to host and port.

## IntelliJ techniques
- A breakpoint with the Suspend box cleared and an expression in the Evaluate and log
  field logs (or alters state) without stopping the program.
- Force return exits the current method early with a value you choose; instructions after
  the current point are skipped.
- Throw Exception (right-click the frame in the Frames tab) throws an exception you
  construct (for example `new NullPointerException()`, without the `throw` keyword) to
  test error handling.
- Reload classes: recompilation happens automatically only when "Build project before
  reloading classes" is enabled under the debugger HotSwap settings; otherwise recompile
  first. What a reload can change is limited by the JVM; check the JetBrains page.

## jdb (no IDE)
```
jdb -attach localhost:5005
> stop at com.acme.OrderService:118
> stop in com.acme.OrderService.place
> catch java.lang.IllegalStateException
> cont / step / next
```
- `stop at Class:line` breaks at a line; `stop in Class.method` at a method start.
- `catch` stops where a matching exception (or subclass) is thrown; `ignore` undoes it for
  the debugger only.
- `step` advances to the next line, entering called methods; `next` stays in the current
  frame; `cont` resumes. `clear` removes breakpoints.

## Checked
2026-11-01. Confirmed against the JPDA connection and invocation spec (JDK 21: `dt_socket`, `server`, `suspend` default, `*` host, `allow`), the jdb man page (`-attach`, `stop at/in`, `catch`, `ignore`, `step`, `next`, `cont`, `clear`) and the JetBrains pages (Evaluate and log with Suspend cleared, Force return, Throw Exception, build before reload). Removed: JDK-version gate, Maven/Gradle debug flags, JDWP-auth statement, breakpoint-type menu paths and performance remarks, suspend-policy advice, hot-swap limits and DCEVM/JRebel, shortcuts, jcmd/jstack/JFR line.
Method: documentation only; no commands were run.
