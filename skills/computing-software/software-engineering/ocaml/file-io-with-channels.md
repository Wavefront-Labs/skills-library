---
id: computing-software.software-engineering.ocaml.file-io-with-channels
name: file-io-with-channels
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, file-io-channels, ocaml-io-unix, in-channel, out-channel, read-file, open-in-bin]
level: practitioner
status: docs-checked
description: "Read and write files with In_channel/Out_channel, open_in_bin, lines and whole-file reads, and close channels reliably."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File I/O

```ocaml
let read_all path = In_channel.with_open_bin path In_channel.input_all     (* 4.14+ *)
let write path s = Out_channel.with_open_bin path (fun oc -> output_string oc s)
let lines path =
  In_channel.with_open_text path (fun ic ->
    let rec go acc = match In_channel.input_line ic with Some l -> go (l :: acc) | None -> List.rev acc in go [])
```

## Notes
- `In_channel`/`Out_channel` modules arrived in 4.14. Older: `open_in`, `input_line`, `close_in` with `Fun.protect`.
- Use binary mode (`_bin`) to avoid newline translation on Windows.
- `input_line` raises `End_of_file`; `In_channel.input_line` returns an option.
- Output is buffered: `flush oc` or close; `exit` flushes all open output channels with `flush_all`.
- `Sys.file_exists`, `Sys.readdir`, `Sys.is_directory`, `Sys.remove`, `Sys.rename` and `Sys.mkdir`; `Unix.mkdir` also exists.

## Self-check
- [ ] A write followed by a read round-trips the data.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the In_channel and Out_channel API pages (with_open_bin, with_open_text, since 4.14), the Sys page (file_exists, readdir, is_directory, remove, rename, mkdir), the Unix page (mkdir) and the Stdlib page (exit flushes channels with flush_all).

Removed or corrected: the domain-safety claim for channels, and the stale statement that only Unix has mkdir (Sys.mkdir exists).

Method: documentation only; no commands were run.
