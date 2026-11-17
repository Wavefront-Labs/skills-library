---
id: computing-software.ai-ml-engineering.hugging-face.training-a-new-tokenizer
name: training-a-new-tokenizer
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, tokenizers, train-new-from-iterator, train-tokenizer, bpe, wordpiece, pretrainedtokenizerfast]
level: practitioner
status: verified
description: "Train a tokenizer for a new domain or language: train_new_from_iterator from an existing fast tokenizer, or build BPE/WordPiece/Unigram from scratch with the tokenizers library."
sources:
  - https://huggingface.co/learn/llm-course/chapter6/2
  - https://huggingface.co/learn/llm-course/chapter6/8
  - https://huggingface.co/docs/tokenizers/quicktour
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Training a new tokenizer

**Goal:** a tokenizer whose vocabulary fits your corpus (code, a new language, chemistry strings), so sequences are shorter and tokens meaningful.

## When to do it
Only when you will **pretrain** (or continue pretraining with a new embedding matrix). A new tokenizer makes the pretrained model's embeddings meaningless; for fine-tuning an existing model, keep its tokenizer (optionally add a few special tokens).

Check need first: average tokens per word/character on your corpus with the existing tokenizer. If it splits domain words into many pieces, training a new one may pay off.

## Same algorithm as an existing tokenizer
```python
from datasets import load_dataset
from transformers import AutoTokenizer
ds = load_dataset("code-search-net/code_search_net", "python", split="train")   # the bare id "code_search_net" fails on datasets 5.1 (HfUriError); use the namespaced repo
def batches(bs=1000):
    for i in range(0, len(ds), bs):
        yield ds[i:i + bs]["whole_func_string"]
old = AutoTokenizer.from_pretrained("gpt2")
tok = old.train_new_from_iterator(batches(), vocab_size=52000)
tok.save_pretrained("code-tokenizer")      # or tok.push_to_hub(...)
```
Keeps the old tokenizer's normaliser, pre-tokeniser, model type and special tokens. Requires a **fast** tokenizer. Checked on 2,000 streamed functions with `vocab_size=5000`: result is a `GPT2Tokenizer` of length 5000, `eos_token` still `<|endoftext|>`, one sample went from 463 tokens (original gpt2) to 282, and `decode(encode(text)) == text` held. Use a generator so the corpus never has to fit in memory.

## From scratch with the tokenizers library
```python
from tokenizers import Tokenizer, models, normalizers, pre_tokenizers, decoders, trainers, processors
tk = Tokenizer(models.BPE())
tk.normalizer = normalizers.NFC()
tk.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
trainer = trainers.BpeTrainer(vocab_size=32000, min_frequency=2, special_tokens=["<|endoftext|>", "<pad>"])
tk.train_from_iterator(batches(), trainer=trainer)
tk.post_processor = processors.ByteLevel(trim_offsets=False)
tk.decoder = decoders.ByteLevel()
from transformers import PreTrainedTokenizerFast
hf_tok = PreTrainedTokenizerFast(tokenizer_object=tk, eos_token="<|endoftext|>", pad_token="<pad>")
```
Algorithm choice: byte-level BPE (GPT family; never produces unknown tokens: checked, `héllo wörld 你好` encodes with `unk_token` None), WordPiece (BERT), Unigram (used by T5/SentencePiece; check the tokenizers docs for when it fits your language).

## Gotchas
- Vocab size trade-off: bigger vocab = shorter sequences but larger embedding/output layers. Reference points read from the loaded tokenizers: gpt2 has 50,257 tokens and bert-base-cased 28,996. A trainer asked for 32,000 on a small corpus stops at whatever the corpus supports (15,394 in the 2,000-function test).
- Normalisation (lowercasing, accent stripping) can't be undone at decode; avoid it for code and case-sensitive domains.
- Ensure special tokens (BOS/EOS/PAD) are defined and their IDs match the model config.

## Verify
- [ ] Tokens-per-word on held-out domain text dropped vs the original tokenizer.
- [ ] `decode(encode(text)) == text` on a sample (round-trip).
- [ ] Special token IDs match the model config.
