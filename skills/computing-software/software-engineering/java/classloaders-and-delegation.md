---
id: computing-software.software-engineering.java.classloaders-and-delegation
name: classloaders-and-delegation
category: computing-software
field: software-engineering
product: java
tags: [java, java-jvm-internals, classloader-delegation, classloader, noclassdeffounderror, classnotfoundexception, verbose-class, thread-context-classloader]
level: advanced
status: docs-checked
description: "How Java class loading delegates: built-in loaders, loadClass order, findClass overrides, parallel-capable loaders and the loader lock."
sources:
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ClassLoader.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class loaders and delegation

## Built-in loaders (Java 9+)
- **Bootstrap**: the VM's built-in loader, typically represented as `null`, with no parent.
- **Platform**: loads platform classes (Java SE APIs, their implementation classes and JDK-specific run-time classes). It can be a parent of your own `ClassLoader` (`ClassLoader.getPlatformClassLoader()`).
- **System (application)**: distinct from the platform loader; typically defines classes on the class path, module path and for JDK tools. The platform loader is its parent or ancestor, so it reaches platform classes by delegating.
- A new `ClassLoader` created without an explicit parent uses `getSystemClassLoader()` as its parent.

## Delegation order
`ClassLoader` uses a delegation model: each instance has a parent and usually asks it before searching itself. The default `loadClass(String, boolean)` does, in order:
1. `findLoadedClass(String)` to see whether it is already loaded.
2. `loadClass` on the parent; if the parent is `null`, the VM's built-in loader.
3. `findClass(String)` to find the class itself.
4. If found and `resolve` is true, `resolveClass`.

Subclasses are encouraged to override `findClass`, not `loadClass`. A failure surfaces as `ClassNotFoundException` from `loadClass`.

## Concurrency
- By default `loadClass` synchronises on the result of `getClassLoadingLock(name)` for the whole load.
- A loader that supports concurrent loading is "parallel capable" and must register itself in its class initialiser with `ClassLoader.registerAsParallelCapable`. `ClassLoader` itself is registered, but subclasses must register themselves.
- If delegation is not strictly hierarchical, loaders need to be parallel capable, otherwise class loading can deadlock because the loader lock is held for the entire load. Parallel-capable loaders can override `getClassLoadingLock` for finer-grained locking.
- If a loader is created with a `null` parent, there is no guarantee that all platform classes are visible to it.

## Verify
- [ ] Write a small loader that overrides `findClass`, and check `loadClass` still prefers the parent for a class the parent also has.

## Checked
Method: docs-checked 2026-11-09 against the java.lang.ClassLoader Javadoc (Java 21). Dropped the unconfirmed material on error diagnosis (NoClassDefFoundError, LinkageError), -verbose:class and -Xlog flags, jcmd classloader commands, thread context class loader, servlet container behaviour and leak patterns, and the JVMS chapter 5 source, which was not read.
