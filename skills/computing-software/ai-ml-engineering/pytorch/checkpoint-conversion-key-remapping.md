---
id: computing-software.ai-ml-engineering.pytorch.checkpoint-conversion-key-remapping
name: checkpoint-conversion-key-remapping
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, checkpoint-conversion, state-dict, key-remapping, load-state-dict, model-migration]
level: practitioner
status: verified
description: "Load old or foreign checkpoints into changed model code: inspect keys, regex remaps, prefix stripping (module./_orig_mod.), fused qkv splits, shape fixes and validation."
sources:
  - https://pytorch.org/tutorials/beginner/saving_loading_models.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.load_state_dict
  - https://huggingface.co/docs/transformers/main/en/modular_transformers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Converting checkpoints across model code changes

**Goal:** reuse weights after refactoring module names, porting from another codebase, or changing layer layouts.

## 1. Diff the keys
```python
sd = torch.load("old.pt", map_location="cpu", weights_only=True)
sd = sd.get("model", sd)                         # unwrap training checkpoints
new_keys = set(model.state_dict()); old_keys = set(sd)
print("missing:", sorted(new_keys - old_keys)[:20])
print("unexpected:", sorted(old_keys - new_keys)[:20])
```

## 2. Common prefixes
| Prefix | Source | Fix |
|---|---|---|
| `module.` | DDP/DataParallel | `k.removeprefix("module.")` |
| `_orig_mod.` | `torch.compile` wrapper | strip it, or save `model._orig_mod.state_dict()` |
| `model.` / `backbone.` | wrappers, Lightning | strip or add as needed |

`torch.nn.modules.utils.consume_prefix_in_state_dict_if_present(sd, "module.")` handles the DDP case in place.

## 3. Regex remap table
```python
import re
RULES = [
    (r"^encoder\.layer\.(\d+)\.attention\.self\.", r"blocks.\1.attn."),
    (r"^encoder\.layer\.(\d+)\.output\.dense\.",   r"blocks.\1.mlp.fc2."),
]
def remap(k):
    for pat, rep in RULES:
        k = re.sub(pat, rep, k)
    return k
sd = {remap(k): v for k, v in sd.items()}
```

## 4. Layout changes
- Fused vs separate QKV: `q, k, v = w.chunk(3, dim=0)` or `torch.cat([q, k, v], 0)`; check head interleaving conventions (some codebases interleave per head).
- Conv1D (GPT-2 style) vs Linear: transpose (`w.T`).
- Vocabulary growth: copy old rows into a new larger embedding, init the rest.
- Rotary permutations (Meta to HF Llama conversion) need a specific permute of q/k weights; use the official conversion script.

## 5. Load strictly and verify
```python
res = model.load_state_dict(sd, strict=False)
assert not res.missing_keys and not res.unexpected_keys, res
```
Only allow known-ignorable keys (e.g. `num_batches_tracked`, rotary caches). Then compare outputs on a fixed input against the original implementation (`torch.testing.assert_close(new_out, old_out, atol=1e-4, rtol=1e-4)`).

## Keep it reusable
Save the converted checkpoint in the new format (safetensors) with a version tag, and keep the conversion script in the repo; register a `_register_load_state_dict_pre_hook` if old checkpoints must keep loading transparently.
