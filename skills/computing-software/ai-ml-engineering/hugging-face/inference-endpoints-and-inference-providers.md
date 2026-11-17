---
id: computing-software.ai-ml-engineering.hugging-face.inference-endpoints-and-inference-providers
name: inference-endpoints-and-inference-providers
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, inference-endpoints, inference-providers, inferenceclient, serverless-inference, model-serving, autoscaling]
level: practitioner
status: docs-checked
description: "Serve Hub models on dedicated Inference Endpoints or call Inference Providers via InferenceClient or the OpenAI-compatible route."
sources:
  - https://huggingface.co/docs/inference-endpoints/index
  - https://huggingface.co/docs/inference-providers/index
  - https://huggingface.co/docs/huggingface_hub/guides/inference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inference Endpoints and Inference Providers

## Inference Providers (pay per request, no infrastructure)
A router to partner inference providers (for example Cerebras, Fal, Fireworks, Groq, Replicate, Together) for popular models.
```python
import os
from huggingface_hub import InferenceClient
client = InferenceClient(provider="auto", api_key=os.environ["HF_TOKEN"])
r = client.chat_completion(model="meta-llama/Llama-3.1-8B-Instruct",
                           messages=[{"role": "user", "content": "Hi"}], max_tokens=100)
img = client.text_to_image("a lighthouse at dusk", model="black-forest-labs/FLUX.1-dev")
```
- OpenAI-compatible route: `base_url="https://router.huggingface.co/v1"` with the OpenAI SDK and your HF token as the key.
- With automatic provider selection the fastest provider is used by default (`:fastest`). Append a policy suffix to the model id: `:cheapest` or `:preferred` (your order in Inference Provider settings), for example `openai/gpt-oss-120b:cheapest`.
- `provider="auto"` also fails over to another provider when the primary is flagged unavailable.
- Billing is pay-as-you-go with no markup from Hugging Face. PRO users and Team or Enterprise organizations get monthly included credits; free users buy credits. You can instead bring your own provider key, in which case Hugging Face does not charge for the call. See the pricing page for amounts.

## Inference Endpoints (dedicated)
Deploy a Hub repo, including private fine-tunes, on dedicated hardware in a chosen cloud and region.
```python
from huggingface_hub import create_inference_endpoint
ep = create_inference_endpoint("my-llm", repository="org/my-finetune", framework="pytorch", task="text-generation",
        accelerator="gpu", vendor="aws", region="us-east-1", type="authenticated",
        instance_size="x1", instance_type="nvidia-l4", min_replica=0, max_replica=2,
        scale_to_zero_timeout=60)
ep.wait(); print(ep.url)
client = ep.client   # an InferenceClient bound to the endpoint URL
ep.pause(); ep.resume(); ep.scale_to_zero()
```
- `accelerator`, `instance_size`, `instance_type`, `region` and `vendor` depend on each other; list valid combinations with `list_inference_endpoints_hardware`.
- `type` is `authenticated` (default), `public` or `private`. `scale_to_zero_timeout` is in minutes; `min_replica` defaults to 1 and 0 enables scale to zero.
- Pin `revision` to deploy a specific model revision.
- `custom_image` selects an engine image keyed by variant (`vLLM`, `sGLang`, `tgi`, `tei`, `llamacpp`) or describes a custom container (`{"url": ..., "port": ...}`).
- Without a managed engine, the Inference Toolkit uses a `handler.py` with an `EndpointHandler` class in the model repository; the docs say it is not as production-ready as TGI, vLLM, SGLang or llama.cpp.
- Scale to zero: idle after 1 hour by default; the first request after zero meets a cold start and the proxy returns `503` while the replica starts. Send an `X-Scale-Up-Timeout` header (seconds) to make the proxy hold the request. Scaling up can take a few minutes, so avoid scale to zero for latency-sensitive apps.
- Autoscaling strategies: hardware utilization (default threshold 80%), pending requests (default 1.5 per replica over 20 seconds), and inference load for vLLM or SGLang (beta).
- AWS PrivateLink makes an endpoint reachable only through a private connection. Prices are shown per hour but billed per minute.

## Verify
Load test with realistic prompts before production; check endpoint logs and the Analytics tab for queueing.

## Checked
2026-11-09. Confirmed against the Inference Endpoints docs source (hf-endpoints-documentation: autoscaling, security, pricing, private link, toolkit engine pages), the Inference Providers docs source (hub-docs: index and pricing pages) and the huggingface_hub source (`HfApi.create_inference_endpoint` signature and docstring, `InferenceEndpointType`, `pause`, `resume`, `scale_to_zero`, `wait`, `client`). Corrected: `type="protected"` does not exist; the values are `public`, `authenticated` (default) and `private`. Removed as unsupported: `health_route` inside `custom_image` (it is a read-only attribute of the endpoint), the `model:provider` suffix claim (the docs show policy suffixes), the Azure PrivateLink claim and the SDK-free `max_new_tokens` call on `ep.client`, "no custom weights, no SLA control", the self-host cost row of the choosing table, and the PRO credit amount.
Method: documentation only; no commands were run.
