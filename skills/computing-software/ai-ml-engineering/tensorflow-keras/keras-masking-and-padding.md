---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-masking-and-padding
name: keras-masking-and-padding
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-masking, mask-zero, padding, sequence-models, compute-mask]
level: practitioner
status: verified
description: "Handle variable-length sequences in Keras: pad_sequences, Embedding(mask_zero=True), Masking layer, mask propagation, supports_masking and custom compute_mask."
sources:
  - https://keras.io/api/layers/core_layers/masking/
  - https://keras.io/api/layers/core_layers/embedding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Masking and padding for sequences

**Goal:** pad batches to a common length without letting padding tokens affect RNN states, attention or the loss.

## Pad
```python
import keras
x = keras.utils.pad_sequences(seqs, padding="post", maxlen=128, value=0)  # ran with maxlen=5: [[3 4 0 0 0] [5 6 7 8 0] [9 0 0 0 0]]
```

## Create a mask
- `layers.Embedding(vocab, 64, mask_zero=True)`: index 0 is reserved for padding; the layer emits a boolean mask `(B, T)` (ran: `[[T T F F F] ...]`). Your real vocabulary must start at 1, so `input_dim` must be vocab size + 1.
- `layers.Masking(mask_value=0.0)`: for already-continuous inputs (e.g. time-series features), masks timesteps where all features equal `mask_value` (ran: `[[T F T]]` for a row with an all-zero middle step).
- Pass explicitly: `layer(x, mask=bool_tensor)` for layers whose `call` accepts `mask`.

## Propagation
- Mask-consuming layers: LSTM/GRU (skip masked steps, carry state: an LSTM on `[3,4,0,0,0]` with `mask_zero=True` equalled the LSTM on `[3,4]` to 1e-6), MultiHeadAttention (its `call` has `query_mask`, `value_mask`, `key_mask`, or uses automatic propagation), GlobalAveragePooling1D (ran: mask `[T,T,F]` on `[1,3,100]` gave 2.0).
- Layers that pass the mask through unchanged set `supports_masking = True` (checked: Dense, Dropout and Activation report `True`).
- A layer with `supports_masking` left `False` that receives a mask raised no error in Keras 3.15 (in both eager and Functional use), and the mask was still attached to its output tensor; older Keras versions raised. Do not rely on either behaviour: set `supports_masking` and implement `compute_mask` deliberately.
- Masks propagate automatically between layers in the Functional API and, in Keras 3.15, also in a subclassed `Model` whose `call` chains Embedding and LSTM (ran: the auto-propagated result equalled the explicit `mask=` result and the unpadded reference).

## Custom layer
```python
class MaskedMeanPool(keras.layers.Layer):
    def __init__(self, **kw):
        super().__init__(**kw); self.supports_masking = True
    def call(self, x, mask=None):
        if mask is None: return keras.ops.mean(x, axis=1)
        m = keras.ops.cast(mask, x.dtype)[..., None]
        return keras.ops.sum(x * m, axis=1) / keras.ops.maximum(keras.ops.sum(m, axis=1), 1.0)
    def compute_mask(self, x, mask=None):
        return None                          # time axis removed, so no mask downstream
```

## Loss masking
For sequence outputs, masks reach the loss automatically when the final layer carries a mask; otherwise pass `sample_weight` with zeros at padded positions.

## Verify
- [ ] Changing values at padded positions does not change model outputs.
- [ ] The mask exists where expected: in Keras 3 there is no `layer.output_mask`; read `tensor._keras_mask` (e.g. the Embedding output, which was a mask tensor in a debug call, a `KerasTensor` at graph-build time).
