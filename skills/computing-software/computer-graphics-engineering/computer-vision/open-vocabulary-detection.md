---
id: computing-software.computer-graphics-engineering.computer-vision.open-vocabulary-detection
name: open-vocabulary-detection
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, recognition, open-vocabulary-detection, grounding-dino, owlv2, yolo-world, zero-shot-detection]
level: practitioner
status: draft
description: "Detect objects from text prompts with open-vocabulary models (OWLv2, Grounding DINO, YOLO-World): prompts, thresholds, speed, and distilling into a closed-set detector."
sources: ["https://huggingface.co/docs/transformers/model_doc/owlv2", "https://github.com/IDEA-Research/GroundingDINO", "https://docs.ultralytics.com/models/yolo-world/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open-vocabulary detection

## Models
| Model | Strength | Speed |
|---|---|---|
| Grounding DINO (1.5/Swin) | Best phrase grounding, referring expressions | Slow (hundreds of ms) |
| OWLv2 | Good zero-shot boxes, image-conditioned queries | Medium |
| YOLO-World / YOLOE | Real-time, set vocabulary offline | Fast |
| Florence-2 | Captioning + grounding in one | Medium |

## Usage (transformers, OWLv2)
```python
from transformers import Owlv2Processor, Owlv2ForObjectDetection
proc = Owlv2Processor.from_pretrained("google/owlv2-base-patch16-ensemble")
model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble")
inputs = proc(text=[["a forklift", "a person wearing a hard hat"]], images=img, return_tensors="pt")
out = model(**inputs)
res = proc.post_process_object_detection(out, threshold=0.2, target_sizes=[img.size[::-1]])
```
OWLv2 pads images to square: box coordinates refer to the padded image; rescale using the padded
size.

## Prompts
- Short concrete noun phrases ("forklift" not "industrial vehicle used for lifting").
- Grounding DINO: separate classes with " . " (e.g. `"person . helmet . forklift ."`).
- Add negative/confuser classes so the model has somewhere to put them.
- Thresholds are prompt-specific; calibrate each class on a few labelled images.

## Production pattern
Zero-shot models are slow and less precise than trained detectors. Use them to **auto-label**
(then human-verify) and train a closed-set YOLO/RT-DETR on the result; or set YOLO-World's
vocabulary once and export it as a fixed-class model.

## Verify
Measure AP per class on 100 to 200 labelled images before trusting it; check false positives on
images without the target.
