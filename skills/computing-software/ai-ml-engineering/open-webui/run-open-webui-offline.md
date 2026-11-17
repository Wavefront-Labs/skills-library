---
id: computing-software.ai-ml-engineering.open-webui.run-open-webui-offline
name: run-open-webui-offline
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [offline-mode, air-gapped, huggingface, embeddings, whisper, internal-network]
level: advanced
status: docs-checked
description: "Prepare Open WebUI for offline use: pre-download embedding and Whisper caches, set OFFLINE_MODE and HF_HUB_OFFLINE, isolate the network, and verify chat and RAG."
sources:
  - https://docs.openwebui.com/tutorials/maintenance/offline-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Open WebUI with no internet. Offline settings only block selected downloads and update checks; they do not block outbound connections, so isolation needs firewall or container-network controls. (Community tutorial.)

## What must be local first
A local inference server and model (for example Ollama; select a local, not cloud, model), a downloaded embedding model, local document extraction and any reranker, the image/packages and persistent caches, an auth method reachable on the isolated network, and local speech models if needed. Check Admin Settings > Documents: a local chat model alone does not make document processing local.

## Prepare while connected
Install, send a chat, configure extraction and embeddings, download the embedding model via Admin Settings > Documents (for example `sentence-transformers/all-MiniLM-L6-v2`), upload a small file and ask about it, then restart once to confirm persistent storage works.

## Prepare for an already-offline target
Download on a staging machine and transfer, keeping cache directory structure and symlinks intact. Embedding:
```python
from huggingface_hub import snapshot_download
snapshot_download(repo_id="sentence-transformers/all-MiniLM-L6-v2", cache_dir="/path/to/embedding-cache")
```
Copy the contents to `/app/backend/data/cache/embedding/models/` and set `RAG_EMBEDDING_MODEL` to the identifier. Whisper (optional): same with `repo_id="Systran/faster-whisper-large-v3"`, copy to `/app/backend/data/cache/whisper/models/`, set `WHISPER_MODEL=Systran/faster-whisper-large-v3` (custom location: `WHISPER_MODEL_DIR`). TTS: use a local service such as Openedai-speech with voices pre-fetched.

## Settings
```bash
OFFLINE_MODE=true
HF_HUB_OFFLINE=1
RAG_EMBEDDING_MODEL_AUTO_UPDATE=false
RAG_RERANKING_MODEL_AUTO_UPDATE=false
WHISPER_MODEL_AUTO_UPDATE=false
```
`OFFLINE_MODE=true` alone sets `HF_HUB_OFFLINE=1`, disables the version check and forces the three auto-update flags false (the extra lines are redundant but harmless); `ENABLE_VERSION_UPDATE_CHECK=false` turns off only the version check. `WHISPER_MODEL_AUTO_UPDATE=false` alone does not stop a download: if the model is missing, Open WebUI retries with downloads enabled and only `HF_HUB_OFFLINE=1` blocks that.

## Isolate the network (Compose example)
Mount `./open-webui-data:/app/backend/data`, `./models/embedding-cache:/app/backend/data/cache/embedding/models/`, optional `./models/whisper-cache:/app/backend/data/cache/whisper/models/`, and attach to a network defined with `internal: true` (for example `open-webui-internal-network`, driver bridge). A reverse proxy and your local model/processing services must join that network.

## Verify
Restart, check logs for attempted downloads, sign in with the offline auth method, send a chat, upload a new small document with a distinctive fact, ask about it, and confirm in the firewall that external access is blocked.

## Gotchas
- With `HF_HUB_OFFLINE=1` and no cache, a fresh install may start but fail on first document upload with "No embedding model is loaded" (see startup troubleshooting).
- Cloud models, hosted web search and external OAuth stop working offline.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: tutorials/maintenance/offline-mode (read in full). Nothing removed.
Method: documentation only; no commands were run.
