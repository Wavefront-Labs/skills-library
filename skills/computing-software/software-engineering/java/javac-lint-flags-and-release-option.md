---
id: computing-software.software-engineering.java.javac-lint-flags-and-release-option
name: javac-lint-flags-and-release-option
category: computing-software
field: software-engineering
product: java
tags: [java, jdk-dev-tools, javac-flags, javac-release, xlint, parameters-flag, werror, source-target-mismatch]
level: practitioner
status: docs-checked
description: "Compile with javac correctly: --release instead of -source/-target, -Xlint categories, -Werror, -parameters, -g, --enable-preview, and wiring them in Maven and Gradle."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html", "https://maven.apache.org/plugins/maven-compiler-plugin/compile-mojo.html", "https://docs.gradle.org/current/dsl/org.gradle.api.tasks.compile.CompileOptions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# javac flags that matter

## --release, not -source/-target
`--release N` compiles according to the language rules of Java SE release N, generates class files that target that release, and compiles against the Java SE and JDK API of that release. `-source` and `-target` set only the language level and class-file level, so the Oracle manual says you should also give the matching platform classes (the boot class path options for releases before 9, or `--system` for 9 and later); otherwise the code is compiled against the running JDK's classes. `--release` cannot be combined with `-source`/`-target`, and with `--release` you cannot use options that break encapsulation (such as `--add-exports` on Java SE, JDK or standard modules) to reach internal classes. Supported values are the current release and a limited number of previous releases; the command-line help lists them.

- Maven: `<release>` parameter of maven-compiler-plugin (user property `maven.compiler.release`, since plugin 3.6). `source` and `target` default to `1.8` in current plugin versions.
- Gradle: `options.release` (`Property<Integer>`) on the compile task. If `--release` is added through `compilerArgs`, `-target` and `-source` are ignored.

## Lint
```bash
javac --release <N> -Xlint:all -Werror -parameters -g Foo.java
```
- `-Xlint:all` enables all warnings. Keys include `unchecked`, `rawtypes`, `deprecation`, `removal`, `this-escape`, `serial`, `fallthrough`, `cast`, `overrides`, `static`, `try`, `varargs`, `processing`. Prefix a key with `-` to disable it: `-Xlint:all,-serial,-processing`. Keys other than `all` and `none` also work with `@SuppressWarnings`.
- `-Werror` terminates compilation when warnings occur. Maven: `failOnWarning` (default false, since 3.6). Adopt it after cleaning existing warnings.
- `-Xdiags:verbose` selects the verbose diagnostic mode; `-Xmaxerrs <n>` and `-Xmaxwarns <n>` set the maximum numbers printed. Maven passes extra flags through `compilerArgs`.
- `-parameters` stores formal parameter names in the class file so `java.lang.reflect.Executable.getParameters` can read them. Maven: `parameters` (default false, since 3.6.2).
- `-g` generates all debugging information including local variables; by default only line numbers and source file are generated. `-g:[lines,vars,source]` picks kinds and `-g:none` generates none. Maven `debug` defaults to true; Gradle `debug` defaults to true.
- `--enable-preview` enables preview language features and is used with `-source` or `--release`. Maven: `enablePreview`; Gradle: `compilerArgs.add("--enable-preview")`.
- `-proc:none|only|full` controls annotation processing: `none` compiles without it, `only` runs only processing, and unset or `full` does both (JDK 21 manual).
- `-encoding <name>` sets the source encoding; if not given, the platform default converter is used (JDK 21 manual).
- `-implicit:none` suppresses class file generation for sources found only through the source path; `-implicit:class` generates them (the default generates them).

## Gotchas
- Javac does not check documentation comments by default; `-Xdoclint` enables the checks.
- Mixed `--release` values across modules in one deployment can still cause version-mismatch bugs: inspect class files with `javap -v` (`inspecting-bytecode-with-javap`).

## Verify
Compile code that calls a method added after the target release with `--release <older>`: the compile must fail, showing that the API check works.

## Checked

Confirmed on the JDK 21 javac manual, the maven-compiler-plugin compile goal page and the Gradle CompileOptions page: --release semantics, source/target conflict, Xlint keys and syntax, Werror, parameters, -g, enable-preview, proc, encoding, implicit, Xdiags, Xmaxerrs, Xdoclint, and the Maven and Gradle options. Removed (not stated on the pages): `ct.sym`, `NoSuchMethodError`, a fixed supported range of 8 to current, the JDK 23 `-proc` default change, UTF-8 as the javac default on JDK 18+, the "class files require the same JVM" preview remark, the Spring and Jackson uses of `-parameters`, the toolchain remark and the exact `-source 8` warning text.

Method: docs-only read of cited pages, 2026-11-08
