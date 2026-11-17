---
id: computing-software.ai-ml-engineering.ollama.cloud-usage-and-balance
name: cloud-usage-and-balance
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [cloud-usage, balance, group-by-model, rate-limit, apiusage]
level: practitioner
status: docs-checked
description: "Query cloud spend with GET /api/usage (range and group_by=model) and credits with GET /api/balance."
sources:
  - https://docs.ollama.com/api/cloud-usage.md
  - https://docs.ollama.com/api/balance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: monitor cloud consumption from scripts.

Both endpoints need `Authorization: Bearer $OLLAMA_API_KEY`.

Usage:

```
curl 'https://ollama.com/api/usage?range=24h' -H "Authorization: Bearer $OLLAMA_API_KEY"
```

`range` is `24h` (hourly buckets, starting 24 hours before the start of the current UTC hour), `7d` or `30d` (daily buckets from 00:00 UTC). The response has `range`, `scope`, `granularity`, `from`, `until`, `totals` and `buckets`. Totals and buckets carry `request_count`, `usage_usd`, `input_tokens`, `cached_input_tokens` and `output_tokens`. The last bucket has `partial: true`. Timestamps are UTC, `from` inclusive and `until` exclusive. Add `group_by=model` to get `groups` per model. Unsupported or repeated query parameters return 400, and new usage may take time to appear.

Balance:

```
curl https://ollama.com/api/balance -H "Authorization: Bearer $OLLAMA_API_KEY"
```

returns `included` (`balance_usd`, `allowance_usd`, and a `period` with `from` and `until`) and `purchased` (`balance_usd`, unexpired credits only). Legacy plans return `session` and `weekly` with `remaining_percent` and `resets_at`. No query parameters. The limit is 10 requests per minute per user; the docs recommend polling once per minute, and a 429 carries `Retry-After`. Team members share balances.

## Checked

2026-11-03. Ranges, bucket sizes, response fields, `partial`, `group_by=model`, 400 on bad parameters, balance fields, 10 requests per minute and `Retry-After` confirmed against the cloud usage and balance API pages. Nothing removed.

Method: documentation only; no commands were run.
