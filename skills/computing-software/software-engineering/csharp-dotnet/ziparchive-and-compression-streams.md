---
id: computing-software.software-engineering.csharp-dotnet.ziparchive-and-compression-streams
name: ziparchive-and-compression-streams
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-io, ziparchive-compression, zipfile, gzipstream, brotli, zip-slip, decompression-bomb]
level: practitioner
status: draft
description: "Create and extract ZIP, GZip and Brotli data in .NET safely: ZipArchive streaming, zip-slip path checks, size limits against decompression bombs, and compression levels."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/io/compress-and-extract-zip-files", "https://learn.microsoft.com/en-us/dotnet/api/system.io.compression.ziparchive", "https://learn.microsoft.com/en-us/dotnet/api/system.io.compression.brotlistream"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ZipArchive and compression streams

```csharp
// create
await using var outFs = File.Create("out.zip");
using (var zip = new ZipArchive(outFs, ZipArchiveMode.Create))
{
    var entry = zip.CreateEntry("data/report.json", CompressionLevel.Optimal);
    await using var es = entry.Open();
    await JsonSerializer.SerializeAsync(es, report);
}
ZipFile.CreateFromDirectory(dir, "dir.zip", CompressionLevel.Fastest, includeBaseDirectory: false);

// extract safely
string root = Path.GetFullPath(destDir) + Path.DirectorySeparatorChar;
using var zin = ZipFile.OpenRead(path);
long total = 0;
foreach (var e in zin.Entries)
{
    string target = Path.GetFullPath(Path.Combine(root, e.FullName));
    if (!target.StartsWith(root, StringComparison.Ordinal)) throw new InvalidDataException("zip-slip");   // ../ entries
    if (e.FullName.EndsWith('/')) { Directory.CreateDirectory(target); continue; }
    if ((total += e.Length) > MaxTotal || e.Length > MaxEntry) throw new InvalidDataException("too large");   // declared size can lie
    Directory.CreateDirectory(Path.GetDirectoryName(target)!);
    e.ExtractToFile(target, overwrite: false);
}

// single-stream formats
await using var gz = new GZipStream(File.Create("a.json.gz"), CompressionLevel.Optimal);
await using var br = new BrotliStream(src, CompressionMode.Decompress);
```
.NET 8 `ZipFile.ExtractToDirectory` checks traversal; with manual loops you must.

## Rules
- Untrusted archives: validate paths, count entries, limit total **actual** decompressed bytes by counting while copying (declared `Length` can be forged), ignore symlink and absolute-path entries, never set permissions from the archive blindly.
- Reading `ZipArchiveMode.Read` over a non-seekable stream buffers it into memory.
- `CompressionLevel.SmallestSize` (.NET 6+) is slow; `Fastest` for logs.
- Brotli for HTTP static text; GZip is universally supported. For ASP.NET response compression see the pipeline skills.

## Gotchas
- Dispose the `ZipArchive` before reading the output file; central directory is written on dispose.
- Entry names use `/`, not `\`.
- Encryption is not supported by `ZipArchive`; use a library.

## Verify
A test archive containing `../evil.txt` must be rejected; a 10 GB-expansion bomb is stopped by the limit; roundtrip equals original bytes.
