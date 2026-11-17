---
id: computing-software.computer-graphics-engineering.computer-vision.segmentation-metrics-miou-panoptic-quality
name: segmentation-metrics-miou-panoptic-quality
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-data-evaluation, miou, panoptic-quality, dice-coefficient, segmentation-metrics, mask-ap]
level: practitioner
status: verified
description: "Compute segmentation metrics correctly: confusion-matrix mIoU, ignore labels, frequency-weighted IoU, boundary IoU, Dice, panoptic quality (PQ = SQ x RQ) and mask AP."
sources: ["https://arxiv.org/abs/1801.00868", "https://github.com/cocodataset/panopticapi", "https://lightning.ai/docs/torchmetrics/stable/", "https://arxiv.org/abs/2103.16562"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segmentation metrics (mIoU, PQ)

## Semantic: confusion matrix first
```python
def confusion(pred, gt, n, ignore=255):
    m = gt != ignore
    return np.bincount(n * gt[m].astype(int) + pred[m], minlength=n * n).reshape(n, n)
C = sum(confusion(p, g, n) for p, g in dataset)          # accumulate over the WHOLE dataset
iou = np.diag(C) / (C.sum(0) + C.sum(1) - np.diag(C))
miou = np.nanmean(iou)
```
- Accumulate the confusion matrix over the dataset, then compute IoU. Averaging per-image IoU gives a
  different number (0.13871 against 0.13872 on 5 random 32x32 label maps, so it can differ in either
  direction); state which you report.
- Exclude ignore/void pixels. Classes absent from both GT and predictions give NaN (0/0, with a NumPy RuntimeWarning): use nanmean.
- Dice = 2|A n B| / (|A| + |B|) = 2 IoU / (1 + IoU) (checked on two overlapping squares, both 0.25); medical imaging usually reports Dice per
  structure, per case.
- Boundary IoU measures edge quality, which mIoU barely notices.

## Panoptic quality
Match predicted and GT segments of the same class with IoU > 0.5 (unique matching guaranteed).
`PQ = sum_TP IoU / (|TP| + 0.5|FP| + 0.5|FN|) = SQ x RQ`, where SQ = mean IoU of matched segments,
RQ = F1 of detection. Report PQ for things and stuff separately (PQ_th, PQ_st). Use the official
`panopticapi` (`panopticapi.evaluation.pq_compute(gt_json_file, pred_json_file, gt_folder, pred_folder)`)
on COCO-format PNG + JSON; its source implements the same formula and the `iou > 0.5` match rule
(computed PQ = SQ x RQ = 0.511 for TPs 0.8, 0.6, 0.9 with 2 FP and 1 FN).

## Instance segmentation
COCO mask AP (pycocotools with `iouType="segm"`), averaged over IoU 0.5:0.95 in steps of 0.05
(ran: one mask pair with IoU 0.68 gave AP 0.400, i.e. matched at the four thresholds 0.50 to 0.65 of ten).

## Gotchas
- Predictions resized with bilinear interpolation of class ids create fake classes (a 0/10 label map
  resized bilinearly with OpenCV gained the classes 2 and 7): use nearest or resize logits.
- Report per-class IoU, not just the mean: rare classes hide behind mIoU.

## Verify
Unit-test the metric on hand-built masks with known IoU (e.g. two overlapping squares).
