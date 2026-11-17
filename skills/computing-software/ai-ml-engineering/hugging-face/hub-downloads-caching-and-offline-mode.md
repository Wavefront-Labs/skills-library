---
id: computing-software.ai-ml-engineering.hugging-face.hub-downloads-caching-and-offline-mode
name: hub-downloads-caching-and-offline-mode
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, hf-hub-download, hf-offline, huggingface-cli, hf-cache, snapshot-download]
level: practitioner
status: verified
description: "Download and cache Hugging Face Hub files with hf_hub_download, snapshot_download and the hf CLI: cache layout, HF_HOME, allow_patterns, offline mode and cache cleanup."
sources:
  - https://huggingface.co/docs/huggingface_hub/guides/download
  - https://huggingface.co/docs/huggingface_hub/guides/manage-cache
  - https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hub downloads, caching and offline mode

## Download
```python
from huggingface_hub import hf_hub_download, snapshot_download
path = hf_hub_download("org/model", "config.json", revision="<sha>")
local = snapshot_download("org/model", revision="<sha>",
                          allow_patterns=["*.safetensors", "*.json", "tokenizer*"],   # skip .bin/.onnx duplicates
                          max_workers=8)
```
CLI (huggingface_hub 2.x ships `hf`; the older `huggingface-cli` command is gone there):
```bash
hf download org/model --revision <sha> --include "*.safetensors" --include "*.json" --local-dir ./model
hf auth login            # older: huggingface-cli login
```
Repeat `--include` for each pattern: `--include "*.json" "*.txt"` treats `*.txt` as a file name and fails (checked with huggingface_hub 2.2.0 on Windows). `--local-dir` also creates a `.cache/` metadata folder inside the target.
Faster large downloads: file transfers go through the `hf_xet` backend; `HF_XET_HIGH_PERFORMANCE=1` is the documented tuning switch. `HF_HUB_ENABLE_HF_TRANSFER` is deprecated and `hf_transfer` can no longer be used.

## Cache layout
Default `~/.cache/huggingface/hub/models--org--model/` with `blobs/` (content-addressed files), `snapshots/<sha>/` (symlinks per revision, checked: `os.path.islink` is True on Windows with symlinks enabled) and `refs/main` (a `trees/` folder also appears). Multiple revisions share identical blobs.
- Move it: `HF_HOME=/data/hf` (everything) or `HF_HUB_CACHE=/data/hf/hub`. Set on shared machines and containers so models land on a big disk.
- Windows without developer mode: no symlinks, so files are stored directly in `snapshots/` and duplicated per revision (per the huggingface_hub cache guide; not reproduced here because symlinks are enabled on this machine).
- `local_dir=` writes a plain copy (no symlinks) for packaging into images.

## Offline
```bash
export HF_HUB_OFFLINE=1          # never call the Hub; use cache only
```
Load with the same repo id and revision (resolved from cache) or a local path. Without offline mode, `from_pretrained` and `hf_hub_download` make a request to check for a newer revision (stated in the huggingface_hub environment-variable docs). Checked: with `HF_HUB_OFFLINE=1` a cached repo loads, and an uncached one raises `OSError: We couldn't connect to 'https://huggingface.co' to load the files, and couldn't find them in the cached files`; `local_files_only=True` per call gives the same error.

## Manage the cache
```bash
hf cache ls                      # older: huggingface-cli scan-cache; one row per cached repo (add --revisions for each revision)
hf cache rm model/org/model      # older: huggingface-cli delete-cache; also takes revision hashes, --dry-run and -y
hf cache prune                   # remove detached revisions and incomplete downloads
hf cache verify org/model        # verify checksums of one repo revision
```
In huggingface_hub 2.2.0 `hf cache scan` and `hf cache delete` do not exist (the subcommands are list/ls, rm, prune, verify). Python: `scan_cache_dir().delete_revisions(*hashes)` returns a `DeleteCacheStrategy` you then call `.execute()` on.

## Containers and CI
- Bake pinned snapshots into the image (`snapshot_download(..., local_dir="/models/x")`) or mount a shared read-only cache volume.
- Pre-download in a build step with a token; run inference with `HF_HUB_OFFLINE=1` so startup never depends on the Hub.
- Rate limits: authenticated requests get higher limits; set `HF_TOKEN` in CI.

## Gotchas
- `revision="main"` caches whatever main was at download time; later runs may fetch new commits.
- A download interrupted mid-way (disk full, dropped connection) leaves `.incomplete` blobs; `hf cache prune` removes them.
- `TRANSFORMERS_CACHE` is not referenced anywhere in transformers 5.20 or huggingface_hub 2.2 (checked by grep): use `HF_HOME`/`HF_HUB_CACHE`.

## Verify
With networking disabled and `HF_HUB_OFFLINE=1`, the service starts and loads the model; `hf cache scan` shows only the expected revisions.
