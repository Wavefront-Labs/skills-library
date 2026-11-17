---
id: computing-software.ai-ml-engineering.hugging-face.tokenizer-pipeline-normalizers-pre-tokenizers
name: tokenizer-pipeline-normalizers-pre-tokenizers
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, pre-tokenizer, normalizers, post-processor, tokenizers-library, bpe, decoders]
level: practitioner
status: verified
description: "Assemble a tokenizer from components with the tokenizers library: normalizers, pre-tokenizers, model, post-processor templates and decoder, then wrap as PreTrainedTokenizerFast."
sources:
  - https://huggingface.co/learn/llm-course/chapter6/8
  - https://huggingface.co/docs/tokenizers/components
  - https://huggingface.co/docs/tokenizers/pipeline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tokenizer pipeline: normalizers, pre-tokenizers, post-processors

**Pipeline:** normalization -> pre-tokenization -> model (BPE/WordPiece/Unigram) -> post-processing (special tokens) ; decoding reverses it.

## Build a byte-level BPE tokenizer (GPT-style)
```python
from tokenizers import Tokenizer, models, normalizers, pre_tokenizers, trainers, processors, decoders
tok = Tokenizer(models.BPE(unk_token=None))
tok.normalizer = normalizers.NFC()
tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
trainer = trainers.BpeTrainer(vocab_size=32000, min_frequency=2,
                              special_tokens=["<|endoftext|>", "<|pad|>"],
                              initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
tok.train_from_iterator(text_iterator(), trainer=trainer)
tok.post_processor = processors.ByteLevel(trim_offsets=False)
tok.decoder = decoders.ByteLevel()
```

## WordPiece (BERT-style)
```python
tok = Tokenizer(models.WordPiece(unk_token="[UNK]"))
tok.normalizer = normalizers.Sequence([normalizers.NFD(), normalizers.Lowercase(), normalizers.StripAccents()])
tok.pre_tokenizer = pre_tokenizers.BertPreTokenizer()
# ... train with WordPieceTrainer(special_tokens=["[UNK]","[CLS]","[SEP]","[PAD]","[MASK]"])
cls, sep = tok.token_to_id("[CLS]"), tok.token_to_id("[SEP]")
tok.post_processor = processors.TemplateProcessing(
    single="[CLS] $A [SEP]", pair="[CLS] $A [SEP] $B:1 [SEP]:1",
    special_tokens=[("[CLS]", cls), ("[SEP]", sep)])
tok.decoder = decoders.WordPiece(prefix="##")
```

## Inspect each stage
`tok.normalizer.normalize_str("Héllo")`, `tok.pre_tokenizer.pre_tokenize_str("Hello, world")` show intermediate output with offsets.

## Use with Transformers
```python
from transformers import PreTrainedTokenizerFast
hf_tok = PreTrainedTokenizerFast(tokenizer_object=tok, bos_token="<|endoftext|>",
                                 eos_token="<|endoftext|>", pad_token="<|pad|>")
hf_tok.save_pretrained("my-tokenizer")
```

## Gotchas
- Lowercasing/accent stripping cannot be undone at decode; avoid for generative models.
- Digits and whitespace handling (e.g. `pre_tokenizers.Digits(individual_digits=True)`) strongly affect arithmetic and code.
- Changing normalizers after training invalidates the vocabulary; retrain.

## Verify
- [ ] `hf_tok.decode(hf_tok.encode(s))` reproduces sample strings (including unicode and whitespace) for byte-level tokenizers.
