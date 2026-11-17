---
id: computing-software.ai-ml-engineering.vllm.reproducibility
name: reproducibility
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [reproducibility, batch-invariance, seed, vllm-enable-v1-multiprocessing, deterministic]
level: practitioner
status: docs-checked
description: "Get repeatable output with seed, batch invariance and VLLM_ENABLE_V1_MULTIPROCESSING=0."
sources:
  - https://docs.vllm.ai/en/latest/usage/reproducibility/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make repeated vLLM runs return identical output.

vLLM does not guarantee reproducibility by default, for performance. To achieve it:
- Offline mode: set `VLLM_ENABLE_V1_MULTIPROCESSING=0`, which makes scheduling deterministic, or enable batch invariance, which makes outputs insensitive to scheduling.
- Online mode: only batch invariance works.

Even with these settings, reproducibility holds only on the same hardware and the same vLLM version.

Warning: `VLLM_ENABLE_V1_MULTIPROCESSING=0` changes the random state of your own code, meaning the code that constructs the `LLM` class. By default the variable is `1`, so using vLLM does not accidentally make your other random operations deterministic. Workers share your process, and your random state is updated, only when it is `0`.

The `seed` parameter controls random number generators. Giving a value sets the state of `random`, `np.random` and `torch.manual_seed`.

Default in V1: `seed` defaults to `0`, which sets the random state for each worker, so results stay consistent between runs even when `temperature > 0`. You cannot un-specify a seed in V1, because different workers must sample the same outputs for workflows such as speculative decoding.

## Checked

Method: 2026-11-08 read the reproducibility page in full. All claims (multiprocessing flag, batch invariance, same hardware and version, seed default 0, cannot unset in V1) matched; unchanged.
