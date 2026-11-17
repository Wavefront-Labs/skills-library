---
id: computing-software.data-science-and-analytics.experiment-design.randomisation-and-assignment
name: randomisation-and-assignment
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [hash-bucketing, randomisation-unit, holdout-group]
level: practitioner
status: draft
description: "Assign units to variants with a stable salted hash, keep assignments sticky and handle exposure, holdouts and interference."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assignment
```python
import hashlib
def bucket(user_id, salt, n=1000):
    h = int(hashlib.sha256(f"{salt}:{user_id}".encode()).hexdigest(), 16)
    return h % n          # 0..n-1; split buckets into variants
```
- New salt per experiment to avoid carry-over correlation between experiments.
- Log assignment at the moment of exposure, and analyse only exposed units.
## Gotchas
- Network effects (marketplaces, social) violate independence; consider cluster or switchback designs.
- Re-randomising users mid-test destroys the comparison.
## Verify
- [ ] Bucket sizes match the intended split (see sample-ratio check).
