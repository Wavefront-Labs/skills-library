---
id: computing-software.systems-network-administration.paperless-ngx.auto-classifier
name: auto-classifier
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, auto-matching, classifier, scikit-learn, no-training-data, document-create-classifier]
level: practitioner
status: docs-checked
description: "How the Auto matching classifier learns, when it retrains, its threshold, the 'No training data' error and SSE4.2 crashes on old CPUs."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/troubleshooting/"
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic matching (classifier)

Auto uses a neural network trained on how you have already filed documents. Set a tag, correspondent, type or storage path to Auto and it learns when to assign it.

## Rules of the game
- It trains only on documents without an inbox tag, so tag-correct documents first.
- It needs enough examples, and enough negative ones. If every document is either "Webshop" or "Bank", every new document gets one of them.
- It needs a real correlation. A tag like "TODO" cannot be learned.
- Changes show up after retraining. The schedule `PAPERLESS_TRAIN_TASK_CRON` defaults to `5 */1 * * *` (hourly); `disable` stops it. Force a run with `document_create_classifier`.
- `PAPERLESS_CLASSIFIER_MATCH_THRESHOLD` (default 0.3) discards low-confidence correspondent, type and path predictions.

## Errors
- "No training data available": you have no Auto rules (ignore it) or all documents carry inbox tags.
- sklearn `UserWarning` on unpickling after an update: usually ignorable. To clear it, delete `classification_model.pickle` in the data directory and let Paperless rebuild it.

## Old CPUs
NumPy 2.4 wheels need x86-64-v2 (SSE4.2). On older CPUs the classifier causes `SIGILL` crashes of the worker. Check:
```bash
grep -o -m1 sse4_2 /proc/cpuinfo
```
If it prints nothing, set `PAPERLESS_TRAIN_TASK_CRON=disable`. Classifier-based suggestions are lost; rule-based matching still works.

## Checked
2026-11-04. Compared with the Automatic matching section of advanced_usage, the classifier and sklearn entries of troubleshooting, PAPERLESS_CLASSIFIER_MATCH_THRESHOLD and PAPERLESS_TRAIN_TASK_CRON in configuration, the classifier command in administration, and the NumPy baseline section of the v3 migration page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: every rule listed, hourly default schedule and `disable`, threshold default 0.3 and which fields it covers, both errors and their remedies, x86-64-v2/SSE4.2 requirement, SIGILL symptom, the check command and the disable workaround with its effect. Nothing removed.

Method: documentation only; no commands were run.
