---
id: computing-software.ai-ml-engineering.tensorflow-keras.kerashub-pretrained-models-and-presets
name: kerashub-pretrained-models-and-presets
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-hub, kerashub, presets, pretrained-models, from-preset, fine-tuning]
level: practitioner
status: docs-checked
description: "Load and fine-tune KerasHub pretrained models from presets: task vs backbone classes, preprocessors, LoRA, Kaggle and Hugging Face handles, saving and uploading presets."
sources:
  - https://keras.io/keras_hub/
  - https://keras.io/keras_hub/getting_started/
  - https://keras.io/api/keras_hub/models/
  - https://github.com/keras-team/keras-hub/blob/master/keras_hub/src/models/backbone.py
  - https://github.com/keras-team/keras-hub/blob/master/keras_hub/src/utils/preset_utils.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KerasHub pretrained models and presets

KerasHub (`pip install keras-hub`, formerly KerasNLP) ships pretrained models as **presets** that work on any Keras 3 backend.

## Load
```python
import keras_hub
classifier = keras_hub.models.TextClassifier.from_preset("bert_base_en_uncased", num_classes=2)
lm = keras_hub.models.CausalLM.from_preset("gemma2_2b_en")
img = keras_hub.models.ImageClassifier.from_preset("resnet_50_imagenet")
```
- **Task** classes (`TextClassifier`, `CausalLM`, `ImageClassifier`, `Seq2SeqLM`, `ImageSegmenter`) bundle backbone + head + **preprocessor**, so `fit`/`predict` accept raw strings or images.
- **Backbone** classes (`keras_hub.models.Backbone.from_preset`) give features only.
- Preset handles: built-in names, Kaggle handles of the form `kaggle://<org>/<model>/keras/<variant>[/<version>]` (for example `kaggle://keras/gemma2/keras/gemma2_2b_en`), `hf://<user>/<repo>` handles, or a local directory.
- List: `keras_hub.models.CausalLM.presets.keys()`.

## Fine-tune
```python
classifier.fit(train_ds.batch(16), validation_data=val_ds.batch(16), epochs=2)   # raw (text, label) pairs
lm.backbone.enable_lora(rank=8)              # train only LoRA adapters
lm.preprocessor.sequence_length = 512
lm.compile(optimizer=keras.optimizers.AdamW(5e-5, weight_decay=0.01),
           loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), weighted_metrics=["accuracy"])
lm.fit(texts_ds, epochs=1)
print(lm.generate("Explain overfitting:", max_length=128))
```
- Pass `dtype="bfloat16"` to `from_preset()` to load large models in lower precision (`from_preset` forwards `dtype` and other layer arguments).
- Sampling: `lm.compile(sampler=keras_hub.samplers.TopPSampler(p=0.9))`.

## Preprocessing separately
`preprocessor = keras_hub.models.TextClassifierPreprocessor.from_preset(...)`; map it in `tf.data` and pass `preprocessor=None` to the task for faster input pipelines.

## Save and share
```python
lm.save_to_preset("my_gemma_ft")                      # config + weights + tokenizer assets
keras_hub.upload_preset("kaggle://user/my_gemma_ft/keras/v1", "my_gemma_ft")   # or hf://user/repo
```

## Gotchas
- Gated models such as Gemma need an accepted licence on the Kaggle model page and Kaggle credentials (`KAGGLE_USERNAME`, `KAGGLE_KEY`).
- Distribution (model parallel) must be set before `from_preset`.
- Preset versions change; pin full handles with version for reproducibility.

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23) and KerasHub master (2026-10). Confirmed the `from_preset()` task and backbone classes, `presets` listing on `Backbone` and `Task` classes, the `bert_base_en_uncased` and `resnet_50_imagenet` preset names (preset files), `kaggle://` and `hf://` prefixes (`preset_utils.py`), `Backbone.enable_lora(rank, target_layer_names=None)`, `save_to_preset`, `keras_hub.upload_preset(uri, preset_dir)`, `compile(sampler=...)`, the `sequence_length` attribute of causal LM preprocessors, `preprocessor=None`, the Kaggle licence and credential steps for Gemma, and the README note that KerasNLP is now KerasHub. Removed the KerasCV rename, automatic Hugging Face conversion, `HF_TOKEN`, memory-halving and `.keras` comparison claims.

Method: documentation only; no commands were run.
