---
id: computing-software.ai-ml-engineering.hugging-face.data-collators
name: data-collators
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, data-collator, datacollatorwithpadding, datacollatorforlanguagemodeling, datacollatorforseq2seq, dynamic-padding]
level: practitioner
status: verified
description: "Choose Transformers data collators: dynamic padding, MLM masking, causal LM labels, seq2seq label padding with -100, token classification, flattening, and writing a custom one."
sources:
  - https://huggingface.co/docs/transformers/main/en/main_classes/data_collator
  - https://huggingface.co/learn/llm-course/chapter3/2
  - https://huggingface.co/docs/transformers/main/en/tasks/language_modeling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data collators

**Job:** turn a list of tokenized examples into a padded batch with correct labels. Dynamic padding (pad to the longest in the batch) does less work than padding everything to max_length.

## Pick the right one
| Task | Collator | Key behaviour |
|---|---|---|
| Classification | `DataCollatorWithPadding(tokenizer, pad_to_multiple_of=8)` | pads inputs and attention mask |
| Masked LM | `DataCollatorForLanguageModeling(tokenizer, mlm_probability=0.15)` | masks 15% (80/10/10 rule), labels -100 elsewhere |
| Causal LM | `DataCollatorForLanguageModeling(tokenizer, mlm=False)` | labels = input_ids, pads set to -100 (model shifts internally) |
| Seq2seq | `DataCollatorForSeq2Seq(tokenizer, model=model, label_pad_token_id=-100)` | pads labels with -100; creates `decoder_input_ids` when model given |
| Token classification | `DataCollatorForTokenClassification(tokenizer)` | pads label sequences with -100 |
| Padding-free packing | `DataCollatorWithFlattening()` | concatenates the batch into one `[1, total_tokens]` sequence, emits `position_ids`, and sets the first label of each sequence to -100; meant for padding-free attention such as FlashAttention-2 (checked on CPU: `[[1,2,3],[4,5]]` gives labels `[-100,2,3,-100,5]`, position_ids `[0,1,2,0,1]`) |

`pad_to_multiple_of=8` (or 64) is the usual setting for fp16/bf16 tensor-core efficiency (a common recommendation; not benchmarked here).

## Labels and -100
Loss functions ignore index -100. Padding labels with the pad token id instead makes the model learn to predict padding.

## Causal LM gotcha
If `pad_token == eos_token` (common for Llama-style tokenizers), the LM collator also masks real EOS tokens, so the model never learns to stop. Checked with GPT-2: with `pad_token = eos_token` an appended EOS (50256) becomes -100 in `labels`; with a separate `<pad>` token it stays 50256 and only the padding is -100. Use a distinct pad token or a custom collator that masks only padding positions (via attention mask).

## Custom collator
```python
def collate(features):
    batch = tokenizer.pad([{k: f[k] for k in ("input_ids", "attention_mask")} for f in features],
                          return_tensors="pt", pad_to_multiple_of=8)
    labels = [f["labels"] for f in features]
    L = batch["input_ids"].shape[1]
    batch["labels"] = torch.tensor([l + [-100] * (L - len(l)) for l in labels])
    return batch
```
Trainer drops columns the model's `forward` does not accept (`remove_unused_columns` defaults to True; checked in transformers 5.20, and `TrainingArguments` needs `accelerate>=1.1.0`); set it False when the collator needs extra columns.

## Verify
- [ ] Decode one batch: inputs, padding and labels (replace -100 with pad for display) line up.
