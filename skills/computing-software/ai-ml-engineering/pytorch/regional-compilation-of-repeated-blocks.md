---
id: computing-software.ai-ml-engineering.pytorch.regional-compilation-of-repeated-blocks
name: regional-compilation-of-repeated-blocks
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-compile, regional-compilation, compile-time, transformer-blocks, nested-compile-region]
level: practitioner
status: gated
description: "Compile only the repeated transformer block instead of the whole model to cut compile time 5-10x, keeping most speedup; patterns for HF models and FSDP."
sources:
  - https://pytorch.org/tutorials/recipes/regional_compilation.html
  - https://pytorch.org/docs/stable/torch.compiler_api.html
  - https://huggingface.co/docs/accelerate/usage_guides/compilation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Regional compilation of repeated blocks

**Idea:** a transformer is N copies of the same block. Compiling each block (same code, same shapes) lets Dynamo reuse one compiled artifact for all N, so compile time scales with one block, not the model depth.

## Pattern
```python
for i, block in enumerate(model.layers):
    model.layers[i] = torch.compile(block)          # or block.compile() for in-place
# leave embeddings, head, sampling logic eager (or compile separately)
```
`nn.Module.compile()` compiles in place and keeps the module type and state-dict keys unchanged (no `_orig_mod.` prefix), which matters for checkpoints. Measured on torch 2.14: after `block.compile()` the keys were `layers.0.l.weight, ...` and the type stayed `Block`; with `model.layers[i] = torch.compile(block)` the keys became `layers.0._orig_mod.l.weight` and the type `OptimizedModule`; whole-model `torch.compile(model)` gave `_orig_mod.layers.0.l.weight`.

Compared with `torch.compile(model)`:
- Compile time: a counting backend (`backend=fn`, no C++ compiler needed) was called 2 times for 6 identical blocks (one compile plus one recompile when the input started requiring grad) and 1 time for the whole model, so artifacts are shared across blocks. Minutes to tens of seconds for real deep models, and the "within a few percent of full compilation" runtime figure, were not measured (needs Inductor, which needs a compiler and a GPU here) (gated: unconfirmed, source is paywalled or blocked).
- Loses cross-block fusion and whole-graph CUDA graphs (reasoned, not measured).

## Requirements for reuse
- Blocks must be the same class and receive inputs with the same shapes/dtypes/strides; differing per-layer Python constants cause separate compiles, and worse than the parity example suggests: Dynamo treats integer attributes of an `nn.Module` as static and guards on the value, so 6 blocks with `if self.i % 2` produced 6 compiles (not 2), and with 12 blocks the compile count stopped at the recompile limit of 8 (`torch._dynamo.config.recompile_limit`), with a warning `last reason: 0/7: s.i == 7`, after which the remaining blocks ran eagerly. Move such differences into tensors, avoid integer attributes read in `forward`, or (per the warning's hint) make the int dynamic; `torch._dynamo.config.allow_unspec_int_on_nn_module` exists and defaults to False.
- Watch `TORCH_LOGS=recompiles` to confirm one compile is reused.

## With FSDP2 and activation checkpointing
This section was not run with compilation (no GPU or compiler); only `checkpoint_wrapper` followed by `fully_shard` was run (see the FSDP2 skill) (gated: unconfirmed, source is paywalled or blocked). Apply in this order per block: activation checkpoint wrapper, then `fully_shard`, then compile the block (or compile inside); compiling the whole FSDP model triggers graph breaks at collectives anyway, so per-block compile is the recommended FSDP2 pattern.

## Hugging Face
Accelerate's utilities reference lists `use_regional_compilation` as a `TorchDynamoPlugin` argument; the Diffusers optimisation docs describe `compile_repeated_blocks()` as a helper that wraps `torch.compile` on a component such as the transformer (and claim 8-10x less compile time with the same speedup, a vendor figure not measured here) (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Wall-clock compile time and steady-state step time recorded for both full and regional compile.
- [ ] `torch._dynamo.utils.counters["stats"]["unique_graphs"]` is small (not N): it read 2 for 6 identical blocks.
