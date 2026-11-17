---
id: computing-software.computer-graphics-engineering.graphics-math.rotation-averaging
name: rotation-averaging
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, rotations, rotation-averaging, quaternion-mean, markley-method, karcher-mean, sfm]
level: advanced
status: draft
description: "Average rotations properly: quaternion eigenvector (Markley) method, sign alignment, weighted means, chordal vs geodesic vs L1 means, and multiple rotation averaging in SfM."
sources: ["https://ntrs.nasa.gov/citations/20070017872", "https://users.cecs.anu.edu.au/~hartley/Papers/PDF/Hartley-Trumpf:Rotation-averaging:IJCV.pdf", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.mean.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Averaging rotations

Averaging Euler angles or raw quaternion components is wrong (wrap-around, double cover).

## Quaternion eigen method (Markley et al. 2007)
```python
def quat_mean(Q, w=None):                 # Q: (N,4) unit quaternions
    w = np.ones(len(Q)) if w is None else w
    M = (w[:, None, None] * Q[:, :, None] * Q[:, None, :]).sum(0)
    vals, vecs = np.linalg.eigh(M)
    return vecs[:, -1]                    # eigenvector of largest eigenvalue
```
- Sign-invariant (q q^T is the same for -q), weighted, closed form.
- Minimises the chordal (Frobenius) distance between rotation matrices; for clustered rotations it is
  almost identical to the geodesic mean.
- `scipy.spatial.transform.Rotation.mean(weights=...)` implements this.

## Quick approximation for close rotations
Flip each q to the hemisphere of the first (`if dot(q, q0) < 0: q = -q`), sum, normalise. Fine for
smoothing a jittery tracker; breaks for widely spread rotations.

## Geodesic (Karcher) mean
Iterate: map each rotation to the tangent space at the current estimate (`log(R_est^T R_i)`), average,
map back with exp, repeat until the update is tiny. Use when exact geodesic statistics matter.

## Robust (L1) averaging
Weiszfeld-style iteration on the rotation manifold (Hartley et al.) resists outlier rotations; useful
for fusing noisy pose estimates.

## Multiple rotation averaging (SfM, pose graphs)
Given relative rotations R_ij between many cameras, solve for absolute R_i: chordal initialisation via
spectral/SVD relaxation, then robust IRLS refinement. Basis of global SfM (Theia, GLOMAP).

## Verify
Average of rotations symmetrically spread around a known rotation must return it; randomise signs of
the inputs: result unchanged.
