---
id: computing-software.ai-ml-engineering.model-training.detection-and-segmentation-metrics-iou-map
name: detection-and-segmentation-metrics-iou-map
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, iou, detection-map, mean-average-precision, object-detection, segmentation-metrics, coco-eval]
level: practitioner
status: verified
description: "Evaluate detection and segmentation: IoU and matching, AP per class, COCO mAP@[.5:.95] vs VOC mAP@.5, small/medium/large breakdowns, mIoU/Dice for masks and tooling."
sources:
  - https://cocodataset.org/#detection-eval
  - https://pypi.org/project/torchmetrics/
  - https://github.com/cocodataset/cocoapi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Detection and segmentation metrics (IoU, mAP)

## IoU
`IoU = area(pred ∩ gt) / area(pred ∪ gt)` for boxes or masks. A prediction is a true positive when IoU >= threshold with an unmatched ground truth of the same class (greedy matching in descending confidence).

## Average precision
For each class: sort predictions by confidence, compute the precision-recall curve from TP/FP, integrate (COCO uses 101-point interpolation). mAP averages AP over classes.

| Convention | Definition |
|---|---|
| Pascal VOC | AP at IoU 0.5 (`mAP@0.5`) |
| COCO primary | mean of AP over IoU 0.50:0.05:0.95 (`mAP@[.5:.95]`), rewards precise localization |
| COCO extras | AP50, AP75, AP_small/medium/large (area < 32^2, 32^2-96^2, > 96^2), AR@1/10/100 (checked against pycocotools `Params`: 10 IoU thresholds 0.50..0.95, 101 recall points, maxDets [1, 10, 100], area ranges 0-1024, 1024-9216, 9216+) |
Always state which one you report; values differ hugely.

## Compute
```python
from torchmetrics.detection import MeanAveragePrecision   # needs torchvision installed, else the import fails
metric = MeanAveragePrecision(iou_type="bbox", class_metrics=True)
metric.update(preds=[{"boxes": pb, "scores": ps, "labels": pl}],
              target=[{"boxes": gb, "labels": gl}])          # boxes xyxy absolute pixels
res = metric.compute(); print(res["map"], res["map_50"], res["map_small"])
```
pycocotools (`COCOeval`) is the reference implementation; torchmetrics needs `pycocotools` or `faster-coco-eval` installed (`backend="pycocotools"` ran on torchmetrics 1.9.0; pycocotools installed from a Windows wheel). Ground truth fed back as predictions gave `map` = 1.0, and the result dict also holds `map_50`, `map_75`, `map_small/medium/large` (-1.0 when no box falls in that area range), `mar_1/10/100`, `map_per_class`, `classes`. Box format mismatches (xywh vs xyxy, normalized vs pixels) are the most common bug.

## Segmentation
- Semantic: per-class IoU and mean IoU (mIoU) over classes; Dice = 2|A∩B| / (|A| + |B|) (common in medical imaging).
- Instance: mask AP (`iou_type="segm"`). Panoptic: PQ = SQ x RQ.

## Operational view
mAP ignores the deployment threshold. Also report precision/recall at the chosen confidence threshold, per-class errors, and FPs per image, which drive user experience.

## Verify
- [ ] Sanity check: ground truth as predictions (score 1.0) yields mAP 1.0 with your pipeline.
