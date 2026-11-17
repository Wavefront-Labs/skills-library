---
id: computing-software.ai-ml-engineering.litellm.litellm-key-custom-header
name: litellm-key-custom-header
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, litellm-key-header-name, authorization-header, api-gateway]
level: practitioner
status: docs-checked
description: "Read the LiteLLM virtual key from a custom header with litellm_key_header_name, for example behind an API gateway."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read the LiteLLM virtual key from a header other than Authorization.
Goal: make the proxy look for the virtual key in a header other than `Authorization`, such as when another gateway in front of it uses `Authorization` for its own token.

Config:

```
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  litellm_key_header_name: "X-Litellm-Key"
```

Request (LiteLLM uses the key from X-Litellm-Key; the bad Authorization value is ignored):

```
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Litellm-Key: Bearer $LITELLM_API_KEY" \
  -H "Authorization: Bearer bad-key" \
  -d '{
    "model": "fake-openai-endpoint",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

The expected result is a successful response, since the key in X-Litellm-Key is valid.

With the OpenAI Python SDK, set both headers through default_headers:

```
client = openai.OpenAI(
    api_key="not-used",
    base_url="https://api-gateway-url.com/llmservc/api/litellm",
    default_headers={
        "Authorization": f"Bearer {API_GATEWAY_TOKEN}",   # optional, for your API gateway
        "X-Litellm-Key": f"Bearer sk-<your-litellm-api-key>"
    }
)
```

The header value keeps the `Bearer` prefix, as in the examples. The header name is set in `litellm_key_header_name` under `general_settings`.

## Checked

Method: docs-checked 2026-11-09 against the LiteLLM Virtual Keys (proxy/virtual_keys) page, Pass LiteLLM Key in custom header section.
