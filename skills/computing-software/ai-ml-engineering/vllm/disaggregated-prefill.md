---
id: computing-software.ai-ml-engineering.vllm.disaggregated-prefill
name: disaggregated-prefill
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [disaggregated-prefill, kv-transfer-config, kv-connector, nixl-connector, kv-role]
level: advanced
status: docs-checked
description: "Split prefill and decode into separate vLLM instances with a KV connector and --kv-transfer-config."
sources:
  - https://docs.vllm.ai/en/latest/features/disagg_prefill/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run prefill and decode in different vLLM instances (experimental, subject to change).

Why use it:
- Tune time-to-first-token (TTFT) and inter-token latency (ITL) separately, since each instance can have its own parallel strategy (tp, pp).
- Control tail ITL. Without it, prefill jobs can be inserted during decode of another request. Chunked prefill with a proper chunk size can achieve the same goal, but the right size is hard to find in practice.
- It does not improve throughput.

Configure with `--kv-transfer-config`, a JSON object naming `kv_connector` and `kv_role` (for example `kv_both`). The page says it supports 9 connector types and its list names eight: ExampleConnector, LMCacheConnectorV1 (also an `LMCacheMPConnector` multi-process mode), NixlConnector (fully async send/recv; several transfer backends can be listed), MooncakeConnector, MoRIIOConnector (ROCm only), MultiConnector, OffloadingConnector (CPU offload, `block_size` in tokens and `cpu_bytes_to_use`) and FlexKVConnectorV1.

```bash
--kv-transfer-config '{"kv_connector":"NixlConnector","kv_role":"kv_both","kv_buffer_device":"cuda","kv_connector_extra_config":{"backends":["UCX","GDS"]}}'
```

MultiConnector stacks connectors in an ordered `connectors` list inside `kv_connector_extra_config`.

Reusing prefill token ids on `/v1/chat/completions`: send the prefill request with `return_token_ids` enabled, read `prompt_token_ids` from the response, then set `kv_transfer_params["prompt_token_ids"]` on the decode request. `messages` is still required but not tokenized when the ids are present, so decode skips its own templating and tokenization. The prefill request carries `kv_transfer_params: {"do_remote_decode": true}` and the decode request `{"do_remote_prefill": true, "prompt_token_ids": ids}`. The ids are ignored (and `messages` rendered) if `messages` has non-text content or `echo` is set; otherwise they must be a non-empty list of non-negative integers or the request fails with HTTP 400.

Generate API (`/inference/v1/generate`): set `output_mode` on the decode request only; a proxy must reset it to `tokens` on the prefill request. A prefill instance started with `--tokens-only` rejects `output_mode: "text"` with a 400. A decode instance returning text needs a tokenizer, so start it with `--enable-scale-out` and without `--tokens-only`.

Internals: two vLLM instances (prefill and decode) joined by a connector, code under `vllm/distributed/kv_transfer`. Abstractions are Connector, LookupBuffer (`insert`, blocking `drop_select`) and Pipe (`send_tensor`, `recv_tensor`); each process has a connector (scheduler connector schedules transfers, worker connectors execute them). The page relies on third-party connectors for production use.

## Checked

Method: 2026-11-08 read the disaggregated prefill page in full. Rationale, kv-transfer-config and token-id reuse matched. Corrected the connector count (page says 9, lists 8) and added the OffloadingConnector, Generate API output_mode and internals notes.
