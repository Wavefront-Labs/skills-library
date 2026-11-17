---
id: computing-software.ai-ml-engineering.hugging-face.autoprocessor-and-image-processors
name: autoprocessor-and-image-processors
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, autoprocessor, image-processor, feature-extractor, vision-models, audio-models, multimodal]
level: practitioner
status: gated
description: "Prepare images, audio and multimodal inputs with AutoProcessor, AutoImageProcessor and feature extractors: resizing/normalization configs, fast processors and batch transforms."
sources:
  - https://huggingface.co/docs/transformers/main/en/main_classes/processors
  - https://huggingface.co/docs/transformers/main/en/main_classes/image_processor
  - https://huggingface.co/docs/transformers/main/en/preprocessing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AutoProcessor and image/audio processors

**Rule:** always preprocess with the processor saved alongside the checkpoint; resizing, crop, mean/std and sampling rate must match pretraining.

## Which class
| Modality | Class | Output keys |
|---|---|---|
| Image | `AutoImageProcessor` | `pixel_values` |
| Audio | `AutoFeatureExtractor` | `input_values` / `input_features` |
| Text+image / speech-to-text / VLMs | `AutoProcessor` (wraps tokenizer + image/audio processor) | `input_ids`, `pixel_values`, ... |

## Images
```python
from transformers import AutoImageProcessor
proc = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224", backend="torchvision")  # torchvision-backed; backend="pil" for the PIL one
batch = proc(images=[img1, img2], return_tensors="pt")      # PIL, numpy or torch images
```
On transformers 5.20.2 `use_fast=` is deprecated (warning: use `backend="torchvision"` instead of `use_fast=True`, `backend="pil"` instead of `use_fast=False`). With torchvision installed the default and `backend="torchvision"` gave `ViTImageProcessor`; `backend="pil"` gave `ViTImageProcessorPil`; without torchvision installed, every variant returned the PIL class. Two 300x400 images gave `pixel_values` of shape (2, 3, 224, 224). Inspect `proc.size` (a `SizeDict`, here height=224, width=224), `proc.image_mean` (0.5, 0.5, 0.5 for this ViT), `proc.do_center_crop` (None for this checkpoint). For training augmentation, apply random transforms (torchvision v2/albumentations) then let the processor normalize, or build transforms from `proc.image_mean/std` yourself. Run it inside `dataset.with_transform(fn)` so it executes lazily per batch (ran: slicing a 2-image dataset returned `pixel_values` (2, 3, 224, 224)).

## Audio
```python
fe = AutoFeatureExtractor.from_pretrained("openai/whisper-small")
ds = ds.cast_column("audio", Audio(sampling_rate=fe.sampling_rate))   # resample to model rate
inputs = fe(ds[0]["audio"]["array"], sampling_rate=fe.sampling_rate, return_tensors="pt")
```
Mismatched sampling rates silently degrade accuracy; `WhisperFeatureExtractor` logs "It is strongly recommended to pass the `sampling_rate` argument" when it is omitted (seen on 5.20.2; the call still succeeds). A 1 s array gave `input_features` of shape (1, 80, 3000) and `fe.sampling_rate` was 16000. In datasets 5.1.0, `cast_column("audio", Audio(...))` on in-memory arrays raised `ImportError: To support encoding audio data, please install 'torchcodec'`, so audio decoding and resampling need `torchcodec` (and a working FFmpeg), which was not set up here (gated: unconfirmed, source is paywalled or blocked).

## Multimodal (VLMs)
```python
processor = AutoProcessor.from_pretrained(vlm_name)
messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "Describe this."}]}]
prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(images=img, text=prompt, return_tensors="pt").to(model.device)
```
Ran with `hf-internal-testing/tiny-random-LlavaForConditionalGeneration` (`LlavaProcessor`): the template rendered `<|im_start|>user <image>\nDescribe this.<|im_end|><|im_start|>assistant\n` and the processor returned `input_ids`, `attention_mask`, `pixel_values` and `image_sizes`. Note `apply_chat_template(...)` returns a string here; pass `tokenize=True, return_dict=True` for tensors directly in current releases (not run) (gated: unconfirmed, source is paywalled or blocked).

## Save together
`processor.save_pretrained(out_dir)` with the model so serving uses identical preprocessing (ran: wrote `processor_config.json`, `tokenizer.json`, `tokenizer_config.json` and `chat_template.jinja`).

## Verify
- [ ] `pixel_values.shape` and value range are as expected: normalisation uses the checkpoint's own mean/std, so for this ViT (0.5, 0.5) values lie in [-1, 1]; do not expect mean 0 / std 1 in general (random-noise test images gave std 0.25 after resizing).
- [ ] Predictions on known samples match the model card examples.
