---
id: computing-software.software-engineering.csharp-dotnet.async-file-io-and-filestream
name: async-file-io-and-filestream
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-io, async-file-io, filestream, file-readalllinesasync, useasync, atomic-writes]
level: practitioner
status: docs-checked
description: "Do file I/O in .NET asynchronously and safely: File.*Async helpers, FileStream with FileStreamOptions, streaming large files, File.Replace for safe swaps, and sharing modes."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/io/", "https://learn.microsoft.com/en-us/dotnet/api/system.io.filestream", "https://learn.microsoft.com/en-us/dotnet/api/system.io.file.replace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async file I/O

```csharp
// small files
string text = await File.ReadAllTextAsync(path, ct);
await File.WriteAllLinesAsync(path, lines, ct);

// large files: stream, do not load everything
await using var fs = new FileStream(path, new FileStreamOptions {
    Mode = FileMode.Open, Access = FileAccess.Read, Share = FileShare.Read,
    Options = FileOptions.Asynchronous | FileOptions.SequentialScan, BufferSize = 4096 });
using var reader = new StreamReader(fs, Encoding.UTF8);
while (await reader.ReadLineAsync(ct) is { } line) Process(line);

// raw copy
await using var dst = File.Create(target);
await fs.CopyToAsync(dst, 81920, ct);
```
## What the docs state
- System.IO supports reading and writing synchronously and asynchronously; asynchronous members have `Async` in the name (`CopyToAsync`, `FlushAsync`, `ReadAsync`, `WriteAsync`) and are used with `async`/`await`. Do large transfers asynchronously when the app must stay responsive.
- `FileStream` supports both synchronous and asynchronous reads and writes, has a constructor taking `FileStreamOptions`, and exposes `IsAsync` (whether the handle is configured for asynchronous I/O). It has overloads taking buffer size, `FileShare` and `FileOptions`.
- If the handle position changes unexpectedly, a `Read` discards the buffer and rereads (a performance cost); a `Write` discards the buffer and throws `IOException`.
- Always provide robust exception handling around filesystem calls. Use `Path` for cross-platform path processing.
- `File.Replace(source, destination, backup)` replaces the destination's contents with the source's, deletes the source and keeps a backup of the replaced file. Source and destination on different volumes raise an exception; a backup on another volume is deleted; pass `null` for no backup; an existing backup is overwritten. `ignoreMetadataErrors` ignores attribute/ACL merge errors.

## Atomic-style writes (practitioner pattern)
Write a temp file in the same directory (same volume, as File.Replace requires), then `File.Replace(temp, path, backup)`. The pages do not claim this is crash-proof; verify on your filesystem.

## Not verified by the cited pages (treat as experience, test it)
- Platform differences in how truly asynchronous file I/O is; `File.OpenHandle` plus `RandomAccess` as lowest-overhead API; `FileShare` default values; `Flush(true)`; LOH behaviour of `ReadAllBytes`; path-traversal and BOM advice.

## Checked
Method: 2026-11-08 docs-only read of the File and Stream I/O overview and File.Replace pages; FileStream reference page grepped for async, share and buffer content. Removed the unsupported Windows-vs-Linux async claim, the .NET 6 rewrite claim, the FileShare-default and Flush(true) claims, and the "never leaves a half-written file" guarantee; added the documented File.Replace volume and backup rules.
