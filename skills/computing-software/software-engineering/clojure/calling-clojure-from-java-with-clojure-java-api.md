---
id: computing-software.software-engineering.clojure.calling-clojure-from-java-with-clojure-java-api
name: calling-clojure-from-java-with-clojure-java-api
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, embedding, java-api, clojure-java-api, require, var, invoke, interop, library, embedding-from-java, clojure-embedding]
level: advanced
status: docs-checked
description: "Call Clojure functions from Java using clojure.java.api.Clojure (var, read) and clojure.lang.IFn: look up vars, require namespaces, invoke, and deref non-function vars."
sources: ["https://clojure.org/reference/java_interop#_calling_clojure_from_java"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling Clojure from Java

**Goal:** use a Clojure library inside a Java application.

```java
import clojure.java.api.Clojure;
import clojure.lang.IFn;

IFn require = Clojure.var("clojure.core", "require");
require.invoke(Clojure.read("my.app.core"));
IFn greet = Clojure.var("my.app.core", "greet");
Object out = greet.invoke("world");
IFn map = Clojure.var("clojure.core", "map");
IFn inc = Clojure.var("clojure.core", "inc");
Object r = map.invoke(inc, Clojure.read("[1 2 3]"));
```
- The `clojure.java.api` package is a minimal interface to bootstrap Clojure from other JVM languages: it looks
  up a Var by namespace (giving an `IFn`) and reads data with the EDN reader (`Clojure.read`).
- The public Java API is `clojure.java.api.Clojure` and `clojure.lang.IFn`; treat other Java classes as
  implementation details.
- Functions in `clojure.core` are loaded automatically; other namespaces are loaded with `require`, which you
  also obtain through `Clojure.var`.
- Libraries written in Clojure are usable once their source or compiled form is on the classpath.
- Functions can be passed to higher-order functions (as `inc` is passed to `map` above).
- Most IFns refer to functions; for Vars holding plain data (such as `*print-length*`) call `deref` instead of
  `invoke`.

## Self-check
Write a 10-line Java main that requires a namespace and calls a function; run with `java -cp`.

## Checked
Method: 2026-11-08 read the Calling Clojure From Java section of clojure.org/reference/java_interop. Removed unsupported claims: startup cost figure, gen-class alternative, Java-interface view of collections and PersistentVector.create, classloader guidance, ExceptionInfo, the failure modes, and the "unbound var if not required" claim. The example code matches the documented pattern but was not compiled.
