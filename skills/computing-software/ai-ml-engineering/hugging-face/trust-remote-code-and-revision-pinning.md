---
id: computing-software.ai-ml-engineering.hugging-face.trust-remote-code-and-revision-pinning
name: trust-remote-code-and-revision-pinning
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, trust-remote-code, revision-pinning, supply-chain-security, hub-security]
level: practitioner
status: verified
description: "Handle trust_remote_code safely in transformers: what it executes, review custom modeling files, pin revision to a commit SHA, and prefer native architectures and safetensors."
sources:
  - https://huggingface.co/docs/transformers/models#custom-models
  - https://huggingface.co/docs/hub/security
  - https://huggingface.co/docs/transformers/custom_models
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# trust_remote_code and revision pinning

## What it does
Some repos ship their own Python (`modeling_*.py`, `configuration_*.py`, `tokenization_*.py`) referenced in `config.json` via `auto_map`. `trust_remote_code=True` downloads and **executes** that code in your process with your permissions. A malicious or compromised repo can do anything: read credentials, exfiltrate data, install backdoors. Checked with a local repo whose `modeling_my.py` prints at import: `AutoModel.from_pretrained(dir)` raised `ValueError: The repository ... contains custom code which must be executed`, and with `trust_remote_code=True` the print ran during loading.

## Safe pattern
```python
from transformers import AutoModel, AutoConfig
SHA = "a1b2c3d4..."                                      # full commit hash you reviewed
model = AutoModel.from_pretrained("org/custom-model", trust_remote_code=True, revision=SHA)
```
1. Check whether the architecture is natively supported now (many models start with remote code and get upstreamed). If so, drop `trust_remote_code`.
2. Read the repo's `.py` files at a specific commit on the Hub ("Files and versions" tab).
3. Pin `revision` to that **commit SHA**, not a branch (`main` can change after review) and not only a tag.
4. Pin the same revision for tokenizer and config loads.
5. Run in an isolated environment (container without cloud credentials) when evaluating unknown repos.

## Revision pinning in general
Even without remote code, pin revisions in production: weights, tokenizer files and generation configs on `main` change, silently altering outputs.
```python
tok = AutoTokenizer.from_pretrained(repo, revision=SHA)
from huggingface_hub import snapshot_download
path = snapshot_download(repo, revision=SHA)           # then load from the local path (ran: the snapshot folder is named by the 40-char SHA)
```
Record the SHA in your model registry / run metadata.

## Weights safety
- `.bin` / `.pt` / `.pkl` files are pickles: loading can execute code. Prefer `.safetensors`: with only `pytorch_model.bin` present, the default load succeeded but `use_safetensors=True` raised `OSError: no file named model.safetensors found` (ran, transformers 5.20.2).
- The Hub scans every pushed file with ClamAV and runs a Pickle Import scan that lists the imports a pickle references; the docs say this is not foolproof (huggingface.co/docs/hub/security-pickle). Treat a suspicious import list as a reason to stop, and a clean scan as not proof of safety.
- `torch.load(weights_only=True)` restricts unpickling and is the default in current PyTorch (2.14.1: loading a pickle with a `__reduce__` payload raised `UnpicklingError: Weights only load failed`, payload not run).

## Offline / air-gapped
Mirror the pinned snapshot into an internal artefact store; load with `HF_HUB_OFFLINE=1` and a local path so nothing is fetched at runtime.

## Verify
In CI, assert every `from_pretrained` call has a `revision=` and no unexpected `trust_remote_code=True`; diff the remote code when bumping revisions.
