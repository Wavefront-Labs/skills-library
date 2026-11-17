---
id: computing-software.ai-ml-engineering.tensorflow-keras.subclassed-models-call-training-and-add-loss
name: subclassed-models-call-training-and-add-loss
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, model-subclassing, add-loss, keras-training-argument, keras-model, custom-model]
level: practitioner
status: gated
description: "Write subclassed Keras models correctly: build vs __init__, the training argument, add_loss for regularizers, tracking sublayers and making them saveable."
sources:
  - https://keras.io/guides/making_new_layers_and_models_via_subclassing/
  - https://keras.io/api/models/model/
  - https://keras.io/api/losses/#the-addloss-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Subclassed models: call(training=) and add_loss

**Use subclassing when:** the forward pass has Python control flow, loops over time, or multiple modes that the Functional API cannot express. Otherwise prefer Functional (serializable, plottable, summary shows shapes).

## Skeleton
```python
import keras
from keras import layers, ops

class VAE(keras.Model):
    def __init__(self, latent=16, **kwargs):
        super().__init__(**kwargs)
        self.latent = latent
        self.enc = keras.Sequential([layers.Dense(256, activation="relu"), layers.Dense(2 * latent)])
        self.dec = keras.Sequential([layers.Dense(256, activation="relu"), layers.Dense(784)])
        self.drop = layers.Dropout(0.2)

    def call(self, x, training=False):
        h = self.drop(x, training=training)            # pass training down explicitly
        mean, logvar = ops.split(self.enc(h), 2, axis=-1)
        z = mean + ops.exp(0.5 * logvar) * keras.random.normal(ops.shape(mean))
        kl = -0.5 * ops.mean(ops.sum(1 + logvar - mean**2 - ops.exp(logvar), axis=-1))
        self.add_loss(kl)                               # added to the compiled loss by fit()
        return self.dec(z)

    def get_config(self):
        return {**super().get_config(), "latent": self.latent}
```

## The training argument
- `fit()` calls `call(x, training=True)`, `evaluate/predict` use `training=False`.
- Layers that behave differently (Dropout, BatchNormalization) read it. Ran on Keras 3.15: a subclassed model whose `call(self, x)` has no `training` argument still dropped about 49% of units under `model(x, training=True)` and 0% under `training=False`, and the same with `call(self, x, training=False)` that did not forward it. So Keras propagates it through the call context; passing it explicitly is still clearer and safer across versions.
- BatchNorm in transfer learning: call the frozen base with `training=False` so its statistics stay fixed even when unfrozen later.

## add_loss
- Losses added in `call` are collected in `model.losses` and summed with the compiled loss each step (ran with the VAE skeleton: `len(v.losses) == 1` after one forward pass, `fit` ran for 2 epochs, and the logged `loss` included the KL term). Use for KL terms, activity regularization, auxiliary losses.
- In a custom `train_step` that calls `self.compute_loss(...)`, check that the added losses are included; if you compute the loss by hand, add `sum(self.losses)` yourself.

## Tracking and saving
- Sublayers assigned as attributes are tracked automatically (ran: the `Sequential` encoder, decoder and Dropout appeared in `summary()`); lists and dicts of layers were not tested here (gated: unconfirmed, source is paywalled or blocked).
- Implement `get_config` (and `from_config` if constructor args are not plain) and decorate with `@keras.saving.register_keras_serializable()` to save in `.keras` format (ran: a registered subclass of the VAE saved to `.keras` and reloaded as `VAE2`, with matching output shape).
- `model.summary()` on an unbuilt subclassed model did not raise in Keras 3.15; it printed `0 (unbuilt)` for the sublayers and 0 total params. Call the model once on data or `model.build(input_shape)` first (ran: `build((None, 784))` then `summary()` worked).

## Verify
- [ ] `model(x, training=True)` and `training=False` differ only where expected (dropout/BN).
- [ ] `len(model.losses)` > 0 after a forward pass when using add_loss.
- [ ] Save to `.keras`, reload, and outputs match in inference mode.
