---
id: computing-software.data-engineering.polars.io-cloud-storage-read-write
name: io-cloud-storage-read-write
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, cloud-storage, s3, scan-parquet, pyarrow-dataset, polars-io-cloud, write-parquet, fsspec]
level: practitioner
status: docs-checked
description: "Read, scan with pushdown, and write Parquet or CSV on S3, Azure Blob or GCS from Polars, including PyArrow datasets and writing via file objects."
sources:
  - https://docs.pola.rs/user-guide/io/cloud-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move data to and from cloud object storage; the API is the same for AWS S3, Azure Blob Storage and Google Cloud Storage.

Dependencies (Python): `pip install fsspec s3fs adlfs gcsfs` (may be needed depending on provider/use case). Rust: `cargo add aws_sdk_s3 aws_config tokio --features tokio/full`.

Read (Parquet, CSV, IPC and NDJSON supported)
```python
df = pl.read_parquet("s3://bucket/*.parquet")
```

Scan with query optimisation
`pl.scan_*` benefits from predicate and projection pushdown, applied before the file is downloaded, which can greatly reduce downloaded data. Evaluation runs on `collect`.
```python
df = pl.scan_parquet("s3://bucket/*.parquet").filter(pl.col("id") < 100).select("id","value").collect()
```

PyArrow datasets (useful for partitioned datasets such as Hive)
```python
import pyarrow.dataset as ds
dset = ds.dataset("s3://my-partitioned-folder/", format="parquet")
pl.scan_pyarrow_dataset(dset).filter(pl.col("foo") == "a").select(["foo", "bar"]).collect()
```

Write: pass a cloud URL.
```python
df.write_parquet("s3://bucket/my_file.parquet")
```

Write through a file object (for things not natively supported, e.g. compressed CSV to cloud):
```python
import s3fs, gzip
fs = s3fs.S3FileSystem()
with fs.open("s3://bucket/my_file.csv.gz", "wb") as cloud_f:
    with gzip.open(cloud_f, "w") as f:
        df.write_csv(f)
```

Any Python file object that supports writes works with `DataFrame` writers. For credentials and retries see io-cloud-credentials-and-retries.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
