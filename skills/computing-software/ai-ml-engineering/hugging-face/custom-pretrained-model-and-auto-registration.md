---
id: computing-software.ai-ml-engineering.hugging-face.custom-pretrained-model-and-auto-registration
name: custom-pretrained-model-and-auto-registration
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, custom-pretrained-model, register-for-auto-class, pretrainedconfig, pretrainedmodel, transformers, auto-classes]
level: practitioner
status: gated
description: "Package a custom architecture as a Transformers model: PretrainedConfig, PreTrainedModel, AutoConfig/AutoModel registration, register_for_auto_class and Hub code sharing."
sources:
  - https://huggingface.co/docs/transformers/main/en/custom_models
  - https://huggingface.co/docs/transformers/main/en/main_classes/configuration
  - https://huggingface.co/docs/transformers/main/en/main_classes/model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom models with PretrainedConfig and PreTrainedModel

**Goal:** your own architecture gets `from_pretrained`/`save_pretrained`, Trainer compatibility, Hub sharing and `AutoModel` loading.

## Config
```python
from transformers import PretrainedConfig
class TinyConvConfig(PretrainedConfig):
    model_type = "tinyconv"                       # unique; used by Auto mapping
    def __init__(self, channels=64, num_blocks=4, **kwargs):
        self.channels, self.num_blocks = channels, num_blocks
        super().__init__(**kwargs)   # always forward kwargs; num_labels / id2label live in PretrainedConfig
```
All args need defaults and must be JSON-serializable (config.json; a non-serializable value such as `object()` raises `TypeError` in `to_json_string()`, checked).

Do not give the config its own `num_labels=10` argument and forward it to `super().__init__`: `PretrainedConfig` saves `id2label` (not `num_labels`) to config.json, so on reload your default 10 conflicts with the saved map. Checked in transformers 5.20 with `num_labels=3`: `from_pretrained` logged "You passed `num_labels=10` which is incompatible to the `id2label` map of length 3" and raised a size-mismatch `RuntimeError` for `head.weight`/`head.bias`. Without the extra argument the round trip works (`num_labels=3` passed as a keyword, default is 2), and the model reads `config.num_labels`.

## Model
```python
import torch.nn as nn
from transformers import PreTrainedModel
from transformers.modeling_outputs import SequenceClassifierOutput

class TinyConvForImageClassification(PreTrainedModel):
    config_class = TinyConvConfig
    base_model_prefix = "tinyconv"
    main_input_name = "pixel_values"
    def __init__(self, config):
        super().__init__(config)
        self.body = nn.Sequential(*[nn.Conv2d(3 if i == 0 else config.channels, config.channels, 3, padding=1)
                                    for i in range(config.num_blocks)])
        self.head = nn.Linear(config.channels, config.num_labels)   # sized from the config's own num_labels
        self.post_init()                                     # weight init + final setup
    def _init_weights(self, module):
        if isinstance(module, (nn.Linear, nn.Conv2d)):
            nn.init.normal_(module.weight, std=0.02); nn.init.zeros_(module.bias)
    def forward(self, pixel_values, labels=None, **kwargs):
        logits = self.head(self.body(pixel_values).mean((2, 3)))
        loss = nn.functional.cross_entropy(logits, labels) if labels is not None else None
        return SequenceClassifierOutput(loss=loss, logits=logits)
```
Returning `loss` first when `labels` is passed lets `Trainer` work unchanged.

## Auto registration
Local: `AutoConfig.register("tinyconv", TinyConvConfig); AutoModelForImageClassification.register(TinyConvConfig, TinyConvForImageClassification)`. Checked: before registering, `AutoConfig.from_pretrained` on the saved folder raises `ValueError: The checkpoint you are trying to load has model type `tinyconv` but Transformers does not recognize this architecture`; after registering, `AutoModelForImageClassification.from_pretrained` returns a `TinyConvForImageClassification`.

Hub (code travels with weights):
```python
TinyConvConfig.register_for_auto_class()
TinyConvForImageClassification.register_for_auto_class("AutoModelForImageClassification")
model.push_to_hub("me/tinyconv")    # uploads modeling/config .py files plus auto_map in config.json (push_to_hub itself needs a Hub account and was not run: gated: unconfirmed, source is paywalled or blocked)
```
Checked locally with `save_pretrained` after `register_for_auto_class`: the folder gains `tinyconv.py` and `config.json` gets `auto_map` with `AutoConfig` and `AutoModelForImageClassification` entries; loading it with `AutoModelForImageClassification.from_pretrained(path, trust_remote_code=True)` works and without the flag raises `ValueError` ("contains custom code which must be executed"). Users load with `trust_remote_code=True` (and should pin `revision=`). Keep the model code in its own module file (not `__main__`) so it can be copied.

## Verify
- [ ] `save_pretrained` -> `from_pretrained` round trip gives identical outputs.
- [ ] Loading from the Hub in a fresh environment with `trust_remote_code=True` works.
