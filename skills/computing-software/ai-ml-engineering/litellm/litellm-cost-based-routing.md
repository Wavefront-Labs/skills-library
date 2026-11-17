---
id: computing-software.ai-ml-engineering.litellm.litellm-cost-based-routing
name: litellm-cost-based-routing
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, cost-based-routing, input-cost-per-token, custom-pricing]
level: advanced
status: docs-checked
description: "Pick the cheapest healthy deployment with cost-based-routing, including custom per-token costs."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: route each request to the cheapest healthy deployment in a model group with routing_strategy cost-based-routing.
Set `routing_strategy="cost-based-routing"` (SDK) or `routing_strategy: cost-based-routing` in router_settings.

How it works:

1. Get all healthy deployments.
2. Keep those under their provided rpm/tpm limits.
3. For each, check whether `litellm_params["model"]` exists in `litellm_model_cost_map`.
4. If a deployment is not in the cost map, its cost is treated as $1.
5. Select the deployment with the lowest cost.

Example: a group `gpt-6-luna` with deployments `gpt-6.1-sol` and `groq/llama3-8b-8192`; the Groq deployment (id `groq-llama`) wins because it costs less. The picked id shows in `response._hidden_params["model_id"]`.

Custom pricing for routing: set `input_cost_per_token` and `output_cost_per_token` in litellm_params:

```
model_list = [
  {"model_name": "gpt-6-luna",
   "litellm_params": {"model": "azure/chatgpt-v-2",
     "input_cost_per_token": 0.00003, "output_cost_per_token": 0.00003},
   "model_info": {"id": "chatgpt-v-experimental"}},
  {"model_name": "gpt-6-luna",
   "litellm_params": {"model": "azure/chatgpt-v-1",
     "input_cost_per_token": 0.000000001, "output_cost_per_token": 0.00000001},
   "model_info": {"id": "chatgpt-v-1"}},
]
router = Router(model_list=model_list, routing_strategy="cost-based-routing")
```

The router picks `chatgpt-v-1`, the lowest cost.

Give each deployment a `model_info.id` to identify which one was picked.
Set `routing_strategy: cost-based-routing` in the router settings (or the Router constructor) to enable it.

## Checked

Method: docs-checked 2026-11-09 against the LiteLLM Router Load Balancing (docs/routing) page, Lowest Cost Routing section including custom pricing.
