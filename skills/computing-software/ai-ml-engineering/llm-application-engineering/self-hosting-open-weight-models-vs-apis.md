---
id: computing-software.ai-ml-engineering.llm-application-engineering.self-hosting-open-weight-models-vs-apis
name: self-hosting-open-weight-models-vs-apis
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, open-weight-models, self-hosting, model-selection, total-cost-of-ownership, licensing]
level: practitioner
status: draft
description: "Decide between hosted model APIs and self-hosted open-weight models: capability gaps, data control, cost break-even maths, licences, latency and the operational burden."
sources:
  - https://docs.vllm.ai/en/latest/
  - https://www.llama.com/llama3_1/license/
  - https://huggingface.co/docs/hub/models-licenses
  - https://docs.claude.com/en/docs/about-claude/pricing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Self-hosting open-weight models vs API models

**Goal:** a defensible choice per use case, based on measured quality, full cost and real constraints - not on per-token price alone.

## Decision factors
| Factor | Favours API | Favours self-hosting |
|---|---|---|
| Task difficulty | complex reasoning, agents, long context | narrow, well-defined tasks a small model handles |
| Data control | provider DPAs, zero-retention options, regional processing suffice | data must never leave your environment |
| Volume | low or spiky | high and steady (keeps GPUs busy) |
| Latency control | standard SLOs OK | strict, co-located, or offline/edge |
| Customization | prompting, hosted fine-tuning | full fine-tuning, custom decoding, weights access |
| Team | no GPU/ML ops capacity | existing platform team |

## Cost maths
Self-hosted cost per million output tokens = (GPU hourly cost x GPUs) / (sustained tokens per second x 3600 / 1e6). Use measured throughput at your latency SLO and realistic utilisation (often 30-60%, not 100%), then add engineering time, on-call, monitoring, storage, idle capacity for peaks and upgrade work. Compare with API cost including caching and batch discounts. Many teams find APIs cheaper until volume is large and steady.

## Quality first
Run your eval set on candidate open models (at the quantization you would deploy) and on API models. A cheaper model that needs more retries, human review or produces worse outcomes is not cheaper.

## Licences
Check each model's licence: Apache-2.0/MIT models are permissive; others carry use restrictions, attribution requirements, user-count thresholds or acceptable-use policies (e.g. Llama community licence, Gemma terms). Some forbid using outputs to train competing models. Record licence and version in the AI inventory.

## Hybrid patterns
- Route easy, high-volume tasks to a self-hosted small model and hard ones to an API model (cascade with evals).
- Use an API model to generate training data and distil into a small open model (check API terms).
- Keep an OpenAI-compatible interface (vLLM/SGLang serve one) so routes can switch backends.

## Verify
- [ ] Eval results for each candidate at deployment precision.
- [ ] Full TCO estimate with utilisation assumptions documented.
- [ ] Licence reviewed and recorded.
