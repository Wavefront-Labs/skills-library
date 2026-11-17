---
id: computing-software.software-engineering.csharp-dotnet.system-io-pipelines
name: system-io-pipelines
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-io, io-pipelines, system-io-pipelines, pipereader, readonlysequence, protocol-parsing]
level: advanced
status: docs-checked
description: "Parse network protocols efficiently with System.IO.Pipelines: PipeReader/PipeWriter, ReadOnlySequence<byte> framing, AdvanceTo consumed and examined, and backpressure."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/io/pipelines", "https://learn.microsoft.com/en-us/dotnet/api/system.io.pipelines.pipereader", "https://learn.microsoft.com/en-us/dotnet/standard/io/buffers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System.IO.Pipelines

A `Pipe` couples a writer and a reader with pooled buffers, handling partial reads, buffer management and backpressure for you.

```csharp
static async Task ReadLinesAsync(PipeReader reader, CancellationToken ct)
{
    while (true)
    {
        ReadResult result = await reader.ReadAsync(ct);
        ReadOnlySequence<byte> buffer = result.Buffer;

        while (TryReadLine(ref buffer, out ReadOnlySequence<byte> line))
            Process(line);                                     // frame is complete

        reader.AdvanceTo(buffer.Start, buffer.End);            // consumed = start of unprocessed; examined = end (we've looked at everything)
        if (result.IsCompleted) break;
    }
    await reader.CompleteAsync();
}
static bool TryReadLine(ref ReadOnlySequence<byte> buf, out ReadOnlySequence<byte> line)
{
    var pos = buf.PositionOf((byte)'\n');
    if (pos is null) { line = default; return false; }
    line = buf.Slice(0, pos.Value);
    buf = buf.Slice(buf.GetPosition(1, pos.Value));
    return true;
}
```
`PipeReader.Create(stream)` and `PipeWriter.Create(stream)` adapt streams. `ReadOnlySequence<T>` can represent a contiguous or noncontiguous sequence, so a frame may span several segments.

## Rules
- Always call `AdvanceTo` after `ReadAsync`. The `ReadOnlySequence<T>` from `ReadAsync` is valid only until `AdvanceTo`; using it afterwards is illegal and can corrupt memory (use after free). Never touch `ReadResult.Buffer` after `AdvanceTo` or after completing the reader.
- Wrong `consumed` and `examined` values cause bugs: `AdvanceTo(buffer.Start)` with an unchanged start makes the next `ReadAsync` return immediately (busy loop); passing wrong values can also cause infinite buffering (eventual out of memory). When parsing a single message, passing `buffer.End` as `examined` unconditionally can leave the app unresponsive, because the next `ReadAsync` waits for data that was not yet examined.
- Check `ReadResult.IsCompleted` after processing the buffer, not before: the final segment can arrive with `IsCompleted` true, and exiting early loses data. Base the exit on `Buffer.IsEmpty` and `IsCompleted` for message loops.
- Call `Complete`/`CompleteAsync` on both reader and writer; skipping it can leak memory. A helper that reads a single message must not complete the reader if the caller reads further messages.
- Backpressure: `PipeOptions.PauseWriterThreshold` is how much data is buffered before `FlushAsync` pauses; `ResumeWriterThreshold` is how much the reader must observe before `FlushAsync` resumes.
- Writers: `GetMemory`/`GetSpan` return at least the requested size, never assume the exact size; check `FlushResult.IsCompleted` and stop writing when the reader has completed; do not call `Complete` with unflushed data.
- Copy any payload you keep before calling `AdvanceTo`; returned memory may be reused by the pipe.

## Verify
Feed the parser input split at every possible byte boundary in a test and assert identical output.

## Checked
2026-11-08. Confirmed against the System.IO.Pipelines page (AdvanceTo lifetime rules, consumed/examined pitfalls, IsCompleted handling, Complete, PauseWriterThreshold/ResumeWriterThreshold, writer rules, PipeReader.Create/PipeWriter.Create) and the Buffers page (ReadOnlySequence noncontiguous). The PipeReader API page was not separately mined. Removed as unconfirmed: the IsSingleSegment/FirstSpan fast path, SequenceReader advice, Kestrel BodyReader and connection middleware claims, the single reader/writer rule and the socket-to-pipe snippet. The code sample is illustrative and was not compiled.
Method: documentation only; no commands were run.
