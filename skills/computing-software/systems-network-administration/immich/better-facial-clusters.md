---
id: computing-software.systems-network-administration.immich.better-facial-clusters
name: better-facial-clusters
category: computing-software
field: systems-network-administration
product: immich
tags: [face-clusters, reset-job, minimum-faces, missing-mode, large-library]
level: advanced
status: docs-checked
description: "Re-cluster faces in a large Immich library: raise minimum recognized faces, reset Facial Recognition, then lower the threshold with Missing runs."
sources:
  - https://docs.immich.app/guides/better-facial-clusters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: improve face clustering after importing many images so you need fewer manual merges.

Warning: this deletes all previously assigned person names. Take a database backup first. It suits large libraries right after a big import.

1. Administration, Settings, Machine Learning Settings:
   - Optionally lower Maximum recognition distance, for example to 0.4, if the library contains similar-looking people.
   - Set Minimum recognized faces high: 20 for roughly 100K+ assets, 10 for roughly 40K+.
   A high value means clusters only form from faces that appear at least that many times, giving cleaner seeds.

2. Administration, Job Queues: run FACIAL RECOGNITION, Reset. This rebuilds recognition using the new settings.

3. When the reset finishes, relax the threshold in steps:
   - Lower Minimum recognized faces to 10 (for medium libraries, from 10 to 5), then run FACIAL RECOGNITION in Missing mode.
   - Lower it again to 3, then run FACIAL RECOGNITION in Missing mode again.

Libraries of other sizes may behave better with different values. Try several values before you assign any names, and keep the one that produces the cleanest people.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading guides/better-facial-clusters in full.
Removed: the explanation of why Missing runs avoid noisy groups, which the page does not state.
Method: documentation only; no commands were run.
