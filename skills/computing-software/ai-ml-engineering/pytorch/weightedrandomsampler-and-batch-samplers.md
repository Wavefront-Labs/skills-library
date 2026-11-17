---
id: computing-software.ai-ml-engineering.pytorch.weightedrandomsampler-and-batch-samplers
name: weightedrandomsampler-and-batch-samplers
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, weightedrandomsampler, batch-sampler, sampler, class-imbalance, distributedsampler]
level: practitioner
status: verified
description: "Use PyTorch samplers well: WeightedRandomSampler for imbalance, custom BatchSampler for bucketing or balanced batches, and combining them with DistributedSampler."
sources:
  - https://pytorch.org/docs/stable/data.html#torch.utils.data.WeightedRandomSampler
  - https://pytorch.org/docs/stable/data.html#torch.utils.data.BatchSampler
  - https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Samplers: WeightedRandomSampler and BatchSampler

## WeightedRandomSampler for class imbalance
```python
counts = torch.bincount(labels)                     # labels: tensor of all train labels
w_per_class = 1.0 / counts.float()
sample_w = w_per_class[labels]
sampler = WeightedRandomSampler(sample_w, num_samples=len(labels), replacement=True)
loader = DataLoader(ds, batch_size=64, sampler=sampler)   # no shuffle=True with a sampler
```
- Weights are per sample, not per class; they need not sum to 1.
- `replacement=True` is the normal setting; minority samples repeat within an epoch, so pair with augmentation.
- Fully balanced sampling distorts predicted probabilities toward the minority; recalibrate or adjust the decision threshold, and evaluate on the natural distribution. A softer option: weight by `counts ** -0.5`.
- Alternatives: class-weighted loss (`CrossEntropyLoss(weight=...)`), focal loss. Don't stack both strong weighting methods at once.

## Custom BatchSampler
A batch sampler yields lists of indices; pass it as `batch_sampler=` (then omit `batch_size`, `shuffle`, `sampler`, `drop_last`).
```python
class BucketBatchSampler(torch.utils.data.Sampler):
    def __init__(self, lengths, batch_size, chunk=100, seed=0):
        self.lengths, self.bs, self.chunk, self.seed, self.epoch = lengths, batch_size, chunk, seed, 0
    def set_epoch(self, e): self.epoch = e
    def __iter__(self):
        g = torch.Generator().manual_seed(self.seed + self.epoch)
        idx = torch.randperm(len(self.lengths), generator=g).tolist()
        batches = []
        for i in range(0, len(idx), self.bs * self.chunk):
            c = sorted(idx[i:i + self.bs * self.chunk], key=lambda j: self.lengths[j])
            batches += [c[k:k + self.bs] for k in range(0, len(c), self.bs)]
        for b in torch.randperm(len(batches), generator=g).tolist():
            yield batches[b]
    def __len__(self): return (len(self.lengths) + self.bs - 1) // self.bs
```
Same pattern for class-balanced batches (k samples from each of m classes, needed for metric learning losses).

## With DDP
- `DistributedSampler(ds, shuffle=True)` + `sampler.set_epoch(epoch)` every epoch; without `set_epoch` every epoch has the same order.
- WeightedRandomSampler is not distributed-aware. Options: give each rank its own sampler with a different seed and `num_samples=len//world`, or use a distributed weighted sampler (Catalyst `DistributedSamplerWrapper`).
- Custom batch samplers under DDP must slice by rank themselves and yield the same number of batches on every rank, or training hangs.

## Verify
Count labels drawn over one epoch (`torch.bincount(torch.cat([y for _, y in loader]))`) and confirm the intended balance.
