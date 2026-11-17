---
id: computing-software.software-engineering.java.multi-release-jars
name: multi-release-jars
category: computing-software
field: software-engineering
product: java
tags: [java, java-modules-packaging, multi-release-jar, meta-inf-versions, jep-238, library-packaging]
level: advanced
status: docs-checked
description: "Ship one Java library JAR with version-specific classes (JEP 238): META-INF/versions layout, Multi-Release manifest attribute, jar --release, Maven support and the rules."
sources: ["https://openjdk.org/jeps/238", "https://docs.oracle.com/en/java/javase/21/docs/specs/jar/jar.html#multi-release-jar-files", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/jar.html", "https://maven.apache.org/guides/mini/guide-multi-release-jars.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-release JARs (Java 9+)

A multi-release JAR holds base classes at the root plus version-specific classes and resources under `META-INF/versions/N`, where the runtime picks the best match.
```
mylib.jar
  META-INF/MANIFEST.MF                         Multi-Release: true
  com/acme/Hash.class                          (baseline)
  META-INF/versions/9/com/acme/Hash.class      (used on a Java 9+ runtime)
  META-INF/versions/17/com/acme/Hash.class     (preferred on Java 17+)
```
(`com/acme/Hash` is a placeholder.)

## How the runtime chooses (JAR specification)
- The JAR is identified by the main manifest attribute `Multi-Release: true` (value case is ignored; any other value means the attribute is ignored).
- `N` must be 9 or greater; versioned directories below 9, or malformed names, are ignored.
- On a runtime of major version N, the class loader searches the Nth versioned directory first, then lower versioned directories in descending order down to 9, and finally the root.
- Without the attribute, only the base (root) classes are used.
- Resources under `META-INF` itself cannot be versioned. A multi-release JAR can be signed. The boot class loader does not support them: a JAR appended with `-Xbootclasspath/a` is treated as an ordinary JAR.

## Rules for contents
- The public API exported by classes must be exactly the same across versions. A public or protected class in a versioned directory must also exist, with the same fully qualified name and access modifier, in the top-level directory. Tools such as `jar` are not required to verify this and a runtime does not verify it.
- A class file in version directory N must have a class file version no higher than the one for Java N.
- Keep all versions in sync: if you add a method to one class, add it to the others. The Maven guide suggests having the version-specific classes implement an interface and calling only the interface methods from base code.

## Build
With the `jar` tool, `--release VERSION` places the files that follow it under `META-INF/versions/VERSION/` (VERSION is an integer 9 or greater):
```bash
jar --create --file foo.jar --main-class com.foo.Hello -C classes . --release 10 -C classes-10 .
```
This is the man-page example; it produces a manifest containing `Multi-Release: true`. `jar --describe-module --file foo.jar` prints the module descriptor.

With Maven (compiler plugin guide): the compiler must run once per Java version, either from several modules or from extra compiler executions in the POM. Setting `release` together with `multiReleaseOutput` to `true` in an additional execution places that execution's output in `META-INF/versions/${release}`. The maven-jar-plugin adds `Multi-Release: true` by itself when the JAR contains a `META-INF/versions` directory (`detectMultiReleaseJar`, on by default), or you can add it explicitly with `manifestEntries`.

## Gotchas
- The attribute is only recognised for classes inside a JAR, so you cannot test `target/classes/META-INF/versions/...` directly; test the built JAR on every targeted Java version.
- `JarFile` and the `jar:` URL handler keep their old behaviour by default; code that opens the JAR itself must opt in to version selection (JEP 238). The runtime's own class loaders opt in automatically.
- The Maven guide warns that multi-release JARs are hard to read, maintain and test; consider whether a simple `if/else`, or raising the minimum Java version, is enough.

## Verify
List the built JAR (`jar tf`) to confirm the `META-INF/versions/N` entries and manifest attribute, then run a smoke test on each targeted runtime.

## Checked
2026-11-03. Confirmed against the JAR specification (multi-release section), JEP 238, the Java SE 21 `jar` man page and the Maven multi-release guide: layout, manifest attribute, version search order, N >= 9, same-API rule, class file version rule, signing, boot loader, `--release` and `--describe-module`, `multiReleaseOutput`, `detectMultiReleaseJar`, testing caveats, JarFile opt-in.
Fixed: the earlier text said signing tools may not understand versions; the specification says a multi-release JAR can be signed. It also described `--describe-module ... --release 17` and an `enableMultiRelease` system property, neither of which appears in the pages read.
Removed (not in the pages read): the Gradle snippet, the Maven `compileSourceRoots` XML, VarHandle/Cleaner/StackWalker examples, shading-tool and obfuscator claims, the `new JarFile(f, true, ZIP_READ, Runtime.version())` call, and `getProtectionDomain`.
Method: documentation only; no commands were run.
