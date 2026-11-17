---
id: computing-software.ai-ml-engineering.hugging-face.extractive-question-answering-preprocessing
name: extractive-question-answering-preprocessing
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, question-answering, squad, offset-mapping, doc-stride]
level: practitioner
status: verified
description: "Preprocess and post-process extractive QA in transformers: overflowing tokens with stride, offset mapping to answer spans, unanswerable questions and n-best decoding."
sources:
  - https://huggingface.co/learn/llm-course/chapter7/7
  - https://huggingface.co/docs/transformers/tasks/question_answering
  - https://rajpurkar.github.io/SQuAD-explorer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extractive question answering preprocessing

The model predicts start and end token logits over `question [SEP] context`. Hard parts: long contexts, mapping character answers to tokens, and back again.

## Training features
```python
max_len, stride = 384, 128
def prep_train(ex):
    enc = tok(ex["question"], ex["context"], truncation="only_second", max_length=max_len, stride=stride,
              return_overflowing_tokens=True, return_offsets_mapping=True, padding="max_length")
    sample_map = enc.pop("overflow_to_sample_mapping"); offsets = enc.pop("offset_mapping")
    starts, ends = [], []
    for i, off in enumerate(offsets):
        ans = ex["answers"][sample_map[i]]
        s_char = ans["answer_start"][0]; e_char = s_char + len(ans["text"][0])
        seq = enc.sequence_ids(i)
        c0 = seq.index(1); c1 = len(seq) - 1 - seq[::-1].index(1)       # context token range
        if off[c0][0] > s_char or off[c1][1] < e_char:
            starts.append(0); ends.append(0)                             # answer not in this window -> CLS
        else:
            idx = c0
            while idx <= c1 and off[idx][0] <= s_char: idx += 1
            starts.append(idx - 1)
            idx = c1
            while idx >= c0 and off[idx][1] >= e_char: idx -= 1
            ends.append(idx + 1)
    enc["start_positions"], enc["end_positions"] = starts, ends
    return enc
train = raw["train"].map(prep_train, batched=True, remove_columns=raw["train"].column_names)
```
- `truncation="only_second"` truncates the context, never the question.
- `stride` creates overlapping windows so answers near a boundary appear whole in some window.
- One example becomes several features: `remove_columns` is required because row counts change.
- Requires a fast tokenizer (offset mapping).
- Checked: the `prep_train` function above, run on one example (about 4,600 characters of context, `max_len=384, stride=128`, bert-base-cased), gave 4 windows with `start_positions=[0, 368, 122, 0]` and `end_positions=[0, 370, 124, 0]`; windows 1 and 2 decode to `'forty - two'` (decode inserts spaces around the hyphen) and the windows without the answer point at CLS (0). The snippet reads `ex["answers"][sample_map[i]]`, which works for the batched `map` call but was run here on a single example with `ex["answers"]` directly.

## Evaluation post-processing
For validation keep `example_id` and offsets (set question-token offsets to None). For each example, across all its windows, take the top-n start and end logits, keep pairs with `start <= end`, length <= max_answer_len (~30), both inside the context; score = start_logit + end_logit; map back with offsets to `context[off[s][0]:off[e][1]]`.

## Unanswerable questions (SQuAD v2)
Null score = CLS start + end logits. Predict "no answer" if null score > best span score + threshold; tune the threshold on validation for best F1.

## Metrics
`evaluate.load("squad")` / `"squad_v2"`: exact match and token F1 after normalisation (lowercase, strip punctuation and articles). Checked: prediction `The Forty-two.` against reference `forty-two` scored `exact_match` 100 and `f1` 100; `squad_v2` also returns `HasAns_*`, `best_exact`, `best_f1` and their thresholds. Note that `evaluate.load` downloads a metric script from the Hub.

## Gotchas
- Models with `token_type_ids` (BERT) vs without (RoBERTa): tokenizer handles it; don't hardcode.
- Padding side right; `max_len` <= model max positions.
- Answers with leading spaces or Unicode: check `context[answer_start:answer_start+len(text)] == text` before training.

## Verify
On a few training features, decode `tok.decode(input_ids[start:end+1])` and compare with the gold answer text.
