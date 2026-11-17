---
id: computing-software.ai-ml-engineering.kserve.kserve-huggingface-runtime
name: kserve-huggingface-runtime
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [huggingface, model-id, model-name, model-dir, task, backend, vllm, max-model-len, trust-remote-code, return-probabilities, return-raw-logits, safetensors-fast-gpu, hf-hub-disable-telemetry, fill-mask, token-classification, sequence-classification]
level: practitioner
status: docs-checked
description: "Hugging Face serving runtime: supported tasks, V1/V2/OpenAI endpoints, default env vars, and command-line args (--model_id, --task, --backend, --dtype, --max_model_len)."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/huggingface/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hugging Face serving runtime

Serves `transformers` models from the Hub or your own storage with `modelFormat: {name: huggingface}`. Predictive tasks (text classification, token classification, fill-mask) are exposed through the Open Inference Protocol or the V1 API; generative tasks also support OpenAI-compatible endpoints.

Image env defaults: `SAFETENSORS_FAST_GPU` enabled (faster loading), `HF_HUB_DISABLE_TELEMETRY` enabled.

## Arguments (container args)
vLLM engine args are also accepted and parsed by the runtime.
- `--model_name` name used on the endpoint path
- `--model_dir` local download path (ignored if `--model_id` is set)
- `--model_id`, `--model_revision`, `--tokenizer_revision`
- `--dtype` one of `auto`, `float16`, `float32`, `bfloat16`, `float`, `half`; default float16 on GPU, float32 on CPU; encoder models default float32
- `--task` one of `text_generation`, `text2text_generation`, `fill_mask`, `token_classification`, `sequence_classification` (inferred from architecture if omitted)
- `--backend` `auto`, `huggingface` or `vllm`
- `--max_model_len` max tokens; defaults to the model max position encodings
- `--disable_lower_case`, `--disable_special_tokens`, `--trust_remote_code`
- `--tensor_input_names` (Triton backend), `--return_token_type_ids`
- `--return_probabilities` and `--return_raw_logits`: classification tasks only
- `--disable_log_requests`

The overview page shows no manifest: use the task examples it links (token classification with BERT, sequence classification with distilBERT, fill-mask with BERT) for a working InferenceService.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website Hugging Face overview page: supported tasks, API endpoints, environment defaults, and every runtime argument with its defaults. Removed the sample manifest (`modelFormat: huggingface`, `hf://` storageUri), which the overview does not show. Also fixed `--model_name` wording to match the page.
