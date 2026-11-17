---
id: computing-software.ai-ml-engineering.pytorch.streaming-sharded-datasets-webdataset-mosaic
name: streaming-sharded-datasets-webdataset-mosaic
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, webdataset, mosaic-streaming, sharded-datasets, object-storage, iterabledataset, data-loading]
level: practitioner
status: docs-checked
description: "Stream large training sets from object storage as tar or MDS shards with WebDataset or MosaicML Streaming: shuffling, multi-node splitting and resumption."
sources:
  - https://github.com/webdataset/webdataset
  - https://docs.mosaicml.com/projects/streaming/en/stable/
  - https://pytorch.org/docs/stable/data.html#iterable-style-datasets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming sharded datasets (WebDataset / MosaicML Streaming)

Millions of small files on network storage kill throughput (metadata ops, random reads). Pack samples into large shards and read them sequentially.

## Shard design
- Use many more shards than (nodes x GPUs x workers) so every worker gets distinct shards.
- Shuffle samples before writing shards; the runtime only shuffles within a buffer. Mosaic's docs say a dataset that has not been pre-shuffled should use a shuffle-block algorithm.

## WebDataset
Shards are plain tar files named like `something-000000.tar`, specified with brace notation.
```python
import webdataset as wds
url = "pipe:aws s3 cp s3://bucket/train-{000000..001023}.tar -"
ds = (wds.WebDataset(url, shardshuffle=1000, nodesplitter=wds.split_by_node, resampled=False)
        .shuffle(5000)                     # sample buffer
        .decode("pil")
        .to_tuple("jpg", "cls")
        .map_tuple(train_tf, int)
        .batched(64))
loader = wds.WebLoader(ds, batch_size=None, num_workers=8)
```
- `shardshuffle` should be set explicitly (to False or a number): leaving it None warns. It is ignored (with a warning) when `resampled=True`. `nodesplitter` defaults to single-node only, and multi-node training needs an explicit splitter such as `wds.split_by_node`.
- Write: `wds.ShardWriter("train-%06d.tar", maxsize=5e8)` with `sink.write({"__key__": k, "jpg": bytes, "cls": label})`. `maxsize` is the maximum size of each shard (default 3e9).
- The README notes an exactly balanced sample count across many nodes for a fixed epoch size is tricky, and that multi-node training usually uses shard resampling: use `resampled=True` + `.with_epoch(n)` for a fixed number of samples per epoch. The `pipe:` protocol is disabled in WebDataset's security mode.

## MosaicML Streaming
```python
from streaming import MDSWriter, StreamingDataset
with MDSWriter(out="s3://bucket/mds/train", columns={"image": "jpeg", "label": "int"}, compression="zstd") as w:
    for img, y in samples: w.write({"image": img, "label": y})
ds = StreamingDataset(remote="s3://bucket/mds/train", local="/local_nvme/cache", shuffle=True,
                      shuffle_algo="py1e", batch_size=64)   # batch_size = per-device batch
loader = streaming.StreamingDataLoader(ds, batch_size=64, num_workers=8)
```
- `batch_size` of StreamingDataset is the device batch size; set it equal to the DataLoader `batch_size`. `py1e` is the default `shuffle_algo`.
- Mid-epoch resumption: use `StreamingDataLoader`, save `dataloader.state_dict()` with your checkpoint and call `load_state_dict()` on resume.
- Elastic determinism across different GPU counts needs a constant global batch size that is divisible by every GPU count, and the same `num_canonical_nodes`.
- `cache_limit` caps the per-node shard cache and Streaming evicts shards once it is reached; too low a value causes repeated redownloads.
- Mix datasets with `Stream(..., proportion=...)`; `repeat` and `choose` are alternatives, one scheme for all streams.

## Choosing
| Need | Pick |
|---|---|
| Simple, standard tars, any tool can write | WebDataset |
| Exact resumption, deterministic order across GPU counts, dataset mixing | Mosaic Streaming |

## Verify
- Measure samples/s from the loader alone (no model) vs required GPU throughput.
- Check each rank sees different samples in step 0 (log a few keys per rank).

## Checked
2026-11-01. Confirmed from the webdataset repo (README.md; src/webdataset compat.py, shardlists.py, writer.py) and the MosaicML Streaming docs source (docs/source: shuffling, fast_resumption, elastic_determinism, faqs_and_tips, shard_retrieval, mixing_data_sources, basic_dataset_conversion).
Removed: shard size range and shard-count multiplier, the compressed-format advice, the DDP-hang claim, the Hugging Face datasets row, and the claim of deterministic order regardless of node count (now conditioned on global batch size).
Method: documentation only; no commands were run.
