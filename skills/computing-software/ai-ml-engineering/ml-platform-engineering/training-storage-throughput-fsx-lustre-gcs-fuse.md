---
id: computing-software.ai-ml-engineering.ml-platform-engineering.training-storage-throughput-fsx-lustre-gcs-fuse
name: training-storage-throughput-fsx-lustre-gcs-fuse
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, fsx-lustre, gcs-fuse, training-storage, data-loading, checkpointing]
level: practitioner
status: draft
description: "Feed GPUs fast enough: FSx for Lustre linked to S3, GCS FUSE CSI with file caching, sizing throughput per GPU, sharded formats, and checkpoint write bandwidth."
sources:
  - https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html
  - https://docs.aws.amazon.com/fsx/latest/LustreGuide/performance.html
  - https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/cloud-storage-fuse-csi-driver
  - https://cloud.google.com/storage/docs/cloud-storage-fuse/file-caching
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Training storage throughput (FSx for Lustre, GCS FUSE)

**Goal:** GPUs never wait on input data or checkpoint writes, at the lowest storage cost that achieves it.

## Size the requirement
Required read throughput = samples/s per GPU x bytes/sample x GPUs (plus epochs re-reading). Checkpoint bandwidth = checkpoint size / acceptable pause (e.g. 500 GB in 2 minutes = ~4 GB/s). Confirm the bottleneck first: low GPU utilisation with dataloader workers busy on I/O wait, or `torch.profiler` showing long data-loading steps.

## FSx for Lustre (AWS)
- Link to S3 with a data repository association: files appear immediately (metadata), content lazy-loads on first read; export writes back to S3.
- Deployment types: Scratch (temporary, cheapest, no replication) for short jobs; Persistent 2 for long-lived shared data. Throughput scales with storage: per-TiB tiers (e.g. 125-1000 MB/s/TiB) - a small file system is a slow file system.
- Mount: `sudo mount -t lustre -o relatime,flock fs-0abc.fsx.us-east-1.amazonaws.com@tcp:/<mountname> /fsx`; on EKS use the FSx CSI driver; SageMaker training accepts `FileSystemInput`.
- Pre-warm before training to avoid first-epoch lazy-load stalls: `find /fsx/data -type f -print0 | xargs -0 -n 64 -P 16 sudo lfs hsm_restore`.
- Large files: stripe across OSTs (`lfs setstripe -c -1 /fsx/ckpt`) for parallel checkpoint writes.
- Place file system in the same AZ as the GPU nodes (EFA clusters are single-AZ anyway).

## GCS FUSE (GKE)
```yaml
metadata:
  annotations:
    gke-gcsfuse/volumes: "true"
spec:
  volumes:
  - name: data
    csi:
      driver: gcsfuse.csi.storage.gke.io
      volumeAttributes:
        bucketName: ml-train-data
        mountOptions: "implicit-dirs,file-cache:max-size-mb:-1,file-cache:cache-file-for-range-read:true,metadata-cache:ttl-secs:-1"
```
Enable the file cache on local SSD for multi-epoch training, parallel downloads for large files, and long metadata TTLs for read-only data. For heavy small-file or checkpoint workloads consider Parallelstore or managed Lustre on Google Cloud.

## Data format matters more than storage
Millions of small files kill any file system's metadata path. Pack into shards (WebDataset tar, TFRecord, MosaicML MDS, Parquet) of 100 MB-1 GB and stream sequentially; read directly from object storage with high parallelism when the format supports it.

## Checkpoints
Write asynchronously (PyTorch DCP async save) to local NVMe first, then upload; or to Lustre striped directories. Keep only N recent checkpoints on the fast tier; tier older ones to object storage.

## Verify
- [ ] Measured read throughput (fio or a dataloader benchmark) exceeds requirement with headroom.
- [ ] GPU utilisation unchanged between first and later epochs (no lazy-load stall).
- [ ] Checkpoint save time within the target pause.
