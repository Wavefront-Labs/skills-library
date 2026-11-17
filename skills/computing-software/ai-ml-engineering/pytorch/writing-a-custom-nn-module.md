---
id: computing-software.ai-ml-engineering.pytorch.writing-a-custom-nn-module
name: writing-a-custom-nn-module
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, custom-nn-module, nn-module, extra-repr, submodule-registration, torch-nn]
level: practitioner
status: verified
description: "Write custom nn.Module classes correctly: registration rules for submodules/params/buffers, forward contracts, extra_repr, device/dtype-safe init and hooks for state_dict."
sources:
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html
  - https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html
  - https://pytorch.org/docs/stable/notes/modules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing a custom nn.Module

**Goal:** a module whose parameters are found by the optimizer, moved by `.to()`, saved by `state_dict()` and printed usefully.

## Skeleton
```python
import torch, torch.nn as nn, torch.nn.functional as F

class GatedMLP(nn.Module):
    def __init__(self, d, hidden, dropout=0.0, *, device=None, dtype=None):
        super().__init__()                         # must come first
        kw = dict(device=device, dtype=dtype)
        self.up = nn.Linear(d, 2 * hidden, **kw)   # submodule: auto-registered
        self.down = nn.Linear(hidden, d, **kw)
        self.scale = nn.Parameter(torch.ones(d, **kw))          # trainable
        self.register_buffer("step", torch.zeros((), dtype=torch.long, device=device))  # saved, not trained
        self.register_buffer("cache", None, persistent=False)   # moved by .to(), not saved
        self.dropout = dropout
        self.hidden = hidden

    def forward(self, x):
        a, b = self.up(x).chunk(2, dim=-1)
        h = F.dropout(F.silu(a) * b, self.dropout, self.training)
        return self.down(h) * self.scale

    def extra_repr(self):
        return f"hidden={self.hidden}, dropout={self.dropout}"
```

## Registration rules
- Assigning an `nn.Module`, `nn.Parameter` or calling `register_buffer` registers it. A plain tensor attribute is **not** registered: it will not move with `.to()` and is not saved.
- Python lists/dicts of modules are invisible (a module holding `[nn.Linear(2, 2)]` in a list had 0 parameters); use `nn.ModuleList`/`nn.ModuleDict`/`nn.ParameterList`. The skeleton above was run: parameter count, `state_dict` keys (`scale`, `step`, `up.*`, `down.*`; the non-persistent `cache` is absent), `strict=True` round trip and `device="meta"` construction all behave as described.
- Use `self.training` (not a custom flag) for train/eval behaviour so `model.eval()` works.
- Accept `device`/`dtype` kwargs so the module can be built on the meta device or directly on GPU.
- Call the module (`self.up(x)`), never `self.up.forward(x)`, so hooks run (checked: a forward hook fired once for a call and not for a direct `.forward`). Assigning a submodule before `super().__init__()` raises `AttributeError: cannot assign module before Module.__init__() call`.

## Initialization
Put custom init in `reset_parameters()` and call it at the end of `__init__`; frameworks (FSDP meta init, `to_empty`) call it again.

## State-dict compatibility
- Renaming attributes renames keys and breaks old checkpoints; handle with `_load_from_state_dict` or a key-remap function.
- `_register_load_state_dict_pre_hook` / `register_state_dict_post_hook` let you migrate keys in one place.

## Verify
- [ ] `sum(p.numel() for p in m.parameters())` equals the expected count.
- [ ] `m.to("cuda")` then all params/buffers report `cuda` (`{t.device for t in m.state_dict().values()}`).
- [ ] `m.load_state_dict(m.state_dict())` passes with `strict=True`; `print(m)` shows `extra_repr` values.
