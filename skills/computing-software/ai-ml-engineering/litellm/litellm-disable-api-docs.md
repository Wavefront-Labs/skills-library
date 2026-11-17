---
id: computing-software.ai-ml-engineering.litellm.litellm-disable-api-docs
name: litellm-disable-api-docs
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, no-docs, no-redoc, no-openapi]
level: practitioner
status: docs-checked
description: "Lock down Swagger, Redoc and the OpenAPI schema on a production or air-gapped proxy with three environment variables."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Swagger, Redoc and the raw OpenAPI schema are three independent surfaces, each disabled by its own variable:

```
NO_DOCS="True"      # Swagger UI at the base URL
NO_REDOC="True"     # Redoc, default <your-proxy-url>/redoc
NO_OPENAPI="True"   # raw schema, default <your-proxy-url>/openapi.json
```

Set all three to fully lock down a production or air-gapped deployment, then restart the proxy.

Result:

- `/redoc` and `/openapi.json` return 404 with no schema in the response.
- `/` returns only the plain "LiteLLM: RUNNING" status string.
- Inference and management routes are unaffected.

Failure mode: setting only NO_DOCS leaves Redoc and the OpenAPI schema reachable. Each variable disables only its own surface.

For a container deployment, set them next to your other environment variables, then restart the container.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/configs (Disable Swagger UI section); removed unconfirmed config.yaml Swagger page remark and docker example
