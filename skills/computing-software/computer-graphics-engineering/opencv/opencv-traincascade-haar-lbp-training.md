---
id: computing-software.computer-graphics-engineering.opencv.opencv-traincascade-haar-lbp-training
name: opencv-traincascade-haar-lbp-training
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-objdetect, cascade-training, opencv-traincascade, haar-cascade, lbp-cascade, opencv-createsamples]
level: advanced
status: docs-checked
description: "Train Haar/LBP cascades with opencv_createsamples, opencv_annotation and opencv_traincascade: sample files, key flags, stop value, and the 3.4-branch tool note."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/others/traincascade.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Training Haar/LBP cascades

The tutorial notes that `opencv_createsamples` and `opencv_traincascade` are disabled since OpenCV 4.0; use those apps from the 3.4 branch. The model format is the same between 3.4 and 4.x, so the trained XML loads with `CascadeClassifier`. Ignore tutorials that use the deprecated `opencv_haartraining`. Training can use TBB for multithreading if OpenCV was built with it.

## 1. Negatives
A text file (for example `bg.txt`) with one image path per line, absolute or relative. Each image must be at least as large as the training window, because windows are subsampled from it.

## 2. Positives
`opencv_createsamples` builds a binary `.vec` file two ways:
1. From one object image (`-img`, with `-bg`, `-num` and distortion flags `-maxxangle`, `-maxyangle`, `-maxzangle` in radians, `-bgcolor`, `-bgthresh`, `-inv`, `-randinv`, `-maxidev`): it perspective-distorts the object onto arbitrary backgrounds. This works for rigid objects such as logos and "tends to fail rather soon" for less rigid ones.
2. From annotated images (`-info file`): each line is `path count x y w h [x y w h ...]`. Boxes are cut out and resized to `-w` by `-h`; no distortion is applied and distortion flags are ignored.
```
opencv_createsamples -info info.dat -num 2000 -w 24 -h 24 -vec pos.vec
```
Examples: `img/img1.jpg  1  140 100 45 45`. `opencv_annotation --annotations=file.txt --images=folder/` builds the info file interactively (keys: `c` confirm, `d` delete last, `n` next image, ESC exit). Cover the real variety of the object class in the samples. Running createsamples with only `-vec`, `-w` and `-h` lets you inspect a vec file.

## 3. Train
```
opencv_traincascade -data out/ -vec pos.vec -bg bg.txt -numPos 1800 -numNeg 3600 -numStages 20 -w 24 -h 24 -featureType LBP -minHitRate 0.995 -maxFalseAlarmRate 0.5
```
- `-data` folder must exist beforehand. `-w` and `-h` must equal the values used in createsamples.
- `-numPos` and `-numNeg` are the counts used per stage. `-featureType` is `HAAR` (default) or `LBP`. LBP uses integer precision, so training and detection are several times faster; quality depends mainly on data and parameters, and an LBP model can come close to Haar quality.
- `-minHitRate` and `-maxFalseAlarmRate` are per stage; the overall rates are estimated as the value to the power of the number of stages.
- `-acceptanceRatioBreakValue`: guideline is not to train further than 10e-5 to avoid overtraining; the default -1 disables it.
- `-precalcValBufSize` and `-precalcIdxBufSize` (MB) speed training up but together must not exceed available memory. `-numThreads` caps threads.
- Other options: `-bt` (DAB, RAB, LB, GAB default), `-weightTrimRate` (0.95 suggested), `-maxDepth` (1 suggested), `-maxWeakCount`, Haar `-mode` (BASIC default, CORE, ALL), `-baseFormatSave` to save in the old format.
- Output is `cascade.xml` in the `-data` folder; the other files only serve interrupted training and may be deleted afterwards.

## 4. Visualise
`opencv_visualisation --image=object.png --model=model.xml --data=result/` renders features per stage; it handles only stump-based cascades from traincascade and needs an image of the original model window size.

## Checked
Method: docs-checked 2026-11-09 against the traincascade tutorial markdown (4.x), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: positive and negative count guidance, the numPos versus vec-count formula and the 85 to 90 percent rule, the "hours versus days" training time claim, "Haar is slightly more accurate", failure-sign diagnostics, the specific example flag values as recommendations (kept as an example only), detectMultiScale parameter advice, and the CNN-detectors-outperform note.
