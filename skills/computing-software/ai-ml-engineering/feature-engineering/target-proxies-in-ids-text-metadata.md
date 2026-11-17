---
id: computing-software.ai-ml-engineering.feature-engineering.target-proxies-in-ids-text-metadata
name: target-proxies-in-ids-text-metadata
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, proxy-leakage, data-leakage, target-proxy, identifier-leakage, metadata-leakage, shortcut-learning]
level: practitioner
status: draft
description: "Find target proxies hiding in IDs, free text, file metadata and collection artefacts (shortcut learning), with audits by importance, adversarial checks and data provenance review."
sources:
  - https://arxiv.org/abs/2004.07780
  - https://www.kaggle.com/code/alexisbcook/data-leakage
  - https://arxiv.org/abs/2207.07048
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Target proxies in IDs, text and metadata

Models exploit any signal correlated with the label, including ones that only exist because of how data was collected (shortcut learning, Geirhos et al. 2020). They score well offline and fail in production.

## Where proxies hide
| Place | Example |
|---|---|
| IDs and sequence numbers | case IDs assigned in batches per outcome; positives inserted later get higher IDs |
| Timestamps | positives collected in a specific campaign/month |
| Free text | notes written after the outcome ("refund issued", "patient deceased"), template phrases per outcome |
| File metadata | image scanner model or hospital site differs between classes; EXIF, resolution, file size, filename ("tumor_001.png") |
| Image artefacts | rulers in malignant skin lesion photos, hospital tokens in X-rays, watermarks |
| Data source | positives from one database, negatives from another (different missingness, formats) |
| Row duplication | same entity repeated with the label in neighbouring rows |
| Engineered feature | count of follow-up records (only exist if positive) |

## Audits
1. **Importance review**: any ID, timestamp, source, file property, or text token with high importance is suspect until explained.
2. **Single-feature models**: train a model on each suspicious field alone; AUC well above chance for an ID or file size is a red flag.
3. **Text**: list top tokens/n-grams per class from a linear model; read samples containing them. Mask outcome-revealing phrases or restrict to text written before the decision time.
4. **Images**: saliency/Grad-CAM to see where the model looks; train on crops excluding the object; check performance per site/device.
5. **Provenance**: ask how positives and negatives were collected; if different processes, expect proxies.
6. **Cross-source validation**: test on data from a different site/time/collection; proxy-reliant models collapse.

## Fixes
- Drop pure identifiers and collection metadata from features.
- Restrict text to fields and timestamps before the prediction moment.
- Harmonise preprocessing across sources (resize, normalise, strip metadata, crop artefacts).
- Collect negatives through the same process as positives.
- Group-aware splits (by patient, device, site) so proxies tied to groups cannot transfer from train to test.

## Verify
After fixes, the drop in offline score is expected; the model is now measuring the real signal. Confirm with an external or prospective test set.
