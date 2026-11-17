---
id: computing-software.software-engineering.java.jpms-modules-and-jlink
name: jpms-modules-and-jlink
category: computing-software
field: software-engineering
product: java
tags: [java, java-build, jpms, jlink, module-info, java-modules, jdeps, custom-runtime]
level: practitioner
status: docs-checked
description: "Use the Java Platform Module System: module-info exports/requires, strong encapsulation errors, jdeps analysis, and building small custom runtimes with jlink."
sources:
  - https://docs.oracle.com/en/java/javase/21/docs/specs/man/jlink.html
  - https://docs.oracle.com/en/java/javase/21/docs/specs/man/jdeps.html
  - https://docs.oracle.com/javase/specs/jls/se21/html/jls-7.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Java Platform Module System and jlink

**Goal:** explicit module boundaries where they pay off, and minimal runtime images for deployment, without fighting reflection-heavy frameworks.

## 1. module-info.java
```java
module com.acme.orders {
    requires java.net.http;
    requires transitive com.acme.money;     // consumers of orders get money too
    requires static lombok;                  // mandatory at compile time, optional at run time
    exports com.acme.orders.api;             // only this package is visible
    exports com.acme.orders.spi to com.acme.plugins;
    opens com.acme.orders.model to com.fasterxml.jackson.databind;   // deep reflection
    uses com.acme.orders.spi.PriceRule;
    provides com.acme.orders.spi.PriceRule with com.acme.orders.internal.DefaultRule;
}
```
- `exports` = compile-time and public access; `opens` = runtime deep reflection (frameworks needing private field access).

## 2. Classpath vs module path
Most applications can keep using the classpath. Check the Java Platform Module System documentation on dev.java for how unnamed and automatic modules behave before moving jars to the module path.

## 3. Strong encapsulation errors
Reflection into JDK internals fails when the package is not opened. Fix by upgrading the library; the temporary workaround is the java launcher option `--add-opens module/package=target-module(,target-module)*`, for example `--add-opens java.base/java.lang=ALL-UNNAMED`. Find internal API use with `jdeps --jdk-internals app.jar` (`-jdkinternals` is the short form).

## 4. Custom runtime with jlink
```bash
jdeps --ignore-missing-deps --print-module-deps --multi-release 21 --class-path 'lib/*' app.jar
# -> java.base,java.logging,java.net.http,java.sql
jlink --add-modules java.base,java.logging,java.net.http,java.sql \
      --strip-debug --no-man-pages --no-header-files --compress=2 \
      --output build/runtime
build/runtime/bin/java -cp 'app.jar:lib/*' com.acme.Main
```
The jlink page documents `--compress={0|1|2}` in JDK 21. Service-provider modules such as `jdk.crypto.ec` and `jdk.localedata` are not pulled in by `jdeps` output alone; add them if needed. A missing module fails only at runtime.

## Gotchas
- Spring, Hibernate and many frameworks rely on reflection and classpath scanning; full modularisation of such apps is costly. Use jlink with a classpath app instead.

## Verify
- `java --list-modules` on the jlink image lists only the intended modules, and the app's integration tests pass on that image (exercise TLS, locales and JDBC paths).

## Checked
2026-11-01. Confirmed against the JDK 21 jlink and jdeps man pages and the java command page: jlink
`--add-modules`, `--strip-debug`, `--no-man-pages`, `--no-header-files`, `--output`, `--compress={0|1|2}`;
jdeps `--print-module-deps`, `--ignore-missing-deps`, `--jdk-internals`; java `--add-opens` syntax.
Fixed `--compress=zip-6` to `--compress=2`. Removed unconfirmed claims: runtime size figures, the JDK 17
encapsulation date, automatic-module naming, split-package rule, the Maven, Gradle and jpackage
section, resource and ServiceLoader gotchas, and two source links not fetched. The module-info
syntax block was checked against JLS SE 21 chapter 7 (requires transitive and static, qualified exports, opens and reflective access, uses and provides); requires static corrected to "optional at run time" wording.
Method: documentation only; no commands were run.
