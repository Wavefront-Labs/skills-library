---
id: computing-software.ai-ml-engineering.vllm.lora-dynamic-loading
name: lora-dynamic-loading
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [lora-dynamic-loading, load-lora-adapter, vllm-allow-runtime-lora-updating, load-inplace]
level: advanced
status: docs-checked
description: "Load, unload and replace LoRA adapters at runtime through /v1/load_lora_adapter, with the security caveat."
sources:
  - https://docs.vllm.ai/en/latest/features/lora/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change LoRA adapters on a running server without restarting it.

Warning from the docs: this feature has security risks and should not be used in production unless the environment is isolated and fully trusted. Enable it first:

```bash
export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True
```

Load:

```bash
curl -X POST http://localhost:8000/v1/load_lora_adapter \
  -H "Content-Type: application/json" \
  -d '{"lora_name": "sql_adapter", "lora_path": "/path/to/sql-lora-adapter"}'
```

Success returns HTTP 200 and `Success: LoRA adapter 'sql_adapter' added successfully`; errors such as an adapter that cannot be found or loaded return an error message.

Unload by sending `{"lora_name": "sql_adapter"}` to `/v1/unload_lora_adapter` (the page says name or ID); success returns `Success: LoRA adapter 'sql_adapter' removed successfully`.

In-place reload: to replace an existing adapter with updated weights under the same name, add `"load_inplace": true` to the load request. This is common in asynchronous reinforcement learning setups where adapters are continuously swapped in without interrupting inference. With `load_inplace=True` vLLM replaces the existing adapter.

```bash
curl -X POST http://localhost:8000/v1/load_lora_adapter -H "Content-Type: application/json" \
  -d '{"lora_name": "my-adapter", "lora_path": "/path/to/adapter/v2", "load_inplace": true}'
```

Plugin alternative: LoRAResolver plugins load adapters on demand when a request names a model not yet loaded; the first adapter found wins when several resolvers exist. Built-in resolvers (all need `VLLM_ALLOW_RUNTIME_LORA_UPDATING`):
- `lora_filesystem_resolver`: add it to `VLLM_PLUGINS` and set `VLLM_LORA_RESOLVER_CACHE_DIR`; a request for adapter `foobar` looks for a directory `foobar` there.
- `lora_hf_hub_resolver`: add it to `VLLM_PLUGINS` and set `VLLM_LORA_RESOLVER_HF_REPO_LIST` to comma-separated repo IDs. The page says enabling remote downloads is insecure and not for production.
Custom resolvers implement `LoRAResolver.resolve_lora` and register through `LoRAResolverRegistry.register_resolver`.

For mixed MoE formats the load request also carries `is_3d_lora_weight`, and the server needs `--enable-mixed-moe-lora-format`; vLLM trusts the layout the caller declares, so you must know your adapter's layout.

## Checked

Method: 2026-11-08 read the vLLM LoRA Adapters page (docs source markdown) in full, focusing on the dynamic-serving sections.
Changes: added the LoRAResolver plugin route with its env vars and the production caveat, and noted that "name or ID" for unload is the page's wording. Endpoint, env var and load_inplace claims were unchanged and match the page.
