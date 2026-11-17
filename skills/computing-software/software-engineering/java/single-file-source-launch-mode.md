---
id: computing-software.software-engineering.java.single-file-source-launch-mode
name: single-file-source-launch-mode
category: computing-software
field: software-engineering
product: java
tags: [java, jdk-dev-tools, source-file-mode, shebang-scripts, jep-330, jep-458, multi-file-source]
level: practitioner
status: docs-checked
description: "Run Java source with 'java Foo.java' (JEP 330), shebang scripts, class path options, and the multi-file source launch of Java 22 (JEP 458)."
sources: ["https://openjdk.org/jeps/330", "https://openjdk.org/jeps/458", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-file source launch mode

## Basics (JDK 11, JEP 330)
```bash
java Hello.java arg1 arg2                 # compiles into memory, runs the first top-level class found in the file
java --class-path 'libs/*' Tool.java      # compiler-relevant options go before the source file
java --enable-preview --source 21 Demo.java
```
- Source-file mode is selected when the launcher is given a name that is an existing file with the `.java` extension. Arguments after the file name go to `main`.
- The class run is the first top-level class in the file; it must declare `public static void main(String[])`. Put the class with `main` first.
- Options before the source file that matter to compilation are used: `--class-path`, `--module-path`, `--add-exports`, `--add-modules`, `--limit-modules`, `--patch-module`, `--upgrade-module-path` and `--enable-preview`. `--source` specifies the source version, is used as an implicit `--release`, and must accompany `--enable-preview`.
- The code is compiled in the context of an unnamed module; classes are held in memory and loaded by a custom class loader. Annotation processing is disabled (as if `-proc:none`).
- It is an error if a class on the application class path has the same name as the class to be executed. Classes on the class path cannot refer to classes declared in the source file.
- Requires the `jdk.compiler` module.

## Shebang scripts
```java
#!/usr/bin/java --source 21
public class Greet { public static void main(String[] a) { System.out.println("hi " + a[0]); } }
```
Save as `greet` (no `.java` extension), mark it executable and run `./greet world`. The first two bytes must be `#!`; the `java` path in the line is system specific. The `--source` option is required in a shebang file when the file name does not follow Java source naming conventions or when you add VM options on the first line (put `--source` first after the executable). A file with a standard `.java` name must not be run through the shebang mechanism. Run it explicitly with `java --source 21 greet` if needed.

## Multi-file programs (JDK 22, JEP 458)
- `java Prog.java` now finds other classes the program refers to as `.java` files in the source tree and compiles them in memory too; the order and timing of compilation is not guaranteed (some code may be compiled lazily).
- The tree must follow the package layout: files in the root directory declare the unnamed package, files in `foo/bar` declare package `foo.bar`. The root is computed from the initial file's package and path; a mismatch makes the launch fail.
- If the root contains a `module-info.java`, the program is modular and its classes live in the named module (this is allowed; the program is not limited to the unnamed module).
- Duplicate class names across the files are prohibited. Extra file names on the command line are just arguments to `main`.
- If a class exists both in the source tree and on the class path, the source tree version is preferred. Pre-compiled classes cannot refer to classes compiled in memory.
- Before JDK 22 only the single launched file is compiled.

## Verify
`java Hello.java` runs without producing a `.class` file next to the source; on JDK 22 or later a `Prog.java` that references `Helper.java` in the same directory runs without a separate `javac`.

## Checked
2026-11-03. Confirmed against JEP 330, JEP 458 and the Java SE 21 `java` man page: source-file mode selection, first top-level class, option scanning, `--source` rules, unnamed module, annotation processing off, shebang rules, multi-file lookup, package/directory layout, module-info handling, duplicate-class rule, source-tree preference.
Fixed: the earlier text said the multi-file launcher is limited to sources without a `module-info`; JEP 458 says a `module-info.java` in the root makes the program modular. Also the earlier text said sibling files are found in the "same directory tree" without the package-layout rule, and used `/usr/bin/env java --source` in the shebang (JEP shows `#!/path/to/java --source version`).
Removed (not in the pages read): compact source files and instance main (JEPs 445/463/477/495), the 0.3-0.5 s startup figure, JBang, `-Xlint`/`@argfiles` advice, the `CLASSPATH` environment variable note, the `System.console()` remark, and the `java --release` / `ls *.class` verify step.
Method: documentation only; no commands were run.
