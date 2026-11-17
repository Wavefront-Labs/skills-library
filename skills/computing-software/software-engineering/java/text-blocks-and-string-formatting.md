---
id: computing-software.software-engineering.java.text-blocks-and-string-formatting
name: text-blocks-and-string-formatting
category: computing-software
field: software-engineering
product: java
tags: [java, text-blocks, string-formatting, formatted, stringbuilder, string-methods, modern-java]
level: practitioner
status: docs-checked
description: "Work with Java strings well: text blocks and their indentation rules, formatted()/String.format, StringBuilder, modern String methods, equality and Unicode pitfalls."
sources: ["https://docs.oracle.com/en/java/javase/21/text-blocks/index.html", "https://openjdk.org/jeps/378", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Formatter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text blocks and string formatting

**Goal:** readable multi-line literals (SQL, JSON, HTML) and correct string building.

## Text blocks (final in Java 15, JEP 378)
```java
String sql = """
    SELECT id, email
    FROM users
    WHERE status = ?
    """;
```
- The opening `"""` is followed by optional white space and then a line terminator; content starts on
  the next line.
- The compiler normalises line terminators to LF and removes incidental white space: the same amount of
  leading white space is removed from every line until at least one line has a non-white-space
  character in the leftmost position. The position of the opening `"""` has no effect, but the closing
  `"""` does when it sits on its own line: move it left to keep leading spaces.
- Incidental white space at line ends is removed too. `String::indent` can adjust indentation after.
- The content ends before the closing delimiter, so put the closing `"""` on the last content line if
  you do not want a final line terminator.
- Line terminators may appear directly in the content; `\n` is allowed but not necessary.

## Formatting
```java
String msg = "User %s has %d items".formatted(name, n);
```
`String.formatted(Object...)` formats like `String.format`. Format strings follow `java.util.Formatter`.
Pass an explicit `Locale` for machine-readable output (the default locale can change number formats).
Never build SQL with `formatted`; use query parameters.

## Useful String methods
`formatted`, `isBlank`, `strip`, `stripIndent`, `lines`, `repeat`, `indent`, `transform` are all
methods of `java.lang.String` in the JDK 21 API.

## Verify
- [ ] Machine-facing formatting passes an explicit `Locale`.
- [ ] Text block output checked in tests (indentation and trailing newline as intended).

## Checked
2026-11-01. Confirmed against JEP 378 (Java 15 delivery, opening and closing delimiter rules, line
terminator normalisation, re-indentation algorithm, closing-delimiter effect, `String::indent`) and the
JDK 21 String API (method list). Removed unconfirmed claims: the `\s` and line-continuation escapes,
the quote-escaping rule, StringConcatFactory since Java 9, StringBuilder/StringJoiner advice, the
Turkish locale and German decimal examples, UTF-16 length, BreakIterator and Normalizer notes.
Method: documentation only; no commands were run.
