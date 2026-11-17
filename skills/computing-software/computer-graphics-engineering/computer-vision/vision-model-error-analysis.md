---
id: computing-software.computer-graphics-engineering.computer-vision.vision-model-error-analysis
name: vision-model-error-analysis
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-data-evaluation, error-analysis, failure-slicing, tide, fiftyone, label-errors]
level: practitioner
status: draft
description: "Find why a vision model fails: per-slice metrics, confusion analysis, TIDE error breakdown for detection, FiftyOne evaluation views, label error detection and prioritising fixes."
sources: ["https://docs.voxel51.com/user_guide/evaluation.html", "https://github.com/dbolya/tide", "https://github.com/cleanlab/cleanlab"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Error analysis and failure slicing

## 1. Look at errors, systematically
```python
import fiftyone as fo
ds = fo.Dataset.from_dir(dataset_dir="val", dataset_type=fo.types.COCODetectionDataset)
# add predictions to ds as a "predictions" field, then:
res = ds.evaluate_detections("predictions", gt_field="ground_truth", eval_key="eval", compute_mAP=True)
res.print_report()
view = ds.filter_labels("predictions", fo.ViewField("eval") == "fp").sort_by("predictions.detections.confidence", reverse=True)
session = fo.launch_app(view)
```
Review the highest-confidence false positives and the largest false negatives first.

## 2. Slice metrics by metadata
Lighting (day/night), camera, location, object size (small/medium/large), occlusion, distance,
weather, demographic attributes. A healthy average can hide a slice at half the accuracy. Add
metadata tags during collection so slicing is possible.

## 3. Detection error types (TIDE)
TIDE attributes lost mAP to: classification, localisation, both, duplicate, background (false
positive), missed. Fix the largest bucket:
- Localisation -> better box regression/resolution.
- Background -> hard negatives, more context.
- Missed -> small objects: higher input resolution, tiling.
- Classification -> confusable classes: more examples, merge classes, fine-grained head.

## 4. Label errors
High-loss and high-confidence-disagreement samples are often **label** mistakes. Cleanlab
(`find_label_issues`) or FiftyOne `compute_mistakenness` rank them; relabel before adding model
capacity. Typical public datasets have several percent label errors.

## 5. Prioritise
For each failure cluster estimate: frequency x impact x cost to fix (data collection, labels,
model change). Write it down; re-run the same analysis after each change.

## Verify
Track per-slice metrics in every evaluation report, not just the headline number.
