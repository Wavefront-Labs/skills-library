---
id: computing-software.software-engineering.java.deserialization-filters-and-serialization-risks
name: deserialization-filters-and-serialization-risks
category: computing-software
field: software-engineering
product: java
tags: [java, java-io-nio, deserialization-filter, objectinputfilter, java-serialization, gadget-chains, jep-290, serializable]
level: advanced
status: docs-checked
description: "Reduce Java deserialization attack surface: avoid ObjectInputStream on untrusted data, set a JVM-wide ObjectInputFilter allow-list, and migrate to JSON."
sources: ["https://openjdk.org/jeps/290", "https://openjdk.org/jeps/415", "https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deserialization filters and serialization risks (defensive)

Java native serialization reconstructs object graphs from bytes. OWASP notes that attacks on deserializers have enabled denial of service, access-control bypass and remote code execution, and that further "gadget" classes will keep being found. Avoid it for untrusted data, then filter.

## 1. Remove it
Prefer a data format such as JSON with explicit schemas for anything crossing a trust boundary. OWASP notes that fixing the problem may mean re-architecting messaging so serialized objects are no longer accepted.

## 2. Filter what remains (JEP 290, delivered in Java 9)
A filter is called for each class in the stream (before instantiation), for each array length, and for depth, reference count and stream length. It returns accepted, rejected or undecided. It is not called for primitives or `java.lang.String` instances encoded concretely, so bound the input size separately.

Process-wide filter via the `jdk.serialFilter` system property (which supersedes the security property of the same name in `conf/security/java.security`):
```bash
java -Djdk.serialFilter='com.acme.model.*;java.base/*;!*' -jar app.jar
```
Pattern rules (JEP 290):
- Patterns are separated by `;`; whitespace is significant.
- Limit patterns contain `=`: `maxdepth`, `maxrefs`, `maxbytes`, `maxarray`. Exceeding a limit rejects; limits are checked before class patterns.
- Class patterns are matched left to right against the class name (arrays use the element type). A leading `!` rejects on match.
- `module/pattern` matches the module name first.
- A trailing `.**` matches the package and all subpackages, `.*` matches the package, `*` matches any class with the given prefix. An exact name matches that class.
- A class matching no pattern is undecided, so end an allow-list with `!*` to reject everything else.

Per-stream filter:
```java
ObjectInputFilter f = ObjectInputFilter.Config.createFilter("com.acme.model.*;maxdepth=<n>;!*");
ois.setObjectInputFilter(f);
```
If no filter is set on the stream, the global filter is used. JEP 415 (Java 17) adds a JVM-wide filter factory (`ObjectInputFilter.Config.setSerialFilterFactory`, or the `jdk.serialFilterFactory` property, which must be set before the first deserialization) that chooses a filter per stream from context.

## 3. Operations
- Filter actions are logged to the `java.io.serialization` logger if logging is enabled; use it to discover legitimate classes before enforcing.
- Keep dependencies patched, since gadget classes come from libraries on the classpath.
- Search the codebase for `new ObjectInputStream`, `readObject(`, RMI endpoints and JMX exposed to networks.

## Gotchas
- OWASP: filtering does not make arbitrary untrusted deserialization safe.
- Backporting JEP 290 to older releases needs implementation-specific APIs, so do not assume the same API on Java 8.

## Verify
Feed the app a serialized instance of a non-listed class in a test and assert the read fails with the filter's rejection.

## Checked
2026-11-09. Confirmed against JEP 290, JEP 415 and the OWASP Deserialization Cheat Sheet: filter call points and statuses, jdk.serialFilter property and precedence, limit names, the pattern grammar (including the `.*`, `.**` and `*` forms), per-stream and factory APIs, the logger name, the string/primitive exemption, the backport note.
Removed: the wrong claim that a `*` suffix means a package (it is a prefix match; `.*` is the package form), the 8u121 backport claim, the records-canonical-constructor claim, the DEBUG log-level and java.util.* claims, serialVersionUID remark, the quoted exception text and the concrete limit numbers. The Oracle serialization-filtering page returned only a landing stub and was dropped as a source.
Method: documentation only; no commands were run.
