---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-multiheadattention-transformer-blocks
name: keras-multiheadattention-transformer-blocks
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-multiheadattention, transformer-block, attention-mask, causal-mask, keras]
level: practitioner
status: verified
description: "Build transformer encoder and decoder blocks with keras.layers.MultiHeadAttention: shapes, attention_mask vs use_causal_mask, padding masks and positional embeddings."
sources:
  - https://keras.io/api/layers/attention_layers/multi_head_attention/
  - https://keras.io/examples/nlp/text_classification_with_transformer/
  - https://www.tensorflow.org/text/tutorials/transformer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keras MultiHeadAttention and transformer blocks

## The layer
```python
mha = keras.layers.MultiHeadAttention(num_heads=8, key_dim=64, dropout=0.1)
out, scores = mha(query=x, value=ctx, key=ctx, attention_mask=mask,
                  use_causal_mask=False, return_attention_scores=True, training=training)
```
- Shapes: `query (B, Tq, D)`, `value/key (B, Tv, D)`; output `(B, Tq, D)` projected back to query's last dim (or `output_shape`). Ran with B=2, Tq=5, Tv=7, D=8, 2 heads: output `(2, 5, 8)`, scores `(2, 2, 5, 7)`.
- `key_dim` is per head; total projection width = `num_heads * key_dim`, usually `D // num_heads`.
- Self-attention: `mha(x, x)`. `key` defaults to `value`.

## Masks
- `attention_mask` shape `(B, Tq, Tv)`, boolean, True = may attend. Build from padding: `pad = ids != 0; mask = pad[:, None, :]`.
- `use_causal_mask=True` adds the lower-triangular mask (decoder self-attention); the attention scores above the diagonal summed to 0.0. Combined with `attention_mask` by AND (ran: masking keys 3-4 plus causal gave zeros in those columns and the causal triangle elsewhere).
- Keras propagates masks automatically: if the input comes from `Embedding(mask_zero=True)`, MHA uses the query/value `_keras_mask` and you can omit `attention_mask` (ran: attention scores onto padded keys were 0.0). Check with `x._keras_mask` in a debug call. The `call` signature in Keras 3.15 is `(query, value, key=None, query_mask=None, value_mask=None, key_mask=None, attention_mask=None, return_attention_scores=False, training=None, use_causal_mask=False)`.

## Encoder block (pre-norm)
```python
class EncoderBlock(keras.layers.Layer):
    def __init__(self, d, heads, ff, rate=0.1, **kw):
        super().__init__(**kw)
        self.att = keras.layers.MultiHeadAttention(heads, d // heads, dropout=rate)
        self.ffn = keras.Sequential([keras.layers.Dense(ff, activation="gelu"), keras.layers.Dense(d)])
        self.n1, self.n2 = keras.layers.LayerNormalization(epsilon=1e-6), keras.layers.LayerNormalization(epsilon=1e-6)
        self.drop = keras.layers.Dropout(rate)
    def call(self, x, training=False):
        h = self.n1(x)
        x = x + self.drop(self.att(h, h, training=training), training=training)
        return x + self.drop(self.ffn(self.n2(x)), training=training)
```
Decoder adds a causal self-attention (`use_causal_mask=True`) and a cross-attention `mha(query=x, value=enc_out)`.

## Positions
MHA is permutation invariant; add positions: learned `keras.layers.Embedding(max_len, d)` on `ops.arange(T)`, or sinusoidal. KerasHub provides `keras_hub.layers.PositionEmbedding`, `SinePositionEncoding`, `RotaryEmbedding`, plus ready `TransformerEncoder` / `TransformerDecoder` layers (all five exist in the installed keras-hub).

## Performance
- Mixed precision (`keras.mixed_precision.set_global_policy("mixed_bfloat16")`) is available but its speed benefit needs supporting hardware and was not tested here.
- `MultiHeadAttention.__init__` has a `flash_attention` argument (default `None`) in Keras 3.15; without a fused kernel the scores are `(B, heads, Tq, Tv)`, i.e. O(T^2) memory per head.

## Gotchas
- Forgetting `training=training` disables attention dropout in fit or enables it in predict.
- `return_attention_scores=True` materialises `(B, heads, Tq, Tv)`; turn it off in production.
- Serialise custom blocks with `get_config` and `@keras.saving.register_keras_serializable()`.
