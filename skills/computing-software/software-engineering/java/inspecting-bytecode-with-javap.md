---
id: computing-software.software-engineering.java.inspecting-bytecode-with-javap
name: inspecting-bytecode-with-javap
category: computing-software
field: software-engineering
product: java
tags: [java, java-jvm-internals, javap-bytecode, javap, bytecode, class-file-version, lambda-invokedynamic, string-concat-indy]
level: advanced
status: docs-checked
description: "Use javap -c -p -v -s -l to disassemble class files, select classes by name, file, jar URL or class path, and understand what each option shows, per the JDK 21 man page."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/javap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting bytecode with javap

`javap [options] classes...` disassembles class files and prints to stdout. With no options it prints protected and public fields and methods.

## Options (JDK 21 man page)
| Option | Effect |
|---|---|
| `-c` | disassembled code: the instructions comprising the bytecodes of each method |
| `-p` / `-private` | show all classes and members |
| `-v` / `-verbose` | additional information about the class |
| `-s` | internal type signatures |
| `-l` | line number and local variable tables |
| `-public`, `-protected`, `-package` | restrict to those access levels; `-package` is the default |
| `-constants` | static final constants |
| `-sysinfo` | path, size, date and SHA-256 hash of the class |
| `--class-path`, `-classpath`, `-cp` | where to find user class files; overrides CLASSPATH |
| `--module` / `-m`, `--module-path`, `--system` | module selection and lookup |
| `--multi-release version` | choose the version in multi-release JARs |
| `-J<option>` | pass an option to the JVM |

## Selecting classes
The `classes` argument can be a file name, URL or fully qualified class name: `path/to/MyClass.class`, `jar:file:///path/to/MyJar.jar!/mypkg/MyClass.class`, `java.lang.Object`.

## Commands
```bash
javap -c -p com.acme.Foo                    # disassemble all members including private
javap -v -p target/classes/com/acme/Foo.class
javap -s Foo
javap -l Foo
```

## Gotchas
- `javap` is not multi-release JAR aware: the class-path form views the base entry in every JAR; use the URL form or `--multi-release` to pick a version.
- Without `-p` you only see package, protected and public members.
- The man page's example shows `javap -c` printing `Code:` listings with constant-pool references in comments, such as `invokespecial #1 // Method javax/swing/JFrame."<init>":()V`.

## Verify
Compile a small class, run `javap` with no options, then with `-c -p`, and compare what appears.

## Checked
Confirmed against the JDK 21 `javap` man page: synopsis, description, options, class argument forms, multi-release note and example. Removed: class-file major version numbers, what lambdas, string concatenation, switches and records compile to, the JIT and hsdis notes, `--release 8` behaviour and the JVMS chapter 6 source, none of which the man page states.
Method: docs-only read of cited pages, 2026-11-08
