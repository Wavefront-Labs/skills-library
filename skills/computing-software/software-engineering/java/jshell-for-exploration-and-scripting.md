---
id: computing-software.software-engineering.java.jshell-for-exploration-and-scripting
name: jshell-for-exploration-and-scripting
category: computing-software
field: software-engineering
product: java
tags: [java, jdk-dev-tools, jshell, repl, jshell-classpath, jshell-scripts, api-exploration, java-9]
level: intro
status: docs-checked
description: "Use jshell to try APIs and snippets: class path and module flags, feedback modes, /commands, startup scripts, loading files and piping scripts, per the JDK 21 man page."
sources: ["https://docs.oracle.com/en/java/javase/21/jshell/introduction-jshell.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/jshell.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jshell

JShell evaluates declarations, statements, variable, method and class definitions, imports and expressions ("snippets") interactively, to learn the language, explore unfamiliar code and APIs and prototype code. Terminating semicolons are added automatically to completed snippets.

## Start and options (JDK 21 man page)
```bash
jshell
jshell --class-path target/classes:lib/guava.jar   # separator is : on Linux/macOS, ; on Windows
jshell --enable-preview
jshell -R-Xmx512m                                  # -R passes a flag to the remote runtime
jshell -J-Xmx512m                                  # -J passes a flag to the runtime system
jshell -C-Xlint                                    # -C passes a flag to the compiler
jshell -s                                          # silent feedback (-q concise, -v verbose)
```
- `--class-path` overrides CLASSPATH; if neither is set the current directory is searched.
- Also available: `--module-path`, `--add-modules`, `--add-exports`, `--feedback mode` (default is normal), `--startup file`, `--no-startup`, `--show-version`, `--version`.
- Predefined load/startup scripts: `DEFAULT` (common imports), `JAVASE` (all Java SE packages), `PRINTING` (print, println, printf methods), `TOOLING` (javac, jar and other JDK tool methods).

## Everyday use
```
jshell> int a=4
jshell> int square(int i1) { return i1 * i1; }
jshell> square(a)
$3 ==> 16
jshell> /vars        /methods     /types     /imports     /list     /history
jshell> /edit square     /open script.jsh      /save -all session.jsh
jshell> /set feedback verbose
jshell> /exit
```
- With no variable given, a scratch variable such as `$5` holds the result.
- Redefine a variable, method or class by entering it again; `/edit name` opens it in an editor.
- `/list` shows active snippets and IDs; `-all` includes startup snippets, failed or dropped ones (IDs starting with `s` are startup, `e` failed); `-start` shows startup snippets.
- The default startup snippets are imports of java.io, java.math, java.net, java.nio.file, java.util, java.util.concurrent, java.util.function, java.util.prefs, java.util.regex and java.util.stream.
- Tab completes snippets and commands; Tab after a method's opening parenthesis shows parameters; Shift+Tab V converts an expression to a variable declaration, Shift+Tab M to a method, Shift+Tab I suggests imports.
- Command abbreviations work if unique (`/l` is `/list`; `/s` is ambiguous, use `/se` or `/sa`).
- `/exit [integer-snippet]` uses the integer as the exit status.

## Scripting
```bash
jshell script.jsh                              # scripts run after startup scripts
echo 'System.out.println(java.time.Instant.now())' | jshell -s -    # '-' reads standard input without interactive I/O
jshell --startup DEFAULT --startup my-imports.jsh
```
Startup scripts run when JShell starts and after `/reset`, `/reload` or `/env`. `/set start [-retain] files` sets the startup scripts for the next reset; `-retain` keeps them across sessions. `/reset` discards all snippets and loses history; `/reload` replays history.

## Verify
Start jshell with `--class-path` pointing at your classes, call a method, then `/exit`.

## Checked
Confirmed against the JDK 21 `jshell` man page (synopsis, options, commands, shortcuts, examples). Removed: scratch-variable numbering claims beyond the page's example, checked-exception and forward-reference rules, `--release`, the remote-agent restart on System.exit, access-modifier warnings, Ctrl-C and the single-file source launch comparison, none of which the page states.
Method: docs-only read of cited pages, 2026-11-08
