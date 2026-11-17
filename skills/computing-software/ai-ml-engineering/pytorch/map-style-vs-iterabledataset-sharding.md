---
id: computing-software.ai-ml-engineering.pytorch.map-style-vs-iterabledataset-sharding
name: map-style-vs-iterabledataset-sharding
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, iterabledataset, map-style-dataset, worker-sharding, get-worker-info, streaming-data]
level: practitioner
status: verified
description: "Choose map-style Dataset or IterableDataset in PyTorch and shard an IterableDataset across DataLoader workers and DDP ranks without duplicated samples."
sources:
  - https://pytorch.org/docs/stable/data.html#dataset-types
  - https://pytorch.org/docs/stable/data.html#torch.utils.data.IterableDataset
  - https://pytorch.org/docs/stable/data.html#torch.utils.data.get_worker_info
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map-style vs IterableDataset

## Choose
- **Map-style** (`__getitem__`, `__len__`): random access available (files on local disk, arrays, a DB with keys). Gets shuffling, samplers, `DistributedSampler` and exact epoch length for free. Default choice.
- **IterableDataset** (`__iter__`): data only readable sequentially (streams, huge sharded tar/parquet in object storage, generated data). You own shuffling and sharding.

## The duplication bug
Every DataLoader worker gets a copy of the IterableDataset and calls `__iter__`. Without sharding, `num_workers=4` yields every sample 4 times (run here with 2 workers over 12 items: every item appeared twice); with DDP on 8 GPUs and 4 workers each, 32 times.

## Shard by rank and worker
```python
import torch.distributed as dist
from torch.utils.data import IterableDataset, get_worker_info
class ShardedFiles(IterableDataset):
    def __init__(self, files):
        self.files = files
        # read rank/world HERE, in the main process: DataLoader workers started with
        # spawn (always on Windows/macOS) have no initialised process group
        self.rank, self.world = (dist.get_rank(), dist.get_world_size()) if dist.is_initialized() else (0, 1)
    def __iter__(self):
        rank, world = self.rank, self.world
        wi = get_worker_info()
        wid, nw = (wi.id, wi.num_workers) if wi else (0, 1)
        shard, nshards = rank * nw + wid, world * nw
        for f in self.files[shard::nshards]:
            yield from read_records(f)
```
- Run on 2 gloo ranks x 4 workers over 16 files of 3 records on Windows: the sharded class yielded 24 records per rank, 48 unique in total. The earlier version that called `dist.get_rank()` inside `__iter__` yielded 48 per rank and only 48 unique among 96, because the spawned workers saw `dist.is_initialized() == False` and every rank read the same shards.
- Shard at file granularity; aim for many more files than `world * num_workers` or some workers sit idle (with 3 files and 8 shards, 5 shards were empty).
- Shuffle: shuffle the file list per epoch with a seed shared across ranks (`random.Random(seed + epoch)`), then use a local shuffle buffer of a few thousand records.
- Unequal shard sizes make DDP ranks finish at different steps and hang on the next all-reduce (the standard DDP failure mode that `Join` exists for). Fix by capping steps per epoch (`itertools.islice`), using `torch.distributed.algorithms.join.Join` (imports in 2.14), or padding shards.

## Other points
- `len()` is undefined for IterableDataset; schedulers needing total steps must use an estimate.
- `shuffle=True` raises `ValueError: DataLoader with IterableDataset: expected unspecified shuffle option, but got shuffle=True`, and `len()` of the dataset raises `TypeError: object of type ... has no len()`.
- Libraries that already do this: Hugging Face `datasets` streaming (`split_dataset_by_node` exists in `datasets.distributed`), WebDataset, torchdata nodes (`torchdata.nodes` in the torchdata README), MosaicML Streaming (existence of each confirmed from its repository). Prefer them for object storage.
- Map-style over many small files on network storage is slow; pack into shards and go iterable.

## Verify
Iterate one epoch with `num_workers=4` on 2 ranks, collect sample IDs, and assert `len(ids) == len(set(ids)) == expected_total`.
