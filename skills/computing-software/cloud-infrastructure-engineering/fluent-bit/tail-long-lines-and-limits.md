---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.tail-long-lines-and-limits
name: tail-long-lines-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, tail-input, skip-long-lines, buffer-max-size, truncate-long-lines, mem-buf-limit]
level: advanced
status: docs-checked
description: "Prevent tail from dropping a file when a line exceeds buffer_max_size, using skip_long_lines or truncation."
sources: ["https://docs.fluentbit.io/manual/pipeline/inputs/tail"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tail long lines

Each monitored file gets a buffer starting at `buffer_chunk_size` (default `32k`) that grows when a line does not fit. `buffer_max_size` limits that growth. If reading a file exceeds the limit, the default behaviour is that the file is removed from the monitored list and stops being read.

Options to change this:
- `skip_long_lines: true`: skip lines that exceed `buffer_max_size` and continue with the rest of the file.
- `truncate_long_lines: true`: truncate lines that exceed the buffer capacity after conversion to UTF-8. Use it when encoding conversion can expand a line.

```yaml
pipeline:
  inputs:
    - name: tail
      path: /var/log/app/*.log
      buffer_chunk_size: 64k
      buffer_max_size: 256k
      skip_long_lines: true
      mem_buf_limit: 50M
```

Because buffers are per file, a high limit multiplied by many files can use a lot of memory. `mem_buf_limit` caps what the plugin appends to the engine: when reached, tail pauses and resumes after data flushes.

Sizes follow the Unit Size specification. `buffer_max_size` defaults to `32k`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Tail input page: buffer_chunk_size and buffer_max_size defaults of 32k, the default of dropping the file from monitoring, skip_long_lines, truncate_long_lines, per-file buffers, and mem_buf_limit pause and resume. Removed: an unsourced sizing rule and verification step.

Method: documentation only; no commands were run.
