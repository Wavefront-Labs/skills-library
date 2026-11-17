---
id: computing-software.ai-ml-engineering.hugging-face.large-files-xet-and-git-lfs-on-the-hub
name: large-files-xet-and-git-lfs-on-the-hub
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, xet-storage, git-lfs, hub, large-files, upload-folder, hf-xet]
level: practitioner
status: docs-checked
description: "Store and move large models and datasets on the Hugging Face Hub: Xet storage vs Git LFS, upload_folder, file and repo limits, high-performance transfers and cleaning history."
sources:
  - https://huggingface.co/docs/hub/storage-backends
  - https://huggingface.co/docs/hub/storage-limits
  - https://huggingface.co/docs/huggingface_hub/guides/upload
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Large files with Xet / LFS and repo limits

## Storage backends
- **Xet**: the Hub's current storage backend, with chunk-level deduplication, smaller uploads and faster downloads than Git LFS. Large files stay out of the Git history as pointer files (identified through `.gitattributes`) while the data lives in remote storage. `hf_xet` is installed with `huggingface_hub` by default (since 0.32.0); to install it explicitly use `pip install -U "huggingface_hub[hf_xet]"`.
- **Git LFS**: the historical backend, still supported (see the Backwards Compatibility page of the Xet docs).

## Upload big things
```python
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(repo_id="org/model", folder_path="out/", allow_patterns=["*.safetensors", "*.json"])
```
CLI: `hf upload org/model ./out .` (same helpers underneath).
- With `hf_xet` installed, `upload_folder()` streams files and splits folders with many files into several commits (follow-up commit messages get a `(part 2)` suffix).
- It is resumable: re-run the same call and already-committed files are skipped. Exception: with `create_pr=True` a re-run opens a new PR, so resume with `revision="refs/pr/N"`.
- Shard large weights so no single file is enormous.

## Limits and recommendations (check the storage-limits page for current values)
Recommended values from the Storage Limits page:
- File size under 200 GB (split larger data into chunks); 500 GB is the hard limit for a single file.
- Under 100k files per repo; merge small files (Parquet, WebDataset, jsonl).
- Under 10k entries per folder: use subdirectories.
- Commits of fewer than 100 files; if you commit manually keep around 50-100 files per commit (HTTP requests time out at 60 s).
- No hard limit on commits, but the Hub degrades after a few thousand; squash history to start fresh.
- Account storage quotas depend on plan; see the page.

## Fast download
`hf_xet` is enabled by default. For maximum throughput set `HF_XET_HIGH_PERFORMANCE=1`; it will use all available bandwidth and CPU cores. The legacy `HF_HUB_ENABLE_HF_TRANSFER=1` flag is no longer used (`hf_transfer` was removed in favour of `hf_xet`).

## Cleaning history
Deleting a file in a new commit keeps old LFS versions in storage. To reclaim space use `super_squash_history` (Hub Python library or API only): it compresses the whole Git history into one commit, is destructive and cannot be undone, and the quota change can take up to 36 hours to show. Individual LFS files can also be deleted from the repo settings Storage section (\"List LFS files\").

## Git workflow (when needed)
```bash
git lfs install
git clone https://huggingface.co/org/model
```
Prefer `huggingface_hub` Python/CLI over git for big uploads.

## Checked
2026-11-01. Confirmed against the Hub Storage Limits page, the Xet storage-backend page and the huggingface_hub upload guide: Xet adoption, chunk dedup, `hf_xet` installed by default (0.32.0), `upload_folder`/`hf upload` splitting and resuming, `HF_XET_HIGH_PERFORMANCE=1`, removal of `hf_transfer`, size/file/folder/commit recommendations, `super_squash_history` behaviour. Removed: `upload_large_folder` and `hf upload-large-folder` (not on the pages read), the 10 MB git threshold, `GIT_LFS_SKIP_SMUDGE`, `hf download` and `max_workers` examples, the 50 GB figure (page says 200 GB recommended, 500 GB hard).
Method: documentation only; no commands were run.
