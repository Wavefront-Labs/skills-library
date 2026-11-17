---
id: computing-software.ai-ml-engineering.pytorch.torch-compile-minifier-and-bug-reports
name: torch-compile-minifier-and-bug-reports
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, compile-minifier, torch-compile, repro-after, accuracy-minifier, tlparse, bug-report]
level: practitioner
status: gated
description: "Shrink torch.compile crashes and accuracy mismatches to a minimal repro with TORCHDYNAMO_REPRO_AFTER and REPRO_LEVEL, then file a usable PyTorch bug report."
sources:
  - https://pytorch.org/docs/stable/torch.compiler_troubleshooting.html
  - https://pytorch.org/docs/stable/torch.compiler_troubleshooting_old.html#minifying-backend-compiler-errors
  - https://github.com/pytorch/tlparse
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compile crash and accuracy minifiers

## 1. Locate the layer first (backend bisect)
Run with `backend="eager"`, `"aot_eager"`, `"inductor"` (the first two are in `torch._dynamo.list_backends(None)` on 2.14). If `aot_eager` passes and `inductor` fails, the bug is in Inductor codegen; set repro to after AOT. If `eager` fails, it is in Dynamo; repro after Dynamo.

## 2. Crash minifier
```bash
TORCHDYNAMO_REPRO_AFTER="aot" TORCHDYNAMO_REPRO_LEVEL=4 python train.py
```
- `REPRO_AFTER="dynamo"`: minify the FX graph Dynamo produced (backend failures).
- `REPRO_AFTER="aot"`: minify the post-AOTAutograd graph (Inductor failures; usually what you want).
- `REPRO_LEVEL` (default 2; read from `TORCHDYNAMO_REPRO_LEVEL`, and `repro_after` defaults to None so the minifier is off until you set it): 1 = dump a repro of the failing graph, 2 = write a `minifier_launcher.py` for it, 3 = dump the graph before compiling (for hangs and crashes) so the launcher can minify in a fresh process, 4 = accuracy minifier (source: `torch/_dynamo/repro/after_dynamo.py`).
Measured with `backend="relu_compile_error_TESTING_ONLY"`, `REPRO_AFTER=dynamo`: level 1 wrote `repro.py` and `checkpoints/` in the current directory; level 2 wrote `torch_compile_debug/run_<ts>-pid_<pid>/minifier/minifier_launcher.py` and printed "Run this script to find the smallest traced graph which reproduces this error". Running `python minifier_launcher.py minify` reduced 4 nodes to 3 and wrote `repro.py` into the current directory (a standalone script with the minimal graph and inputs of the right shapes). I ran only the `dynamo` path; the `aot` and level 3/4 paths were not run (they need Inductor, which needs a compiler here) (gated: unconfirmed, source is paywalled or blocked).

## 3. Accuracy minifier
When compiled outputs differ from eager (no crash):
```bash
TORCHDYNAMO_REPRO_AFTER="aot" TORCHDYNAMO_REPRO_LEVEL=4 python train.py
```
It compares compiled vs eager (fp64 reference) per subgraph and shrinks to the smallest graph that still mismatches. Tolerance: `torch._dynamo.config.repro_tolerance` (default 0.001 on 2.14). Make the run deterministic first (fixed seed, dropout off) or noise looks like a bug.

## 4. Logs that go with the repro
```bash
TORCH_TRACE=/tmp/trace python train.py && tlparse /tmp/trace -o tl_out/   # HTML: graphs, guards, recompiles, compile times (tlparse is a separate tool, not installed or run here)
TORCH_LOGS="+dynamo,guards,recompiles,output_code" python repro.py
TORCH_COMPILE_DEBUG=1 python repro.py      # dumps FX graphs, IR and generated Triton/C++ code
```
For Inductor numerics also try `torch._inductor.config.fallback_random = True` (match eager RNG) and `emulate_precision_casts = True` (both names exist on 2.14 and default to False).

## 5. Narrow inside Inductor
- `torch._inductor.config.triton.cudagraphs = False` and `max_autotune = False` to exclude those (both read False by default on 2.14; mode names set them).
- Disable fusions selectively (`torch._inductor.config.epilogue_fusion = False`; the option exists and defaults to True) to see which pass breaks.

## 6. File the issue
Include: `python -m torch.utils.collect_env` output, the minified `repro.py`, the backend bisect result, the tlparse link or key logs, and expected vs actual. Search existing issues for the error string first; nightly builds often already fix it (`pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu` for CPU; pick the CUDA index that matches your GPU, since the `cu126` suffix in older notes changes between releases).

## Workaround while waiting
Wrap the offending function with `torch.compiler.disable` or compile with `backend="aot_eager"` for that submodule only (regional compilation).
