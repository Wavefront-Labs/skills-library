---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-lstm-gru-cudnn-conditions
name: keras-lstm-gru-cudnn-conditions
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-lstm, cudnn-lstm, gru, recurrent-layers, bidirectional, stateful-rnn]
level: practitioner
status: docs-checked
description: "Use Keras LSTM/GRU efficiently: cuDNN fast-kernel conditions, return_sequences/return_state, Bidirectional, stateful RNNs and masking with right-padding."
sources:
  - https://keras.io/api/layers/recurrent_layers/lstm/
  - https://keras.io/guides/working_with_rnns/
  - https://github.com/keras-team/keras/blob/master/keras/src/layers/rnn/rnn.py
  - https://github.com/keras-team/keras/blob/master/keras/src/layers/rnn/lstm.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keras LSTM / GRU and cuDNN kernel conditions

**Goal:** get the fused cuDNN kernel and wire RNN outputs correctly.

## cuDNN fast path conditions
The `use_cudnn` argument of `LSTM` and `GRU` defaults to `"auto"`: use a cuDNN-backed implementation when feasible, otherwise fall back to the default implementation. The Keras RNN guide says the layer cannot use the cuDNN kernel if you change the defaults, for example:
- `activation` other than `tanh`, or `recurrent_activation` other than `sigmoid`
- `recurrent_dropout > 0`, `unroll=True`, `use_bias=False`
- masking where the input is not strictly right padded (strictly right-padded masks can still use cuDNN)
- GRU: `reset_after=True` is the default and is cuDNN compatible
- cuDNN is only available at the layer level: `LSTM(units)` can use it, `RNN(LSTMCell(units))` cannot

Use input `dropout=` instead of `recurrent_dropout=` to keep the fast path. The Keras 3 source defines a `cudnn_ok` check per backend (TensorFlow, JAX and PyTorch) covering the activation, recurrent activation, unroll and bias conditions.

## Outputs
```python
from keras import layers
seq = layers.LSTM(128, return_sequences=True)(x)            # (B, T, 128) for stacking or seq labeling
last, h, c = layers.LSTM(128, return_state=True)(x)        # final output + states (LSTM has h and c)
bi = layers.Bidirectional(layers.GRU(64, return_sequences=True), merge_mode="concat")(x)  # (B, T, 128)
```
Stack RNNs with `return_sequences=True` on every layer except possibly the last.

## Encoder-decoder state passing
`decoder = layers.LSTM(128, return_sequences=True)(dec_in, initial_state=[h, c])`.

## Stateful RNNs
`stateful=True` reuses the states computed for the samples of one batch as the initial states for the next batch, so it assumes a one-to-one mapping between samples in successive batches (long sequences split into chunks). Specify a fixed batch size (`batch_size=...` on the `Input`), use `shuffle=False` in `fit()`, and call `reset_state()` on the layer or the whole model to clear the states.

## Verify
- [ ] Time one epoch with a deliberately non-cuDNN config (e.g. `recurrent_dropout=0.1`) vs default to confirm the fast kernel is active.
- [ ] Output shapes printed with `model.summary()` match expectations.

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23). Confirmed the cuDNN conditions and the layer-level restriction (Keras RNN guide), the `use_cudnn="auto"` argument and `reset_after=True` default (LSTM and GRU source), the per-backend `cudnn_ok` functions, `return_sequences`, `return_state`, `initial_state`, and the statefulness requirements and `reset_state()` (RNN layer docstring). Replaced the removed Keras 2 `reset_states()` with `reset_state()`; removed the 3-10x figure, the eager/tf.function condition and the opinion section.

Method: documentation only; no commands were run.
