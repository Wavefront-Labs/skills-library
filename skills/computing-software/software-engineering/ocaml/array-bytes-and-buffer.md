---
id: computing-software.software-engineering.ocaml.array-bytes-and-buffer
name: array-bytes-and-buffer
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, array-bytes-buffer, array-module, bytes-module, buffer-module, string-builder]
level: practitioner
status: docs-checked
description: "Use Array, Bytes and Buffer for mutable sequences and efficient string building; bounds checks and Array.blit/sub."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array, Bytes, Buffer

```ocaml
let a = Array.init 5 (fun i -> i * i)
let () = Array.sort compare a
let s = Array.sub a 1 3        let b = Array.copy a
let () = Array.blit a 0 b 0 5
let buf = Buffer.create 256
let () = Buffer.add_string buf "x"; Buffer.add_char buf 'y'
let out = Buffer.contents buf
```

## Notes
- `Array.make n x` fills with elements physically equal to `x`, so a mutable `x` is shared. `Array.sort` currently uses heap sort in constant stack space; `Array.stable_sort` currently uses merge sort, needs a temporary array of length n/2 and is usually faster.
- Maximum array size is `Sys.max_array_length` (only half of that when the elements are floats); strings are limited by `Sys.max_string_length`.
- Use `Buffer` rather than repeated `^`: buffers give accumulative concatenation in linear time (instead of quadratic). `Buffer.add_substring` and `Buffer.add_utf_8_uchar` exist.
- `Bytes.unsafe_to_string` avoids a copy; the caller must own the byte sequence and give up ownership (never mutate it afterwards).

## Self-check
- [ ] Building a 1 MB string uses `Buffer`, not `^` in a loop.

## Checked

2026-11-02. Checked against the OCaml 5.5 manual Array, Bytes and Buffer modules (Array.make physical equality, Array.sort heap sort, stable_sort merge sort with n/2 temporary array, Sys.max_array_length halved for floats, Buffer linear-time concatenation, add_substring, add_utf_8_uchar, Bytes.unsafe_to_string ownership rule). Removed: the unboxed float array and Obj remark, and the iteration helper list (not re-verified).

Method: documentation only; no commands were run.
