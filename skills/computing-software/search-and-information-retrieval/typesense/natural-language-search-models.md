---
id: computing-software.search-and-information-retrieval.typesense.natural-language-search-models
name: natural-language-search-models
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [nl-search, nl-search-models, llm-query-parsing, typesense]
level: advanced
status: docs-checked
description: "Create Typesense natural language search models via POST /nl_search_models for OpenAI, Azure, Cloudflare, vLLM, Gemini or Vertex AI."
sources: ["https://typesense.org/docs/30.2/api/natural-language-search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Natural language search models

An LLM turns text like "A honda or BMW with at least 200hp, rear-wheel drive, from 20K to 50K" into structured `filter_by`, `sort_by` and query parameters, even when the words are not in the data.

## Create

`POST /nl_search_models` with `id` (any string, referenced later as `nl_model_id`), `model_name`, `api_key`, `max_bytes` (example 16000), `temperature` (example 0.0) and an optional `system_prompt` appended to the prompt Typesense generates from your dataset.

Providers:

- OpenAI: `openai/gpt-4.1`.
- Azure: `azure/gpt-35-turbo` plus `url`.
- Cloudflare: `cloudflare/@cf/meta/llama-2-7b-chat-int8` plus `account_id`.
- vLLM: `vllm/mistral-7b-instruct` with `api_url`.
- Google Gemini: `google/gemini-2.5-flash`; optional `top_p`, `top_k`, `stop_sequences`, `api_version` (default v1beta).
- GCP Vertex AI: `gcp/gemini-2.5-flash` with `project_id` and either OAuth values (`access_token`, `refresh_token`, `client_id`, `client_secret`) or `service_account` (`client_email`, `private_key`, optional `token_uri`); optional `region` (default us-central1), `temperature` (0.0 to 2.0), `top_p`, `top_k`, `max_output_tokens`.

## Manage

`GET /nl_search_models`, `GET /nl_search_models/{model_id}`, `PUT` with changed fields such as `temperature` and `system_prompt`, `DELETE`. Renaming the `id` to an existing one gives `409`.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Natural Language Search (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
