---
id: computing-software.computer-graphics-engineering.rendering-techniques.nearest-neighbour-search-nanoflann-faiss
name: nearest-neighbour-search-nanoflann-faiss
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, spatial-structures, nanoflann, nearest-neighbor-search, kd-tree, faiss, knn, point-clouds]
level: practitioner
status: docs-checked
description: "Run nearest-neighbour searches on point sets: kd-trees with nanoflann, radius and kNN queries, approximate methods with FAISS on CPU/GPU, and choosing exact vs approximate."
sources: ["https://github.com/jlblancoc/nanoflann", "https://github.com/jlblancoc/nanoflann/blob/master/include/nanoflann.hpp", "https://github.com/facebookresearch/faiss", "https://github.com/facebookresearch/faiss/blob/main/faiss/IndexIVFPQ.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nearest-neighbour search (nanoflann, FAISS)

## 1. Low-dimensional (2D/3D) exact: kd-trees
**nanoflann** (header-only C++, BSD) - fast kd-tree for point clouds:
```cpp
#include <nanoflann.hpp>
struct Cloud { std::vector<std::array<float,3>> pts;
  size_t kdtree_get_point_count() const { return pts.size(); }
  float kdtree_get_pt(size_t i, size_t d) const { return pts[i][d]; }
  template <class B> bool kdtree_get_bbox(B&) const { return false; } };
using KD = nanoflann::KDTreeSingleIndexAdaptor<nanoflann::L2_Simple_Adaptor<float, Cloud>, Cloud, 3>;
KD index(3, cloud, nanoflann::KDTreeSingleIndexAdaptorParams(10 /*leaf size*/));
// kNN
uint32_t idx[8]; float d2[8];   // default index type is uint32_t
index.knnSearch(query, 8, idx, d2);
// radius (squared radius for L2)
std::vector<nanoflann::ResultItem<uint32_t, float>> matches;
index.radiusSearch(query, r * r, matches);
```
Note: L2 adaptors use **squared** distances for the radius and all returned distances. `leaf_max_size` (default 10) trades build vs query
speed; the README suggests 10-50 when queries dominate.
`KDTreeSingleIndexDynamicAdaptor` supports insertions.

## 2. High-dimensional or huge: FAISS
For embeddings and feature descriptors (high-dimensional vectors) use FAISS (Meta; library of similarity search over dense vectors, with Python wrappers and GPU indexes):
```python
import faiss, numpy as np
d = 128; xb = np.random.rand(1_000_000, d).astype('float32')
index = faiss.IndexFlatL2(d)                 # exact brute force (GpuIndexFlatL2 is the GPU counterpart)
index.add(xb); D, I = index.search(xq, 10)
quant = faiss.IndexFlatL2(d)
ivf = faiss.IndexIVFPQ(quant, d, 4096, 16, 8)   # (quantizer, d, nlist, M, nbits_per_idx)
ivf.train(xb); ivf.add(xb); ivf.nprobe = 16; D, I = ivf.search(xq, 10)
hnsw = faiss.IndexHNSWFlat(d, 32)            # (d, M) graph-based approximate index
```
Tune `nprobe` (default 1) and the HNSW `efSearch` (default 16) for the recall-speed trade-off; measure recall@k against `IndexFlatL2`.

## 3. Graphics uses
Normal estimation and point cloud processing (kNN), photon mapping density estimation (radius),
ICP registration, SPH neighbour finding (often uniform grids instead), descriptor matching (FAISS).

## 4. Choosing
| Data | Use |
|---|---|
| 2D/3D static points | nanoflann / cKDTree |
| 3D dynamic particles, fixed radius | uniform grid / spatial hash |
| high-dimensional vectors, millions of points | FAISS (IVF/HNSW), approximate |

## Gotchas
- Mixing squared and unsquared radii is the classic nanoflann bug.
- Approximate indexes need training data representative of queries.

## Verify
- [ ] Results match brute force exactly (kd-tree) or meet recall target (approximate).
- [ ] Query throughput measured at the target dataset size.

## Checked

2026-10-26: nanoflann.hpp and README (jlblancoc/nanoflann master) and FAISS headers (facebookresearch/faiss main, release v1.15.1 of 2026-09-16), read 2026-10-26. Confirmed: nanoflann is a BSD-licensed header-only fork of FLANN, the KDTreeSingleIndexAdaptor constructor (dimensionality, dataset, params), knnSearch and radiusSearch signatures, ResultItem, squared distances for L2, leaf_max_size default 10, KDTreeSingleIndexDynamicAdaptor, FAISS IndexFlatL2, IndexIVFPQ(quantizer, d, nlist, M, nbits_per_idx), IndexHNSWFlat(d, M), nprobe default 1, efSearch default 16. Wrong claim fixed: the default index type is uint32_t, so the size_t idx array in the example did not compile. Removed the SciPy/Open3D line, the 64-1024 dimension kd-tree claim and the 20-dimension threshold, which no documentation states.

Method: documentation only; no commands were run.
