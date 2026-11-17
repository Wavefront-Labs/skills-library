---
id: computing-software.ai-ml-engineering.hugging-face.long-inputs-stride-and-overflowing-tokens
name: long-inputs-stride-and-overflowing-tokens
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, return-overflowing-tokens, stride, truncation, long-documents, offset-mapping, tokenizers]
level: practitioner
status: verified
description: "Handle texts longer than max_length: truncation strategies, return_overflowing_tokens with stride windows, overflow_to_sample_mapping and aggregating window predictions."
sources:
  - https://huggingface.co/learn/llm-course/chapter6/3b
  - https://huggingface.co/docs/transformers/main/en/pad_truncation
  - https://huggingface.co/docs/transformers/main/en/tasks/question_answering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Long inputs with stride and overflowing tokens

**Problem:** encoders have a max length (often 512); naive truncation drops the rest of the document, losing answers, entities or evidence.

## Sliding windows
```python
enc = tokenizer(texts, truncation=True, max_length=384, stride=128,
                return_overflowing_tokens=True, return_offsets_mapping=True, padding="max_length")
sample_map = enc.pop("overflow_to_sample_mapping")    # window i -> original example index
```
- `stride` is the number of overlapping tokens between consecutive windows, so content near a boundary appears whole in at least one window. Checked with bert-base-cased on 600 repeated words, `max_length=384, stride=128`: 2 windows with 382 and 346 word tokens (384 minus [CLS]/[SEP]); the second starts 128 tokens before the first ended, and `overflow_to_sample_mapping` is `[0, 0]`.
- Requires a fast tokenizer.
- With pairs (question, context) use `truncation="only_second"` so only the context is windowed.

## In datasets.map
Windowing changes the number of rows; return only new columns and drop the originals:
```python
def prep(batch):
    enc = tokenizer(batch["text"], truncation=True, max_length=512, stride=64, return_overflowing_tokens=True)
    enc["label"] = [batch["label"][i] for i in enc["overflow_to_sample_mapping"]]
    return enc
ds = ds.map(prep, batched=True, remove_columns=ds.column_names)
```

## Aggregating predictions
| Task | Aggregation |
|---|---|
| Document classification | mean or max of window logits per document (`sample_map` groupby) |
| Extractive QA | best span across windows using offsets; ignore spans outside the context |
| Token classification / NER | for overlapping tokens keep the prediction from the window where the token is farthest from an edge |

## Alternatives
Long-context models (ModernBERT 8k, Longformer, LLMs with 128k+ context), hierarchical models (encode chunks, then pool), or retrieval of relevant chunks first.

## Verify
- [ ] Count windows per document; check the last window covers the document end (decode it).
- [ ] Compare document-level metric vs head-only truncation.
