---
id: computing-software.computer-graphics-engineering.computer-vision.colmap-structure-from-motion
name: colmap-structure-from-motion
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, sfm-slam, colmap, structure-from-motion, bundle-adjustment, glomap, sparse-reconstruction]
level: sme
status: draft
description: "Run sparse structure-from-motion with COLMAP: feature extraction, matcher choice, incremental vs GLOMAP global mapping, camera models, and diagnosing failures."
sources: ["https://colmap.github.io/tutorial.html", "https://colmap.github.io/cli.html", "https://colmap.github.io/faq.html", "https://github.com/colmap/glomap"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Structure from motion with COLMAP

## 1. CLI pipeline
```bash
colmap feature_extractor --database_path db.db --image_path images \
  --ImageReader.camera_model OPENCV --ImageReader.single_camera 1 \
  --SiftExtraction.max_num_features 8192
colmap exhaustive_matcher --database_path db.db          # < ~500 images
# colmap sequential_matcher --database_path db.db --SequentialMatching.overlap 15 --SequentialMatching.loop_detection 1   # video
# colmap vocab_tree_matcher --database_path db.db --VocabTreeMatching.vocab_tree_path vocab.bin                            # large unordered
mkdir -p sparse
colmap mapper --database_path db.db --image_path images --output_path sparse
# or global SfM, much faster on big sets: glomap mapper --database_path db.db --image_path images --output_path sparse
colmap model_analyzer --path sparse/0                    # registered images, points, mean reproj error
colmap model_converter --input_path sparse/0 --output_path sparse/0 --output_type TXT
```

## 2. Choices that matter
- **Camera model**: SIMPLE_RADIAL for unknown phone shots; OPENCV for wider lenses; OPENCV_FISHEYE for fisheye.
  `single_camera 1` when every image comes from one fixed-focal camera (big stability gain).
- Known intrinsics: set `--ImageReader.camera_params` and `--Mapper.ba_refine_focal_length 0`.
- GPU SIFT is used automatically when CUDA is available (`--SiftExtraction.use_gpu`).

## 3. Diagnosing
- Several models `sparse/0, 1, 2...`: the scene split into disconnected components; add bridging images or use
  a stronger matcher (exhaustive, or learned features via hloc).
- Few registered images: low overlap, textureless or repetitive surfaces, motion blur.
- Mean reprojection error should be about 0.5-1 px; much higher means wrong camera model or bad matches.
- Repetitive structures (facades, symmetric objects) cause "folded" reconstructions; check visually in the GUI
  (`colmap gui`) and use sequential/loop matching or masks.

## 4. Scale and georeference
SfM is up to scale. Use `model_aligner` with GPS/EXIF or known control points, or scale by a measured distance.

## Gotchas
- Mixing cameras/zoom with `single_camera 1` breaks calibration; use per-folder cameras.
- Rolling-shutter and heavy stabilisation (video) degrade accuracy.
- Undistort (`image_undistorter`) before MVS, NeRF or Gaussian splatting tools that expect PINHOLE.

## Verify
- [ ] model_analyzer: >95% images registered in one model, mean reprojection error under ~1 px, camera
  trajectory looks right in the GUI.
