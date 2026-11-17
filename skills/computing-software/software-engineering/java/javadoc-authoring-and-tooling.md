---
id: computing-software.software-engineering.java.javadoc-authoring-and-tooling
name: javadoc-authoring-and-tooling
category: computing-software
field: software-engineering
product: java
tags: [java, java-modules-packaging, javadoc-authoring, javadoc, doclint, markdown-doc-comments, api-documentation]
level: practitioner
status: draft
description: "Write useful Javadoc: summary sentence, @param/@return/@throws, {@code} and {@link}, package-info, doclint errors, JDK 23 Markdown comments, and the Maven/Gradle javadoc tasks."
sources: ["https://docs.oracle.com/en/java/javase/21/javadoc/javadoc.html", "https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html", "https://openjdk.org/jeps/467"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Javadoc authoring

```java
/**
 * Computes the shipping cost for an order.
 *
 * <p>Free shipping applies when the subtotal is at least {@value #FREE_THRESHOLD}.
 *
 * @param order the order to price; must not be {@code null}
 * @return the cost in minor units, never negative
 * @throws IllegalArgumentException if the order has no items
 * @see ShippingZone
 * @since 2.1
 */
public long cost(Order order) { ... }
```
## Style
- First sentence is a summary shown in listings; end it with a period. Describe behaviour and contract (preconditions, thread-safety, nullability, units), not the implementation.
- `{@code List<String>}` for code, `{@link Order#total()}` for navigable references, `<pre>{@code ...}</pre>` for examples, `{@snippet}` (JDK 18+) for compiled, highlightable examples from `snippet-files`.
- Document exceptions callers should handle; mark deprecation with both `@Deprecated(since=..., forRemoval=...)` and `@deprecated` explaining the replacement.
- `package-info.java` (and `module-info.java`) carry package and module overviews.
- JDK 23 (JEP 467) allows Markdown comments with `///` lines.

## Tooling
```bash
mvn javadoc:javadoc                   # target/site/apidocs;  mvn javadoc:jar for Central
./gradlew javadoc
javadoc -Xdoclint:all -d out $(find src/main/java -name '*.java')
```
Doclint rejects malformed HTML, bad `@param` names and missing comments depending on `-Xdoclint` groups; use `-Xdoclint:all,-missing` to enforce correctness without demanding comments everywhere. For Central, the javadoc jar is mandatory (can be a minimal jar for internal-only classes).

## Gotchas
- Self-closing tags such as `<p/>` and unescaped `<`, `>`, `&` break doclint; use `{@code}` or `&lt;`.
- Links to external APIs need `-link https://docs.oracle.com/en/java/javase/21/docs/api/` (offline fails the build).
- Javadoc on private members is skipped unless `-private`.
- Stale comments are worse than none; review them in PRs when signatures change.

## Verify
`javadoc -Xdoclint:all` exits 0; open `apidocs/index.html` and check the summary of the main class reads well.
