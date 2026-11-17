---
id: computing-software.software-engineering.java.nio-files-walk-list-and-streaming
name: nio-files-walk-list-and-streaming
category: computing-software
field: software-engineering
product: java
tags: [java, java-io-nio, files-walk, files-lines, files-list, path, atomic-move, try-with-resources]
level: practitioner
status: docs-checked
description: "Use java.nio.file.Files for reading, writing, listing and walking trees; close the lazy streams, understand ATOMIC_MOVE semantics, symlink loops and UncheckedIOException."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/Files.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/Path.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIO.2 Files: read, write, list, walk

## Whole-file and line APIs
```java
Path p = Path.of("data", "in.txt");
String text = Files.readString(p);                  // decodes as UTF-8
List<String> all = Files.readAllLines(p);           // reads all lines into a List
try (Stream<String> lines = Files.lines(p)) {       // lazy; the stream holds an open file
    lines.filter(l -> !l.isBlank()).forEach(System.out::println);
}
Files.writeString(p, text);                         // default options: CREATE, TRUNCATE_EXISTING, WRITE
```
- `Files.lines` populates lazily and "must be used within a try-with-resources statement or similar" so the open file is closed. Later I/O errors, and malformed or unmappable bytes, surface as `UncheckedIOException` from the stream method that read. The file must not be modified during the terminal operation or the result is undefined.
- For large files read incrementally with `Files.newBufferedReader(p)` (UTF-8 by default).

## Directory listing and walking
```java
try (Stream<Path> s = Files.list(dir)) { ... }                    // one level, not recursive
try (Stream<Path> s = Files.walk(root, 3, FileVisitOption.FOLLOW_LINKS)) { ... }
try (Stream<Path> s = Files.find(root, 10, (path, attrs) -> attrs.isRegularFile() && path.toString().endsWith(".log"))) { ... }
Files.walkFileTree(root, new SimpleFileVisitor<>() {
    @Override public FileVisitResult visitFile(Path f, BasicFileAttributes a) throws IOException {
        Files.delete(f); return FileVisitResult.CONTINUE; }
    @Override public FileVisitResult postVisitDirectory(Path d, IOException e) throws IOException {
        Files.delete(d); return FileVisitResult.CONTINUE; }
});
```
- `list`, `walk` and `find` return streams that hold open directories; close them (try-with-resources). Operating on a closed stream acts as if the end was reached.
- The streams are weakly consistent: they do not freeze the directory and may or may not reflect later changes.
- `walk` is depth-first, always includes the start file, and does not follow symbolic links unless `FOLLOW_LINKS` is passed. With `FOLLOW_LINKS` a directory cycle is treated as an I/O error with a `FileSystemLoopException`. `maxDepth` 0 visits only the start file; a negative value throws `IllegalArgumentException`.
- An `IOException` that happens while accessing a directory after the method returned is wrapped in `UncheckedIOException` thrown from the stream operation that caused it. Use `walkFileTree` with a visitor when you want to handle per-file failures yourself.
- `find` walks like `walk` and may be more efficient than `walk().filter(...)` because it avoids re-reading `BasicFileAttributes`.
- `Files.delete` of a directory requires it to be empty; the Javadoc says it can be used with `walkFileTree` to delete a whole tree.

## Safe writes with move
Write to a temporary file in the target directory, then `Files.move(tmp, target, StandardCopyOption.ATOMIC_MOVE)`.
- With `ATOMIC_MOVE` all other options are ignored, so adding `REPLACE_EXISTING` has no effect. If the target already exists it is implementation specific whether it is replaced or an `IOException` is thrown.
- If the move cannot be atomic (for example the target is on a different file store) `AtomicMoveNotSupportedException` is thrown.
- A non-atomic move that fails with `IOException` leaves the state of both files undefined.

## Gotchas
- `Path.resolve(other)` returns `other` itself when it is absolute; use `normalize()` and `startsWith(base)` to check that an untrusted name stays under a base directory.
- `Files.exists` is "immediately outdated": a later access may still fail, so for security-sensitive code attempt the operation and handle the exception.

## Verify
Walk a small temp directory tree and assert the set of relative paths found; check that the stream is closed by running the walk inside try-with-resources.

## Checked
2026-11-03. Confirmed against the Java SE 21 pages for Files and Path: readString/readAllLines/lines/writeString defaults, try-with-resources requirement, weak consistency, FOLLOW_LINKS and FileSystemLoopException, maxDepth rules, UncheckedIOException wrapping, find vs walk, move/ATOMIC_MOVE rules, delete of directories, resolve with absolute argument, exists remark.
Fixed: the earlier example passed `ATOMIC_MOVE, REPLACE_EXISTING`; ATOMIC_MOVE ignores all other options and replacing an existing target is implementation specific.
Removed (not in the pages read): `AccessDeniedException` as the cause of walk failures, "directory entries have no defined order", the Windows file-lock remark, the `@TempDir` JUnit suggestion, and the dev.java source.
Method: documentation only; no commands were run.
