---
id: computing-software.ai-ml-engineering.pytorch.context-parallelism-long-sequences
name: context-parallelism-long-sequences
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, context-parallelism, ring-attention, long-context, sequence-parallelism, torchtitan, distributed]
level: practitioner
status: draft
description: "Train long-sequence transformers with PyTorch context parallelism: ring attention over sharded sequence dims, the context_parallel API, mesh layout and load balancing."
sources:
  - https://pytorch.org/tutorials/prototype/context_parallel.html
  - https://github.com/pytorch/torchtitan/blob/main/docs/composability.md
  - https://arxiv.org/abs/2310.01889
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Context parallelism for long sequences

Activation memory for attention layers grows with sequence length. Tensor parallelism shards hidden dims and FSDP shards parameters, but a single 128k-token sequence can still overflow one GPU. **Context parallelism (CP)** shards the *sequence* dimension of Q/K/V across GPUs and exchanges K/V blocks in a ring so every query sees every key (ring attention).

## API (experimental, PyTorch 2.5+)
```python
from torch.distributed.device_mesh import init_device_mesh
from torch.distributed.tensor.experimental import context_parallel
from torch.distributed.tensor.experimental._attention import set_rotate_method

mesh = init_device_mesh("cuda", (cp_size,), mesh_dim_names=("cp",))
set_rotate_method("alltoall")            # or "allgather"
with context_parallel(mesh, buffers=[input_ids, labels, freqs_cis],   # tensors to shard along seq dim
                      buffer_seq_dims=[1, 1, 0],
                      no_restore_buffers={input_ids, labels}):
    loss = model(input_ids, labels)       # SDPA calls are replaced by ring attention
    loss.backward()
```
- Works when attention goes through `F.scaled_dot_product_attention` (flash or memory-efficient backends).
- Inputs are sharded in place inside the context; position ids / rotary tables must be sharded consistently (pass them as buffers).

## Mesh layout
Combine as a multi-dim mesh, e.g. `("dp_shard", "cp", "tp")`. Put TP innermost (within a node, NVLink), CP next, data parallel outermost. torchtitan exposes `--parallelism.context_parallel_degree`; FSDP shards over `dp_shard x cp` together because CP ranks hold identical params.

## Causal load balancing
With a causal mask, later sequence chunks do more work. The implementation splits the sequence into 2 x cp_size chunks and gives rank i chunks i and (2 x cp_size - 1 - i) so work is even. Do not pre-shard data yourself in plain contiguous chunks when using causal masks.

## Costs and limits
- Communication: K/V of each chunk travels around the ring once per layer (forward and backward); overlap with compute hides it only if chunks are large enough (thousands of tokens per rank).
- Document masking / arbitrary masks are limited; check the supported mask types for your version.
- Prefer FSDP + activation checkpointing first; add CP when a single sequence's activations still do not fit.

## Alternatives
- DeepSpeed Ulysses (all-to-all on heads, needs heads divisible by degree).
- Megatron-Core context parallelism (`--context-parallel-size`).

## Verify
Loss curve of a short run with CP equals the non-CP run at the same global batch (within bf16 noise); peak memory per GPU drops roughly with cp_size for attention activations.
