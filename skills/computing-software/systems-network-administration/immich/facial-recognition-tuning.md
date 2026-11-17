---
id: computing-software.systems-network-administration.immich.facial-recognition-tuning
name: facial-recognition-tuning
category: computing-software
field: systems-network-administration
product: immich
tags: [facial-recognition, dbscan, recognition-distance, detection-score, core-point]
level: advanced
status: docs-checked
description: "Understand Immich's DBSCAN-derived face clustering and tune model, detection score, recognition distance and minimum recognized faces."
sources:
  - https://docs.immich.app/features/facial-recognition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: adjust face grouping with an understanding of how it works.

Face detection sends the generated preview image to the machine learning service, which downloads the model if needed. Facial recognition then clusters detected faces into people with an algorithm derived from DBSCAN. For each face it finds others within a distance threshold. If an already-named person is near, the face joins the person of the most similar face. If none, the face is a core point when enough similar faces exist (default 3, including itself), which creates a new person. Otherwise the face waits until all other faces are processed, then gets reconsidered. A nightly job also recognises unassigned faces with matches.

Unlike DBSCAN, it clusters incrementally, so results depend on queue size. It waits for detection and thumbnails to finish because larger queues cluster better. Re-running recognition for all assets behaves like DBSCAN.

Settings: Administration, Settings, Machine Learning Settings, Facial Recognition.

- Model: the default is usually best; pick a smaller one for constrained hardware.
- Minimum detection score: low values add false positives. A change only applies to new detection jobs, so rerun face detection for all assets.
- Maximum recognition distance: lower it for twins or similar-looking people.
- Minimum recognized faces: people with fewer faces are hidden immediately. Raise it if you raise distance or lower the score. Setting 1 removes core points for a manual workflow.

Change settings in small steps.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/facial-recognition in full (How Face Detection Works, How Facial Recognition Works, Configuration).
Removed: nothing.
Method: documentation only; no commands were run.
