---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.tail-buffer-tuning
name: tail-buffer-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, tail-input, buffer-chunk-size, buffer-max-size, performance, file-reading]
level: practitioner
status: docs-checked
description: "Raise the tail input buffer size above its 32KB default to cut read system calls and CPU use."
sources: ["https://docs.fluentbit.io/manual/administration/performance", "https://docs.fluentbit.io/manual/pipeline/inputs/tail"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tail buffer tuning

The `tail` input reads files with a small default memory buffer of `32KB` per monitored file. That suits generic cases and keeps memory low when watching many files.

If your files are typically larger than `32KB`, a bigger buffer lets Fluent Bit make fewer `read(2)` system calls, reducing CPU use and improving performance. The docs suggest experimenting with `128KB`:

```yaml
pipeline:
  inputs:
    - name: tail
      path: '/var/log/containers/*.log'
      buffer_chunk_size: 128kb
      buffer_max_size: 128kb
```

`buffer_chunk_size` (default `32k`) is the initial buffer size used to read file data; `buffer_max_size` (default `32k`) limits how far the buffer can grow per monitored file.

Trade-offs:
- The buffers are per file, so many monitored files multiply memory use.
- If reading a file exceeds `buffer_max_size` (for example a very long line), the default is to remove the file from the monitored list. Set `skip_long_lines` to `true` to skip such lines and keep processing the rest.

Combine with `threaded: true` to move file reading off the main event loop (see `computing-software.cloud-infrastructure-engineering.fluent-bit.input-threaded-mode`).

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs performance tips page and tail input page (raw markdown; parameter table and Buffers sections read).
