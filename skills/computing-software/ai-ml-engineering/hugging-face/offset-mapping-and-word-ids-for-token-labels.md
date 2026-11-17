---
id: computing-software.ai-ml-engineering.hugging-face.offset-mapping-and-word-ids-for-token-labels
name: offset-mapping-and-word-ids-for-token-labels
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, tokenizers, offset-mapping, word-ids, token-classification, label-alignment, is-split-into-words, ner]
level: practitioner
status: verified
description: "Align labels with subword tokens using fast tokenizer word_ids and offset_mapping: -100 masking, first-subword labeling, character spans for NER and QA."
sources:
  - https://huggingface.co/learn/llm-course/chapter6/3
  - https://huggingface.co/learn/llm-course/chapter7/2
  - https://huggingface.co/docs/transformers/tasks/token_classification
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offset mapping and word_ids for token-level labels

**Goal:** map word- or character-level annotations onto subword tokens, and predictions back onto the original text.

## word_ids for pre-split words
```python
tok = AutoTokenizer.from_pretrained("bert-base-cased")   # must be a fast tokenizer
enc = tok(["EU", "rejects", "German", "call"], is_split_into_words=True)
enc.word_ids()   # [None, 0, 1, 2, 3, None] with bert-base-cased: every word here is one token. None = special tokens; a rare word such as "Sylvain" gives repeated ids, one per subword
```
Label alignment (the standard recipe):
```python
def align(labels, word_ids, label_all_subwords=False):
    out, prev = [], None
    for w in word_ids:
        if w is None:
            out.append(-100)                       # ignored by CrossEntropyLoss
        elif w != prev:
            out.append(labels[w])                  # first subword gets the word's label
        else:
            out.append(labels[w] if label_all_subwords else -100)
        prev = w
    return out
```
If you label all subwords with BIO tags, convert `B-X` to `I-X` for continuation subwords.

## offset_mapping for character spans
```python
enc = tok(text, return_offsets_mapping=True)
for (start, end), tid in zip(enc["offset_mapping"], enc["input_ids"]):
    print(tid, text[start:end])     # special tokens get (0, 0)
```
- Convert character-level entity annotations to token labels: a token belongs to an entity if its span overlaps the entity span.
- Map predictions back: group consecutive tokens with the same entity, take `text[first_start:last_end]` - this keeps original spacing and casing.
- `enc.char_to_token(i)` and `enc.token_to_chars(t)` do single lookups.

## Question answering
For extractive QA, `sequence_ids()` tells which tokens are question (0) vs context (1); offsets locate the answer's start/end tokens; long contexts use `stride` + `return_overflowing_tokens=True` and you must find the answer in each window.

## Gotchas
- Slow (Python) tokenizers don't support `word_ids`/offsets; `AutoTokenizer` returns fast by default when available (`tok.is_fast`).
- Byte-level BPE tokenizers (RoBERTa, GPT-2) with `is_split_into_words=True` should be loaded with `add_prefix_space=True` (`AutoTokenizer.from_pretrained("roberta-base", add_prefix_space=True)`). Checked on transformers 5.20: without it the call does not raise but words are tokenized without the leading-space marker, so ids differ from running text; with it you get `['<s>', 'ĠEU', 'Ġrejects', '</s>']`.
- Truncation drops tokens at the end; entities beyond `max_length` vanish silently. Use striding for long documents.

## Verify
- [ ] Decoding aligned labels back to words reproduces the original word labels.
- [ ] Predicted spans extracted via offsets match the original text exactly.
- [ ] Count of entities lost to truncation is known.
