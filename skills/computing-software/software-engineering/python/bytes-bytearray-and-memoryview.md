---
id: computing-software.software-engineering.python.bytes-bytearray-and-memoryview
name: bytes-bytearray-and-memoryview
category: computing-software
field: software-engineering
product: python
tags: [python, py-text, bytes-bytearray-memoryview, memoryview, zero-copy, buffer-protocol, binary-data]
level: practitioner
status: docs-checked
description: "Work with binary data: bytes vs bytearray, hex and int conversion, zero-copy slicing with memoryview, readinto buffers and the buffer protocol."
sources: ["https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview", "https://docs.python.org/3/c-api/buffer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bytes, bytearray and memoryview

```python
b = b"\x00\xffAB"                      # immutable; indexing gives int, slicing gives bytes
b[2] == 65;  b.hex() == "00ff4142";  bytes.fromhex("00ff") == b"\x00\xff"
int.from_bytes(b"\x01\x00", "big") == 256;  (256).to_bytes(2, "little") == b"\x00\x01"

ba = bytearray(1024)                   # mutable, resizable
n = sock.recv_into(ba)                 # fill an existing buffer, no new allocation
mv = memoryview(ba)
header, body = mv[:16], mv[16:n]       # views: slicing copies nothing
body[0] = 0x7F                         # writes through to ba
header.tobytes()                       # copy out when you need a real bytes
body.release()
```

## Rules of thumb
- Build output with `bytearray` in-place concatenation or `b"".join(parts)` / `io.BytesIO`; repeated `+=` on `bytes` has quadratic cost.
- Reads: methods such as `readinto()` need write access to their argument, so pass a reusable `bytearray` in hot loops.
- `memoryview.cast(fmt)` reinterprets the buffer with another native `struct` format (for example `cast("B")`).
- Decode explicitly: `data.decode("utf-8", errors="strict")`.

## Gotchas
- A `bytearray` with a live `memoryview` export temporarily forbids resizing (`BufferError`). Call `release()` on views first (or use `with memoryview(ba) as mv:`).
- `bytes` indexing returns an int; compare with `b[0] == 0x41`, or slice `b[:1] == b"A"`.
- `bytes(10)` makes ten zero bytes while `bytes([10])` (an iterable of integers) makes one byte with value 10.

## Verify
- [ ] A test asserts a mutation through a view appears in the base buffer.
- [ ] Profile a large-file path with `tracemalloc` to confirm no per-chunk copies.

## Checked

2026-11-08. Confirmed on the Python 3 stdtypes "Binary Sequence Types" page: `int.from_bytes`/`int.to_bytes`, `bytes.fromhex`, `.hex()`, `bytes(10)` zero-filled, `bytes(range(20))` from an iterable of ints, indexing returns an int while slicing returns bytes, quadratic cost of repeated concatenation with `bytes.join()`/`io.BytesIO`/`bytearray` as alternatives, memoryview zero-copy slicing into subviews, `tobytes()`, `cast()`, `release()` (a bytearray would temporarily forbid resizing). The C-API buffer page confirms `readinto()` needs write access and `BufferError` on refusal. Removed: the exact `BufferError` message text, `struct.unpack_from`, `hmac.compare_digest`, the `str(b)` repr remark and the "views keep the whole buffer alive" bullet (not on the cited pages). The `recv_into`, `tracemalloc` lines are code or advice, not documented figures.

Method: docs-only read of cited pages, 2026-11-08
