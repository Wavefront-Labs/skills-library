---
id: computing-software.data-science-and-analytics.pandas-numpy.slicing-views-fancy-indexing
name: slicing-views-fancy-indexing
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [array-slicing-views, fancy-indexing, boolean-mask-numpy]
level: practitioner
status: docs-checked
description: "Distinguish views from copies, use boolean masks and integer-array indexing and avoid accidental mutation of shared memory."
sources:
  - https://numpy.org/doc/stable/user/basics.indexing.html
  - https://numpy.org/doc/stable/user/basics.copies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexing
```python
v = a[1:5]            # basic slice -> VIEW (shares memory)
c = a[[0, 2, 4]]      # integer-array indexing -> COPY
m = a[a > 3]          # boolean mask -> COPY
v[:] = 0              # modifies a!
v.base is a           # True for views; None for copies
```
## Gotchas
- Basic slicing always returns a view; advanced (integer-array or boolean) indexing always returns a copy.
- `base` is the original array for a view and `None` for a copy.
- Write `.copy()` when you want independence.
## Verify
- [ ] `v.base` is `a` for views and `None` for copies, as intended.

## Checked

Method: docs-checked 2026-11-09 against the NumPy indexing and copies-and-views user guides (read via text conversion). Dropped `np.shares_memory` and the repeated-index and `np.add.at` note, which those pages do not state.
