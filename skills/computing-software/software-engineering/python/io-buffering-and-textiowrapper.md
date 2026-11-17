---
id: computing-software.software-engineering.python.io-buffering-and-textiowrapper
name: io-buffering-and-textiowrapper
category: computing-software
field: software-engineering
product: python
tags: [python, py-io, io-buffering-textiowrapper, textiowrapper, bufferedreader, stringio, bytesio, newline-handling, flush]
level: practitioner
status: docs-checked
description: "Understand the io stack (raw, buffered, text), choose buffering, newline and encoding arguments, wrap sockets or pipes, and use StringIO/BytesIO in tests."
sources: ["https://docs.python.org/3/library/io.html", "https://docs.python.org/3/library/functions.html#open"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# io buffering and TextIOWrapper

Layers: `FileIO` (raw bytes, unbuffered) -> `BufferedReader/Writer/Random` -> `TextIOWrapper` (decoding, newline translation).

```python
import io
with open("log.txt", "w", encoding="utf-8", newline="\n", buffering=1) as f:   # line-buffered text
    f.write("hello\n")
with open("big.bin", "rb", buffering=1 << 20) as f:            # 1 MiB buffer for big sequential reads
    while chunk := f.read(1 << 20): ...

raw = open("data.bin", "rb", buffering=0)                       # raw FileIO: read(n) may return fewer bytes
text = io.TextIOWrapper(sock.makefile("rb"), encoding="utf-8", newline="")   # decode a byte stream
buf = io.StringIO(); print("x", file=buf); buf.getvalue()      # capture output in tests
b = io.BytesIO(b"abc"); b.getbuffer()                           # in-memory binary file
```

## Newlines
- Reading, `newline=None` (default): `\r\n` and `\r` become `\n`. `newline=""`: no translation but line splitting recognises all (use for `csv`). Writing: `\n` becomes `os.linesep` unless `newline="\n"`.
- Pass `encoding=` explicitly: when UTF-8 Mode is off the default is locale-specific, and Python 3.15 made UTF-8 Mode the default. `encoding="locale"` (3.10+) asks for the locale encoding explicitly. The `errors` argument selects the error handler.

## Flushing and durability
`flush()` pushes Python's buffer to the OS; the `os.fsync` docs say to call `f.flush()` and then `os.fsync(f.fileno())` to make sure data reaches disk. `buffering=1` (line buffering) is only usable when writing in text mode; `buffering=0` is only allowed in binary mode. `python -u` forces stdout and stderr to be unbuffered.

## Gotchas
- `TextIOWrapper.tell()` returns an opaque number, and `seek()` only accepts a number previously returned by `tell()` (plus offset zero or end); byte offsets need binary mode.
- `detach()` separates the underlying binary buffer from a text stream and returns it; the text stream is then unusable.
- `TextIOWrapper.reconfigure()` can change encoding, errors, newline, `line_buffering` and `write_through`; it is not possible to change the encoding or newline if some data has already been read from the stream.

## Verify
- [ ] Round-trip a file containing `\r\n`, non-ASCII and a lone `\r` in both modes.
- [ ] Durable writes call `flush()` then `os.fsync()` before relying on the data being on disk.

## Checked

- 2026-11-03: checked against the CPython docs `library/io.rst` (raw/buffered/text classes, `TextIOWrapper` newline rules, `line_buffering`, `reconfigure`, `detach`, opaque `tell`, `StringIO`/`BytesIO` `getvalue`/`getbuffer`, 3.15 UTF-8 mode default), `builtins/functions.rst` `open()` buffering rules, `library/os.rst` `fsync` and `library/socket.rst` `makefile`.
- Removed: the `telling position disabled by next()` error text, the garbage-collection close claim, the Windows console fix and the write-to-temp-and-replace recipe (not in these pages).

Method: documentation only; no commands were run.
