---
id: computing-software.software-engineering.groovy.file-io-gdk
name: file-io-gdk
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, file-io-gdk, groovy-gdk-io]
level: practitioner
status: docs-checked
description: "GDK methods on java.io.File: text property, append with <<, eachLine, withWriter, eachFileRecurse, readLines, getBytes, deleteDir."
sources:
  - https://groovy-lang.org/groovy-dev-kit.html
  - https://github.com/apache/groovy/blob/master/src/main/java/org/codehaus/groovy/runtime/ResourceGroovyMethods.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File and stream GDK methods
These are Groovy Development Kit methods added to `java.io.File` (class `ResourceGroovyMethods`):
- `file.text` reads the whole file as a String (`getText(File)`); `getText(File, String charset)` reads with the charset you name.
- `file.text = '...'` writes via `setText(File, String)`.
- `file << 'more'` appends (`leftShift(File, ...)`).
- `file.readLines()` returns a `List<String>`; `file.bytes` is `getBytes(File)`.
- `file.eachLine { }` iterates lines; `file.withWriter('UTF-8') { writer -> ... }` opens a writer with a charset and closes it when the closure ends.
- `dir.eachFileRecurse(groovy.io.FileType.FILES) { f -> ... }` walks a directory tree.
- `dir.deleteDir()` deletes a directory recursively and returns a boolean.

## Gotchas
- Pass an explicit charset (`getText(charset)`, `withWriter(charset)`) rather than relying on the platform default.

## Checked

2026-11-03. Confirmed against the `ResourceGroovyMethods` source (signatures of `getText`, `setText`, `leftShift`, `readLines`, `getBytes`, `deleteDir`, `withWriter`, `eachFileRecurse`) and the Groovy Development Kit page (I/O section). Removed: the code snippet and self-check, the `Path` GDK claim, and the claim that the default charset is the platform one.

Method: documentation only; no commands were run.
