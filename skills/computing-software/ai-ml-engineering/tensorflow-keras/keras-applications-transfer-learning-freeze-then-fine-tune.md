---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-applications-transfer-learning-freeze-then-fine-tune
name: keras-applications-transfer-learning-freeze-then-fine-tune
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, keras-transfer-learning, keras-applications, fine-tuning, batchnorm-inference]
level: practitioner
status: docs-checked
description: "Transfer learn with Keras Applications: matching preprocess_input, a new head on a frozen base, then unfreeze top layers at low LR with BatchNorm kept in inference mode."
sources:
  - https://keras.io/guides/transfer_learning/
  - https://keras.io/api/applications/
  - https://www.tensorflow.org/tutorials/images/transfer_learning
  - https://github.com/keras-team/keras/blob/master/keras/src/applications/efficientnet.py
  - https://github.com/keras-team/keras/blob/master/keras/src/applications/imagenet_utils.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keras Applications transfer learning

## Step 1: frozen base + new head
```python
import keras
base = keras.applications.EfficientNetB0(include_top=False, weights="imagenet", input_shape=(224, 224, 3))
base.trainable = False
inputs = keras.Input((224, 224, 3))
x = keras.applications.efficientnet.preprocess_input(inputs)   # model-specific preprocessing
x = base(x, training=False)            # BN in inference mode, now and after unfreezing
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.2)(x)
outputs = keras.layers.Dense(num_classes)(x)
model = keras.Model(inputs, outputs)
model.compile(keras.optimizers.Adam(1e-3), keras.losses.SparseCategoricalCrossentropy(from_logits=True), ["accuracy"])
model.fit(train_ds, validation_data=val_ds, epochs=10)
```

## Step 2: fine-tune top layers
```python
base.trainable = True
for layer in base.layers[:-40]: layer.trainable = False      # keep early layers frozen
model.compile(keras.optimizers.Adam(1e-5), ...)               # recompile after changing trainable
model.fit(train_ds, validation_data=val_ds, epochs=10)
```

## The rules that matter
- **Use the matching `preprocess_input`.** ResNet50 expects caffe-style BGR mean subtraction, MobileNet scales to [-1, 1], EfficientNet in Keras includes rescaling internally (its preprocess_input is a pass-through). Wrong preprocessing silently costs a lot of accuracy.
- **`training=False` when calling the base.** Keeps BatchNorm using its ImageNet running stats even after unfreezing. Without it, small fine-tuning batches update BN stats and wreck the pretrained features (a classic sudden accuracy drop at fine-tune start).
- **Recompile after changing `trainable`**; the compiled step captures which weights train.
- **Train the head first.** Unfreezing with a randomly initialised head sends large gradients into the base.
- **Very low LR for fine-tuning**: the Keras guide uses `Adam(1e-5)` after head training.
- Keep BN layers frozen even when unfreezing the block (`if isinstance(layer, keras.layers.BatchNormalization): layer.trainable = False`).

## Data
Augment with preprocessing layers inside the model (`RandomFlip`, `RandomRotation`) so they run on GPU and are off at inference. Input resolution should match the base's native size where possible.

## Verify
- `len(model.trainable_weights)` before and after unfreezing.
- Validation accuracy should not drop at the start of fine-tuning; if it does, check `training=False` and the LR.

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23). Confirmed the freeze-then-fine-tune workflow, `training=False` when calling the base model so BatchNormalization stays in inference mode, recompiling after changing `trainable`, and the very low fine-tuning learning rate (Keras transfer-learning guide); ResNet50 `preprocess_input` uses `mode="caffe"`, MobileNetV2 uses `mode="tf"` (scales to [-1, 1]) and EfficientNet's `preprocess_input` is a documented no-op placeholder (Keras source).

Method: documentation only; no commands were run.
