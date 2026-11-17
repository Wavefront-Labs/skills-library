---
id: computing-software.ai-ml-engineering.pytorch.modulelist-moduledict-and-sequential
name: modulelist-moduledict-and-sequential
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, modulelist, moduledict, sequential, parameter-registration, nn-module]
level: practitioner
status: verified
description: "Use nn.ModuleList, nn.ModuleDict, nn.Sequential and ParameterList so submodules register parameters, move with .to(), save in state_dict and reach the optimizer."
sources:
  - https://pytorch.org/docs/stable/generated/torch.nn.ModuleList.html
  - https://pytorch.org/docs/stable/generated/torch.nn.ModuleDict.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Sequential.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ModuleList, ModuleDict and Sequential

## The bug these prevent
```python
self.layers = [nn.Linear(64, 64) for _ in range(4)]     # plain list: NOT registered
```
Parameters in a plain list or dict are invisible to `model.parameters()`, `.to(device)`, `state_dict()` and `.train()/.eval()`. Symptoms: those layers never train, or "Expected all tensors to be on the same device". Use containers:
```python
self.layers = nn.ModuleList(nn.Linear(64, 64) for _ in range(4))
self.heads = nn.ModuleDict({"cls": nn.Linear(64, 10), "reg": nn.Linear(64, 1)})
self.scales = nn.ParameterList(nn.Parameter(torch.ones(64)) for _ in range(4))
```

## Which container
- `nn.Sequential`: fixed chain where each output feeds the next and `forward` is implied. Accepts an `OrderedDict` for named layers (`model.encoder.conv1`). Slicing returns a new Sequential: `backbone = resnet_seq[:-1]`.
- `nn.ModuleList`: you write `forward` yourself (skip connections, conditional layers, returning intermediates). Supports `append`, `extend`, `insert`, indexing.
- `nn.ModuleDict`: keyed by string (multi-task heads, per-domain adapters). Keys must be strings without dots.
- `nn.ParameterList` / `nn.ParameterDict`: same, for raw `nn.Parameter`s.

## Gotchas
- State dict keys include the index or key: `layers.0.weight`. Reordering, inserting or changing the container type breaks checkpoint loading. Plan names early or write a key-remap function on load.
- `nn.Sequential` forwards a single positional input; for multiple inputs use ModuleList with an explicit loop.
- Don't reuse the same module instance twice in a container unless you want weight sharing; `nn.ModuleList([layer] * 4)` shares one layer four times. Use a comprehension.
- Assigning a plain tensor attribute that should move with the model: register it with `self.register_buffer("mask", m, persistent=False)`.

## Verify
```python
print(sum(p.numel() for p in model.parameters()))   # matches your expected count
print([n for n, _ in model.named_parameters()])     # every layer appears
```
