---
id: computing-software.ai-ml-engineering.vllm.lora-resolver-plugins
name: lora-resolver-plugins
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [lora-resolver, lora-filesystem-resolver, lora-hf-hub-resolver, vllm-plugins]
level: advanced
status: docs-checked
description: "Auto-load LoRA adapters on first request with the filesystem and Hugging Face Hub resolvers or a custom LoRAResolver."
sources:
  - https://docs.vllm.ai/en/latest/features/lora/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: resolve and load a LoRA adapter the first time a request names it.

On each request with a model name that has not been loaded, the `LoRAResolver` tries to resolve and load the adapter. With several resolver plugins (for example local files and S3), vLLM loads the first adapter it finds. Enabling either built-in resolver requires `VLLM_ALLOW_RUNTIME_LORA_UPDATING=True`.

Built-in resolvers:
- Local directory: set `VLLM_PLUGINS` to include `lora_filesystem_resolver` and `VLLM_LORA_RESOLVER_CACHE_DIR` to a directory. For a request using adapter `foobar`, vLLM looks for a directory `foobar` there and loads it as an adapter; once loaded it stays available.
- Hugging Face Hub: set `VLLM_PLUGINS` to include `lora_hf_hub_resolver` and `VLLM_LORA_RESOLVER_HF_REPO_LIST` to a comma-separated list of repo IDs. For a request for `my/repo/subpath`, vLLM downloads `subpath` of `my/repo` if it contains an `adapter_config.json`, then serves from the cached directory. The docs warn that enabling remote downloads is insecure and not intended for production.

Custom plugin:
1. Subclass `LoRAResolver` (from `vllm.lora.resolver`) and implement `async resolve_lora(self, base_model_name, lora_name)` returning a `LoRARequest(lora_name=..., lora_path=..., lora_int_id=...)`. The docs example downloads from S3 using `S3_PATH_TEMPLATE` and `LOCAL_PATH_TEMPLATE` environment variables.
2. Register it:

```python
from vllm.lora.resolver import LoRAResolverRegistry
LoRAResolverRegistry.register_resolver("s3_resolver", S3LoRAResolver())
```

See the vLLM Plugins System design page for packaging details.

## Checked

2026-11-03. Confirmed against the LoRA Adapters page (docs.vllm.ai/en/latest/): LoRAResolver behaviour, built-in resolvers, environment variables and custom plugin example.

Method: documentation only; no commands were run.
