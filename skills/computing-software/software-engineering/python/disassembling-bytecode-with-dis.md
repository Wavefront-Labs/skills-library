---
id: computing-software.software-engineering.python.disassembling-bytecode-with-dis
name: disassembling-bytecode-with-dis
category: computing-software
field: software-engineering
product: python
tags: [python, py-introspection, py-isp-dis, dis-bytecode, dis, bytecode, code-objects, specialization]
level: advanced
status: docs-checked
description: "Inspect CPython bytecode with the dis module: dis.dis, Bytecode, get_instructions, code objects, adaptive specialisation flags and why bytecode is version-specific."
sources: ["https://docs.python.org/3/library/dis.html", "https://docs.python.org/3/reference/datamodel.html#code-objects"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disassembling bytecode with dis

```python
import dis

def f(a, b):
    return a * b + 1

dis.dis(f)                       # human-readable listing
dis.dis(f, adaptive=True)        # 3.11+: show specialised bytecode, which may differ from the original
dis.show_code(f)                 # detailed code information
code = f.__code__                # code object
for ins in dis.get_instructions(f):
    print(ins)                   # Instruction objects
print(dis.Bytecode(f).info())    # like dis.code_info()
```
Command line: `python -m dis [-h] [-C] [-O] [-P] [-S] [infile]`; `-S` / `--specialized` shows specialised bytecode (the `-O` offsets option arrived in 3.13, `-P` positions in 3.14).

## Facts from the docs
- Bytecode is a CPython implementation detail: no guarantee it is not added, removed or changed between Python versions, so use of `dis` should not be assumed to work across VMs or releases.
- 3.11: some instructions are followed by inline `CACHE` entries (hidden by default; `show_caches=True` shows them); `adaptive` and `show_caches` parameters were added.
- 3.12: a jump argument is the offset of the target relative to the instruction after the jump's `CACHE` entries.
- 3.13: output shows logical labels rather than offsets for jump targets and exception handlers; `show_offsets` added; the `show_caches` parameter of `get_instructions` is deprecated and ignored, with `cache_info` populated on each `Instruction`.
- 3.14: `show_positions` added.
- Code objects expose `co_consts` (literals), `co_names`, `co_varnames`, `co_stacksize`, `co_flags` and `co_linetable` (encoded source locations); see the data model reference.

## Gotchas
- Do not ship logic that depends on specific opcodes; record the interpreter version next to any bytecode listing.
- Compare candidate implementations by measuring, not by reading opcodes alone.

## Verify
- [ ] Re-run `dis.dis` on the target Python version before relying on a listing.

## Checked
Date: 2026-11-03. Confirmed against the `dis` module documentation (implementation-detail warning, version changes, signatures, command-line options) and the data model "Code objects" section. Removed as unconfirmed: specific opcode names (LOAD_DEREF, GET_AWAITABLE, SEND), `SETUP_*` removal, zero-cost exception claims, `.pyc` magic number, PyPy/GraalPy remark, constant-folding examples, `co_lines()`, `timeit` advice, adaptive warm-up behaviour.
Method: documentation only; no commands were run.
