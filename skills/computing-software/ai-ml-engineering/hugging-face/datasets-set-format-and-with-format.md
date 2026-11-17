---
id: computing-software.ai-ml-engineering.hugging-face.datasets-set-format-and-with-format
name: datasets-set-format-and-with-format
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, with-format, set-format, datasets, to-pandas, torch-format, arrow]
level: practitioner
status: verified
description: "Control how Hugging Face Datasets returns rows: set_format and with_format for torch/numpy/pandas/polars/arrow, column selection, on-the-fly transforms and pandas conversion."
sources:
  - https://huggingface.co/docs/datasets/use_with_pytorch
  - https://huggingface.co/docs/datasets/process#format
  - https://huggingface.co/docs/datasets/package_reference/main_classes#datasets.Dataset.with_format
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# set_format / with_format and conversion to pandas

Datasets stores data in Arrow and returns Python objects by default. Formatting changes what `ds[i]`, slicing and iteration return, without copying the underlying data.

## Formats
```python
ds = ds.with_format("torch", columns=["input_ids", "attention_mask", "label"], device="cuda")   # returns a new view
ds.set_format("numpy")          # in place
ds.reset_format()
ds.format                       # current type, columns, output_all_columns
```
Types: `None` (Python), `"numpy"`, `"torch"`, `"tensorflow"`, `"jax"`, `"pandas"`, `"polars"`, `"arrow"`.
- `columns=[...]` limits returned columns; `output_all_columns=True` returns others as Python objects.
- Ragged lists (variable-length tokens) become lists of tensors, not a padded tensor: pad in the collator.
- `with_format` returns a new dataset object (preferred in pipelines); `set_format` mutates.

## On-the-fly transforms
```python
def tf(batch):
    batch["pixel_values"] = [train_tf(img.convert("RGB")) for img in batch["image"]]
    return batch
ds = ds.with_transform(tf)      # applied lazily at access; nothing cached
```
Use for random augmentation (map would freeze one augmentation into the cache). `with_transform` overrides formatting; return tensors yourself.

## pandas / polars
```python
df = ds.to_pandas()                     # whole dataset into memory
for chunk in ds.to_pandas(batched=True, batch_size=100_000): ...
ds.with_format("pandas")[:1000]         # slice as DataFrame
pl_df = ds.to_polars()
ds2 = Dataset.from_pandas(df, preserve_index=False)
```
- Large datasets: iterate in batches or use `ds.to_parquet` / DuckDB on the Parquet files instead of a full DataFrame.
- `from_pandas` keeps the index as a column `__index_level_0__` unless `preserve_index=False`.

## Performance
- Formats other than Python avoid per-element conversion; time your own pipeline before choosing `"numpy"` or `"arrow"` (not benchmarked here).
- `with_format("torch", device=...)` is documented to place tensors on the device directly (checked with `device="cpu"`; GPU not tested here).

## Gotchas
- Image and Audio features are decoded on access, which can be slow; decode and resize in a `with_transform` function (not benchmarked here).
- In datasets 5.1.0 a `with_format("numpy")` dataset keeps its format through `save_to_disk` / `load_from_disk`; on older releases reapply the format after loading and check `ds.format`.
