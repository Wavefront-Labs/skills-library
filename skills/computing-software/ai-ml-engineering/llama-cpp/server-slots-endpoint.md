---
id: computing-software.ai-ml-engineering.llama-cpp.server-slots-endpoint
name: server-slots-endpoint
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, slots, monitoring, parallel-requests]
level: practitioner
status: docs-checked
description: "Inspect per-slot state with GET /slots, disable it with --no-slots and use fail_on_no_slot."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GET /slots

Enabled by default; disable with `--no-slots`. The README documents an HTTP 501 error of type `not_supported_error` for a disabled `/metrics` or `/slots` endpoint (its example message is "This server does not support metrics endpoint.").

It returns an array with one object per slot (the count comes from `-np`/`--parallel`). Each entry shows:

- `id` and `id_task`: slot index and the task it is processing.
- `n_ctx`: context size of the slot.
- `is_processing`: whether the slot is busy.
- `speculative`: whether speculative decoding is on.
- `params`: the sampling parameters in effect (`n_predict`, `seed`, `temperature`, `top_k`, `top_p`, `min_p`, `dry_*`, `mirostat*`, `n_keep`, `ignore_eos`, and so on).

Query parameter `?fail_on_no_slot=1` makes the endpoint answer HTTP 503 when there is no available slot.

To pin a request to a given slot use `id_slot` in `/completion`. A value of `-1` assigns the task to an idle slot.

Slot cache persistence is separate: see the `POST /slots/{id_slot}?action=` routes and `--slot-save-path`.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: GET /slots default and --no-slots, fail_on_no_slot, the response fields, id_slot in /completion, the slot save, restore and erase routes, --slot-save-path and the 501 error type. Removed: the load-balancer readiness-probe remark and the exact 501 wording for slots.

Method: docs-only read of cited pages, 2026-11-08
