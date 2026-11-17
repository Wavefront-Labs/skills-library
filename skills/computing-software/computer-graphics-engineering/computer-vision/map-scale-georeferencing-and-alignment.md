---
id: computing-software.computer-graphics-engineering.computer-vision.map-scale-georeferencing-and-alignment
name: map-scale-georeferencing-and-alignment
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, sfm-slam, georeferencing, sim3-alignment, umeyama, model-aligner, map-merging]
level: practitioner
status: verified
description: "Fix scale and georeference SfM/SLAM maps: Umeyama Sim(3) to GPS or control points, COLMAP model_aligner, ECEF/ENU/UTM frames, and merging separately built maps."
sources: ["https://colmap.github.io/faq.html", "https://doi.org/10.1109/34.88573", "https://github.com/MichaelGrupp/evo"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map scale, georeferencing and alignment

Monocular SfM/SLAM is defined up to a similarity transform (7 DOF: rotation, translation, scale).
Fixing that needs external references.

## Umeyama Sim(3)
```python
def umeyama(src, dst, with_scale=True):     # src, dst: (N,3) corresponding points
    mu_s, mu_d = src.mean(0), dst.mean(0)
    S, D = src - mu_s, dst - mu_d
    U, sig, Vt = np.linalg.svd(D.T @ S / len(src))
    E = np.eye(3); E[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ E @ Vt
    s = (sig * np.diag(E)).sum() / S.var(0).sum() if with_scale else 1.0
    t = mu_d - s * R @ mu_s
    return s, R, t                          # dst ~= s R src + t
```
Use camera centres vs GPS positions, or reconstructed control points vs surveyed GCPs. Wrap in
RANSAC when GPS is noisy (phone GPS error is typically several metres). The function was checked on a random Sim(3) (scale 2.7): scale, R and t recovered to 1e-15, det(R) = 1, also for planar points and with noise (scale 2.701 from sigma 0.1); fed a mirrored target it still returns a proper rotation (det +1), so the residual is large and should be checked.

## COLMAP
```bash
colmap model_aligner --input_path sparse/0 --output_path sparse/geo \
  --ref_images_path gps_enu.txt --ref_is_gps 0 --alignment_type custom \
  --alignment_max_error 3.0
```
`ref_is_gps 1` takes lat/lon/alt and converts it to ECEF, or to ENU with the first coordinate as origin when `--alignment_type enu`. Valid `alignment_type` values in the COLMAP source: `plane`, `ecef`, `enu`, `enu-plane`, `enu-plane-unscaled`, `custom`; `--alignment_max_error` is the RANSAC threshold (units of the reference coordinates).

## Coordinate frames
- Do not fit in lat/lon degrees. Convert to ECEF (global, large numbers) or a local ENU/UTM frame
  (metres, small numbers, float-friendly). `pyproj` for conversions.
- Keep a documented origin for ENU; store float64.

## Scale only
Measure one known distance (or use a scale bar/ArUco board of known size) and scale the
reconstruction: `colmap model_transformer` with a similarity, or scale camera centres and points.

## Merging maps
Find common images/landmarks, estimate Sim(3) with RANSAC, then run a joint bundle adjustment
(`colmap model_merger` + `bundle_adjuster`; both exist in the COLMAP command list) to remove seams.

## Verify
Residuals at held-out check points (not used in the fit): report RMSE in metres.

## Checked
NumPy 2.5.4, SciPy 1.18.1, pyproj 3.8.0.
- Run: `umeyama` on synthetic Sim(3) data (exact, noisy, planar, mirrored); `pyproj.Transformer` EPSG:4979 to EPSG:4978 (WGS84 geodetic to ECEF) returned metres-scale ECEF values.
- Fetched: COLMAP `src/colmap/exe/model.cc` (model_aligner options and documented alignment types, GPS conversion rule, model_transformer needs `transform_path`) and `colmap.cc` (model_merger, bundle_adjuster registered), COLMAP FAQ (geo-registration example). COLMAP itself was not run.
