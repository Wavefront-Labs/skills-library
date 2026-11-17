---
id: computing-software.ai-ml-engineering.pytorch.collate-fn-and-padding-variable-length-batches
name: collate-fn-and-padding-variable-length-batches
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, collate-fn, pad-sequence, variable-length, attention-mask, bucketing]
level: practitioner
status: verified
description: "Write PyTorch collate_fn functions that pad variable-length sequences, build attention masks, keep metadata, and reduce padding waste with length bucketing."
sources:
  - https://pytorch.org/docs/stable/data.html#dataloader-collate-fn
  - https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pad_sequence.html
  - https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pack_padded_sequence.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# collate_fn and padding variable-length batches

Default collate stacks tensors, so variable-length items fail with `RuntimeError: stack expects each tensor to be equal size`. Write your own.

## Pad and mask
```python
from torch.nn.utils.rnn import pad_sequence
PAD = 0
def collate(batch):                       # batch: list of dicts from __getitem__
    ids = [torch.as_tensor(b["input_ids"]) for b in batch]
    lengths = torch.tensor([len(x) for x in ids])
    input_ids = pad_sequence(ids, batch_first=True, padding_value=PAD)
    attn = (torch.arange(input_ids.size(1))[None, :] < lengths[:, None]).long()
    labels = pad_sequence([torch.as_tensor(b["labels"]) for b in batch], batch_first=True, padding_value=-100)
    return {"input_ids": input_ids, "attention_mask": attn, "labels": labels,
            "lengths": lengths, "ids": [b["id"] for b in batch]}
loader = DataLoader(ds, batch_size=32, collate_fn=collate, num_workers=4)
```
- Pad labels with `-100`, the default `ignore_index` of `CrossEntropyLoss`, so padding contributes no loss.
- Padding side: right for encoders and training; left for batched generation with decoder-only LMs.
- `pin_memory=True` pins tensors inside dicts/lists/tuples automatically; custom batch classes need a `pin_memory()` method.

## RNNs: pack to skip padding
```python
packed = nn.utils.rnn.pack_padded_sequence(emb, lengths.cpu(), batch_first=True, enforce_sorted=False)
out, h = lstm(packed)
out, _ = nn.utils.rnn.pad_packed_sequence(out, batch_first=True)
```
`lengths` must be on the CPU (a Python list also works); the function casts it to int64 itself (read in torch/nn/utils/rnn.py).

## Reduce padding waste: bucketing
Random batches pad to the longest item; with long-tailed lengths most compute is padding.
- Sort within large random chunks: take 100 x batch_size indices, sort by length, cut into batches, shuffle batches. Implement as a `batch_sampler`.
- Or token-budget batching: fill each batch up to N total tokens.
- HF: `DataCollatorWithPadding(pad_to_multiple_of=8)`; in current transformers `TrainingArguments(train_sampling_strategy="group_by_length")` selects `LengthGroupedSampler` (older releases used `group_by_length=True`; checked against the main-branch source).

## Gotchas
- Collate runs in worker processes: must be picklable (top-level function or `functools.partial`, not a lambda on Windows/macOS spawn).
- Heavy work (tokenisation) belongs in `__getitem__` or preprocessing, not collate, so it parallelises evenly.
- `pad_to_multiple_of=8` keeps shapes tensor-core friendly and reduces `torch.compile` recompiles from varied shapes.

## Verify
Print the padding fraction `1 - attn.sum() / attn.numel()` over 100 batches before and after bucketing.
