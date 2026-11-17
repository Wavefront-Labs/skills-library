---
id: computing-software.ai-ml-engineering.hugging-face.hfapi-repo-management
name: hfapi-repo-management
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, hfapi, upload-folder, create-repo, huggingface-hub, hub-branches, hub-pull-requests]
level: practitioner
status: gated
description: "Automate Hub repos with huggingface_hub HfApi: create_repo, upload_folder/upload_large_folder with allow patterns, branches and tags, PRs, commits and deletion."
sources:
  - https://huggingface.co/docs/huggingface_hub/guides/upload
  - https://huggingface.co/docs/huggingface_hub/guides/repository
  - https://huggingface.co/docs/huggingface_hub/package_reference/hf_api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HfApi repo management

## Auth
`hf auth login` stores a token (`huggingface-cli login` is dead: the old binary now prints "`huggingface-cli` is deprecated and no longer works. Use `hf` instead"); in CI set `HF_TOKEN`. Use fine-grained tokens with write access to only the needed repos/orgs.

## Create and upload
```python
from huggingface_hub import HfApi
api = HfApi()
repo_id = "my-org/fraud-model"
api.create_repo(repo_id, repo_type="model", private=True, exist_ok=True)
api.upload_folder(repo_id=repo_id, folder_path="outputs/final",      # also takes delete_patterns= to remove remote files in the same commit
                  allow_patterns=["*.safetensors", "*.json", "README.md", "tokenizer*"],
                  ignore_patterns=["checkpoint-*", "*.pt"],
                  commit_message="Train run 2026-10-18, val AUC 0.912")
api.upload_file(path_or_fileobj="metrics.json", path_in_repo="eval/metrics.json", repo_id=repo_id)
```
- Very large folders (hundreds of GB, many files): in huggingface_hub 2.2.0 `HfApi` has no `upload_large_folder` method any more and `hf upload-large-folder` is not a command; per the current upload guide, `upload_folder` and `hf upload` are the route for very large folders, streaming files in several commits and resuming when the same call is re-run. (`upload_large_folder` was the answer in 1.x.)
- `run_as_future=True` (an `upload_folder`/`upload_file` parameter, confirmed in the signature) uploads in the background during training; `TrainingArguments(push_to_hub=True, hub_strategy="every_save")` does this by default (`hub_strategy` options per its docstring: `end`, `every_save`, `checkpoint`, `all_checkpoints`).

## Branches, tags and PRs
```python
api.create_branch(repo_id, branch="experiment-lr3e-4")
api.upload_folder(repo_id=repo_id, folder_path="out", revision="experiment-lr3e-4")
api.create_tag(repo_id, tag="v1.2.0", revision="main")
api.upload_folder(repo_id=repo_id, folder_path="out", create_pr=True)   # opens a PR for review
```
Consumers pin `revision="v1.2.0"` or a commit sha for reproducibility.

## Other operations
- `api.list_repo_files`, `api.list_repo_refs`, `api.list_repo_commits` for audits.
- `api.delete_file`, `api.delete_folder`, `api.super_squash_history` (reclaim storage), `api.update_repo_settings(gated="auto")` (signature accepts `'auto'`, `'manual'` or `False`, plus `private` and `visibility`), `api.delete_repo` (irreversible). All of these methods, and `create_commit` with `CommitOperationAdd`/`CommitOperationDelete`, exist in 2.2.0; none was called against a real repo (no Hub write account here) (gated: unconfirmed, source is paywalled or blocked).
- `api.create_commit` with multiple `CommitOperationAdd/Delete` for atomic multi-file changes.

Signatures checked by introspection on 2.2.0: `create_repo(repo_type, private, exist_ok)`, `upload_folder(allow_patterns, ignore_patterns, commit_message, create_pr, revision, run_as_future)`, `create_branch(branch)`, `create_tag(tag, revision)`, `list_repo_files`, `list_repo_refs`, `list_repo_commits`, `model_info(files_metadata)`. The commands in this skill that create or change Hub repos were not executed (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `api.model_info(repo_id, files_metadata=True)` lists expected files and sizes.
- [ ] Fresh environment `from_pretrained(repo_id, revision=tag)` loads.
