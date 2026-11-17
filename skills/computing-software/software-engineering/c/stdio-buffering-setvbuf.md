---
id: computing-software.software-engineering.c.stdio-buffering-setvbuf
name: stdio-buffering-setvbuf
category: computing-software
field: software-engineering
product: c
tags: [c, setvbuf, stdio-buffering, fflush, line-buffered, stderr-unbuffered]
level: advanced
status: docs-checked
description: "Control stdio buffering with setvbuf and fflush and avoid lost or reordered output."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://www.gnu.org/software/libc/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stdio buffering setvbuf

Goal: predictable output timing for logs, pipes and interactive prompts.

- Streams are fully buffered, line buffered, or unbuffered. `stderr` is unbuffered; `stdout` is line buffered only when it refers to a terminal, otherwise fully buffered, so piped logs appear late or are lost if the process dies before flushing.
- `setvbuf(stream, buf, _IOLBF, size)` must be called after opening and before any other operation on the stream; the buffer must outlive the stream.
- `fflush(stdout)` before `fork()` prevents duplicated buffered output in children, and before prompting with `fgets` when no newline is printed.
- Mixing `write(2)` on a descriptor with stdio on the same descriptor reorders output unless flushed.
- `_exit()` does not flush stdio; `exit()` does.

Verify: run `./prog | cat` and compare the order and timing of stdout vs stderr lines.

## Checked

2026-11-02. Confirmed in setvbuf(3), the glibc manual (buffering concepts, controlling buffering), exit(3), _exit(2): three buffering modes, `stderr` unbuffered, terminal stdout line buffered, `setvbuf` only after open and before other operations, `exit` flushes stdio. Removed: the `abort()` claim and the input-stream `fflush` remark.

Method: documentation only; no commands were run.
