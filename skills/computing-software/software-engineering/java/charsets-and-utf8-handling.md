---
id: computing-software.software-engineering.java.charsets-and-utf8-handling
name: charsets-and-utf8-handling
category: computing-software
field: software-engineering
product: java
tags: [java, java-strings-text, charset-utf8-encoding, utf-8, standardcharsets, default-charset, mojibake, jep-400]
level: practitioner
status: docs-checked
description: "Never rely on the platform charset: pass StandardCharsets.UTF_8 explicitly, understand JEP 400 (UTF-8 default in Java 18+), and the COMPAT escape hatch."
sources: ["https://openjdk.org/jeps/400", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/charset/StandardCharsets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Charsets and UTF-8 handling

**Goal:** bytes in and out of Strings with an explicit, known encoding.

## Rules
1. Always pass a charset where the API allows one, using the constant `StandardCharsets.UTF_8` rather than a name string. JEP 400 notes that the standard file and text APIs allow a charset argument, and that the old no-charset constructors (`InputStreamReader`, `FileReader`, `OutputStreamWriter`, `FileWriter`, `PrintStream`) use the default charset.
2. Version behaviour: up to JDK 17 the default charset was chosen from the operating system, locale and other factors, so the same `FileReader("hello.txt")` code gave different text on macOS and Windows. From JDK 18 (JEP 400) the default charset is UTF-8, and `Charset.defaultCharset()` returns it.
3. The `java.nio.file.Files` methods that read or write files without a `Charset` argument are specified to always use UTF-8 on every version. Mixing them with older default-charset APIs is a hazard on JDK 17 and earlier.
4. `System.out` and `System.err` are not covered by the default charset: their charset is whatever `Console.charset()` specifies.

## Configuration
- `-Dfile.encoding=COMPAT` restores the JDK 17 and earlier behaviour (environment-dependent default). `-Dfile.encoding=UTF-8` is a no-op on JDK 18+, kept so existing command lines keep working. Other values are unspecified. Setting the property programmatically after startup does not work.
- Before moving to JDK 18+, run the application on your current JDK (8 to 17) with `-Dfile.encoding=UTF-8` to find charset issues early; compile with `javac -encoding UTF-8` for the same reason.
- `Charset.forName("default")` throws `UnsupportedCharsetException` from JDK 18.
- When different JDK versions exchange text files, the older side can use `-Dfile.encoding=UTF-8` or the newer side `-Dfile.encoding=COMPAT`.

## Verify
Round-trip a non-ASCII string through your reader and writer with an explicit charset, and run the same test on Windows and Linux CI.

## Checked
Checked 2026-11-08 against JEP 400 (UTF-8 by Default) in full and the StandardCharsets API page (constants only, a short page).
Removed because they were not confirmed in those pages: the strict `CharsetDecoder` example, code-point counting and Normalizer advice, HTTP and Servlet header notes, ResourceBundle and `Properties.load` encodings, and the `stdout.encoding` Java 19+ remark. The dev.java strings page is JavaScript-only and could not be read, so it is no longer cited.
Method: documentation only; no commands were run.
