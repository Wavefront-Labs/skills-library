---
id: computing-software.ai-ml-engineering.hugging-face.transformers-pipeline-batching-and-device-map
name: transformers-pipeline-batching-and-device-map
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, pipeline-batching, device-map, pipeline, inference]
level: practitioner
status: gated
description: "Use transformers pipeline() well: pick task and model, place it with device or device_map, batch over datasets with KeyDataset, and avoid the slow per-item loop."
sources:
  - https://huggingface.co/docs/transformers/main_classes/pipelines
  - https://huggingface.co/docs/transformers/pipeline_tutorial
  - https://huggingface.co/docs/accelerate/usage_guides/big_modeling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pipeline(): batching and device_map

## Create
```python
from transformers import pipeline
import torch
clf = pipeline("text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
               device=0)                                   # GPU 0; -1 or "cpu" for CPU, "mps" on Apple
gen = pipeline("text-generation", model="Qwen/Qwen2.5-7B-Instruct",
               dtype=torch.bfloat16, device_map="auto")   # spread across GPUs / offload to CPU (`torch_dtype=` warns "deprecated")
```
- Always pin a `model=` (and `revision=`) in production: the task default is hard-coded per transformers version (`SUPPORTED_TASKS["text-classification"]["default"]` is `distilbert/distilbert-base-uncased-finetuned-sst-2-english` at revision `714eb0f` on 5.20.2), so an upgrade can change it.
- `device_map="auto"` (needs `accelerate`) is for models too big for one device; don't combine with `device=` (on 5.20.2 the combination did not raise on CPU, so the conflict is silent, not an error). `device=-1` and `device="cpu"` both gave `pipeline.device == cpu`; GPU placement was not run (gated: unconfirmed, source is paywalled or blocked).

## Batch over a dataset
```python
from transformers.pipelines.pt_utils import KeyDataset
from datasets import load_dataset
ds = load_dataset("stanfordnlp/imdb", split="test[:2000]")   # bare "imdb" failed on datasets 5.1.0 (HfUriError: Invalid HF URI)
for out in clf(KeyDataset(ds, "text"), batch_size=32, truncation=True):
    ...
```
- Passing a list or Dataset lets the pipeline stream with a DataLoader; a Python loop calling `clf(text)` per item is far slower on GPU.
- `batch_size` helps on GPU with similar-length inputs; on CPU or with very uneven lengths it can be slower (padding). Measured on this CPU with SST-2 DistilBERT over 64 IMDB reviews: `batch_size=16` took 7.8 s (first call, includes warm-up) versus 4.9 s at `batch_size=1`; the per-item Python loop for 32 reviews took 2.4 s. So the "far slower loop" claim is a GPU claim and did not hold on CPU (gated: unconfirmed, source is paywalled or blocked). Start at 8-64 on GPU; reduce on OOM.
- `truncation=True` (or `max_length`) avoids crashes on long inputs.

## Useful task options
- Classification: `top_k=None` returns all labels with scores (ran: POSITIVE 0.99986, NEGATIVE 0.00014); `function_to_apply="sigmoid"` for multi-label (ran: scores 0.990 and 0.0137, no longer summing to 1).
- Token classification: `aggregation_strategy="simple"` merges sub-tokens into entities (ran with `dslim/bert-base-NER`: `Face` ORG, `New York` LOC with start/end offsets).
- Text generation: `max_new_tokens`, `do_sample`, `temperature`, `return_full_text=False` (ran: generated text excludes the prompt); chat models accept a list of message dicts and apply the chat template (ran: the output `generated_text` is the message list with a new assistant message appended).
- ASR: `chunk_length_s=30, stride_length_s=5` for long audio; `return_timestamps=True` (the three parameter names appear in `AutomaticSpeechRecognitionPipeline`'s source; no audio model was run) (gated: unconfirmed, source is paywalled or blocked).
- Zero-shot classification: `candidate_labels=[...]`, `multi_label=True` (ran with `typeform/distilbert-base-uncased-mnli`).

## When to leave pipeline
For high-throughput LLM serving, use TGI or vLLM (continuous batching, paged KV cache). For custom pre/post-processing or training, load `AutoTokenizer` + `AutoModelFor...` directly.

## Gotchas
- Generation pipelines with batching need a pad token: with a GPT-2 style tokenizer (no pad token) `batch_size=2` raised `ValueError: Pipeline with tokenizer without pad_token cannot do batching`, fixed by `gen.tokenizer.pad_token = gen.tokenizer.eos_token`; the pipeline tokenizer's `padding_side` was already `left` in the runs, but check it for decoder-only models.
- Inputs longer than the model's max positions are not truncated by default: a 1,000-word review sent to the SST-2 pipeline without `truncation=True` raised `RuntimeError: The size of tensor a (1002) must match the size of tensor b (512)`; with `truncation=True` it ran.
- First call is slow (CUDA init, weights to GPU); warm up before timing.

## Verify
Throughput test: time 1000 inputs with `batch_size` 1, 8, 32; check GPU utilisation; compare predictions with a direct model call on a few examples.
