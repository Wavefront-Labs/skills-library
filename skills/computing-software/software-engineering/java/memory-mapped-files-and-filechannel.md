---
id: computing-software.software-engineering.java.memory-mapped-files-and-filechannel
name: memory-mapped-files-and-filechannel
category: computing-software
field: software-engineering
product: java
tags: [java, java-io-nio, memory-mapped-files, filechannel, mappedbytebuffer, transferto, foreign-memory]
level: advanced
status: docs-checked
description: "Use FileChannel.transferTo for file copies and map() / MappedByteBuffer for large files; know the Integer.MAX_VALUE size limit, GC-bound unmapping and the Arena-based alternative."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/channels/FileChannel.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/MappedByteBuffer.html", "https://openjdk.org/jeps/454"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory-mapped files and FileChannel

## transferTo
```java
try (var in = FileChannel.open(src, StandardOpenOption.READ);
     var out = FileChannel.open(dst, StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {
    long pos = 0, size = in.size();
    while (pos < size) pos += in.transferTo(pos, size - pos, out);
}
```
`transferTo` may or may not transfer all requested bytes, so loop on the return value. It does not modify the source channel's position, transfers nothing if `position` is at or beyond the file size, and is "potentially much more efficient" than a read/write loop because many operating systems can transfer directly from the filesystem cache. (`src` and `dst` are placeholder `Path` values.)

## Mapping
```java
try (FileChannel ch = FileChannel.open(path, StandardOpenOption.READ, StandardOpenOption.WRITE)) {
    MappedByteBuffer mb = ch.map(FileChannel.MapMode.READ_WRITE, 0, ch.size());
    mb.putInt(0, 42);
    mb.force();                       // write changes to the storage device holding the mapped file
}
```
- Modes: `READ_ONLY` (writes throw `ReadOnlyBufferException`), `READ_WRITE` (changes eventually propagate to the file), `PRIVATE` (copy-on-write, never propagated). The channel must be open for reading for read-only, and for reading and writing for the other modes, otherwise `NonReadableChannelException` / `NonWritableChannelException`.
- Closing the channel does not affect the mapping.
- Javadoc: mapping costs more than reading or writing a few tens of kilobytes, so it is generally only worth it for relatively large files.
- `force()` guarantees, for a file on a local storage device, that changes since creation or the last `force` have been written to that device.

## Limits and hazards
- `size` must be non-negative and no greater than `Integer.MAX_VALUE`; map several regions for larger files.
- The buffer and its mapping remain valid until the buffer itself is garbage-collected; there is no explicit unmap on `MappedByteBuffer`.
- Much about mapped files is OS dependent and unspecified: behaviour when the region is not fully inside the file, whether changes to the file's content or size reach the buffer, and how fast buffer changes reach the file. The content of a mapped buffer can change at any time if the file region is changed by this or another program.
- Alternative: in Java 21 the overload `FileChannel.map(MapMode, long offset, long size, Arena)` returning a `MemorySegment` is a preview API (needs preview features enabled). The returned segment is unmapped when a closeable arena is closed. The Foreign Function and Memory API (JEP 454) is final in Java 22 and motivates this with deterministic deallocation. A mapped segment can become inaccessible, for example if the file is truncated, and then throws an unspecified exception; avoid modifying a mapped file except through its mapped content.

## Verify
Map a temp file, write, call `force()`, then read the file with a normal read and confirm the data persisted.

## Checked
2026-11-03. Confirmed against the Java SE 21 pages for FileChannel and MappedByteBuffer and JEP 454: transferTo semantics, map modes and exceptions, GC-bound validity, unspecified OS behaviour, force guarantee, size limit, performance remark, preview status of the Arena overload in 21 and final FFM API in 22.
Removed (not in the pages read): the `ByteBuffer.allocateDirect` read loop, "positional reads are thread-safe", SIGBUS / `InternalError`, Windows file lock and delete-failure claims, virtual-thread carrier remark, `-XX:MaxDirectMemorySize`, `jcmd` / BufferPool verification, and "64-bit offsets" wording.
Method: documentation only; no commands were run.
