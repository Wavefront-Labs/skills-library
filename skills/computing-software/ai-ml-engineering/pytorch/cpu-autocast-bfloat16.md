---
id: computing-software.ai-ml-engineering.pytorch.cpu-autocast-bfloat16
name: cpu-autocast-bfloat16
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, cpu-autocast, bfloat16, mixed-precision, amx, cpu-inference, autocast]
level: practitioner
status: gated
description: "Run PyTorch training or inference on CPU with torch.autocast(device_type='cpu', dtype=torch.bfloat16): hardware needs (AVX512-BF16/AMX), op lists, accuracy and speed checks."
sources:
  - https://pytorch.org/docs/stable/amp.html#cpu-ops-that-can-autocast-to-bfloat16
  - https://pytorch.org/tutorials/recipes/amx.html
  - https://pytorch.org/docs/stable/amp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CPU autocast with bfloat16

```python
model.eval()
with torch.inference_mode(), torch.autocast(device_type="cpu", dtype=torch.bfloat16):
    out = model(x)
```
Training works the same way (`autocast` around forward and loss, `backward()` outside); no `GradScaler` is needed for bf16.

## Hardware decides the speedup
- **Intel Sapphire Rapids and newer (AMX-BF16)**: large gains on matmul/conv, often 2-4x over fp32 (gated: unconfirmed, source is paywalled or blocked). The test host here has neither AMX nor AVX512-BF16, so no speed figure was measured.
- **AVX512-BF16 (Cooper Lake, Zen 4+)**: moderate gains (gated: unconfirmed, source is paywalled or blocked).
- **No native bf16**: emulated, usually *slower* than fp32 (gated: unconfirmed, source is paywalled or blocked). Check: `lscpu | grep -E "amx|avx512_bf16"` on Linux, `torch.backends.mkldnn.is_available()` (True on the test host, which lacks both features) and benchmark.
- Apple Silicon / ARM: bf16 support varies by chip; test (not available here).

## What runs in bf16
The CPU lists are much shorter than the CUDA ones (PyTorch amp docs, "CPU Ops that can autocast to bfloat16"): `conv1d/2d/3d`, `conv_transpose*`, `bmm`, `mm`, `baddbmm`, `addmm`, `addbmm`, `linear`, `matmul`, `prelu`, `scaled_dot_product_attention` and a few internal ops run in bf16. The fp32 list is only `avg_pool3d`, `binary_cross_entropy`, `grid_sampler*`, `polar`, `prod`, `quantile`, `nanquantile`, `stft`, `cdist`, `trace`, `view_as_complex` and a few linalg ops (`inverse`, `cholesky_*`, `linalg_eigh`, `linalg_lstsq`, `linalg_inv_ex`). `cat`, `stack` and `index_copy` promote to the widest input type. Everything else keeps its input dtype: run on torch 2.14, `softmax`, `layer_norm`, `sum`, `exp` and `cumsum` of a bf16 tensor all stayed bf16 (unlike CUDA autocast, which sends them to fp32). The docs say `float16` shares the bf16 list.

## Combine with
- `torch.compile(model)` (Inductor can generate bf16 CPU kernels; needs a C++ compiler, which the test host lacks, so it was not run).
- Thread settings: `torch.set_num_threads(physical_cores)`, `OMP_NUM_THREADS`, pin to one NUMA node (`numactl -C 0-31 -m 0`, Linux; not run here).
- IPEX (`intel_extension_for_pytorch`) is retired: its GitHub repository is archived, official releases stopped after 2.8 and Intel says most features were upstreamed into PyTorch. Do not start new work on it.

## Accuracy check
```python
ref = model(x)                                 # fp32
with torch.autocast("cpu", dtype=torch.bfloat16): lo = model(x)
print((ref - lo.float()).abs().max(), torch.nn.functional.cosine_similarity(ref.flatten(), lo.float().flatten(), dim=0))
```
Compare task metrics on a validation set, not just tensor diffs. bf16 has ~3 significant digits; models with large dynamic range in reductions may need specific layers forced to fp32 (`with torch.autocast("cpu", enabled=False): ...`).

## Gotchas
- Inputs created inside autocast are not cast; autocast casts at op boundaries.
- Outputs are bf16; call `.float()` before NumPy conversion (NumPy has no bf16).
- Benchmark with warm-up iterations and fixed thread counts; first calls include oneDNN primitive creation.
