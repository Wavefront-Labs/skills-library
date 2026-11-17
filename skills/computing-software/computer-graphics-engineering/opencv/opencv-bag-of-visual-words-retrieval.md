---
id: computing-software.computer-graphics-engineering.opencv.opencv-bag-of-visual-words-retrieval
name: opencv-bag-of-visual-words-retrieval
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-features2d, bag-of-visual-words, image-retrieval, vocabulary, kmeans]
level: advanced
status: docs-checked
description: "Build a bag-of-visual-words vocabulary and image histograms in OpenCV with BOWKMeansTrainer and BOWImgDescriptorExtractor, as documented in features2d.hpp."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/features2d/include/opencv2/features2d.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bag of visual words with OpenCV

## 1. Vocabulary
```python
sift = cv2.SIFT_create()
trainer = cv2.BOWKMeansTrainer(1000)       # clusterCount
for p in train_paths:
    _, d = sift.detectAndCompute(cv2.imread(p, 0), None)
    if d is not None:
        trainer.add(d)
vocab = trainer.cluster()                  # each row is a visual word (cluster centre)
```
- `BOWTrainer.add(descriptors)` adds a matrix whose rows are descriptors to the training set; `descriptorsCount()`, `getDescriptors()` and `clear()` exist.
- `cluster()` clusters the stored descriptors; `cluster(descriptors)` clusters the given ones without adding them to the stored set. The vocabulary is the cluster centres.
- `BOWKMeansTrainer(clusterCount, termcrit=TermCriteria(), attempts=3, flags=KMEANS_PP_CENTERS)` follows `cv::kmeans`.
- The base class cites "Visual Categorization with Bags of Keypoints" (Csurka et al., 2004).

## 2. Image histograms
```python
bow = cv2.BOWImgDescriptorExtractor(sift, cv2.FlannBasedMatcher())
bow.setVocabulary(vocab)
kps = sift.detect(img, None)
h = bow.compute(img, kps)
```
Per the header, `compute` finds the nearest visual word for each keypoint descriptor (using the given matcher) and returns a normalised histogram of word frequencies; the i-th bin is the frequency of the i-th vocabulary word. The extractor-less constructor takes only a matcher and is used with `compute(keypointDescriptors, imgDescriptor)`. `descriptorSize()` returns 0 until a vocabulary is set. `compute` is not const because `DescriptorMatcher::match` is not.

## Scope
This skill covers only the OpenCV classes. TF-IDF weighting, inverted indexes, vocabulary trees, geometric re-ranking and evaluation are outside what the cited header documents.

## Checked
Method: docs-checked 2026-11-09 against features2d.hpp (4.x, BOWTrainer, BOWKMeansTrainer and BOWImgDescriptorExtractor sections), raw GitHub; docs.opencv.org and the Sivic-Zisserman paper were not read.
Removed as unconfirmed: subsampling and MiniBatchKMeans advice, vocabulary-size ranges, domain-representative training advice, TF-IDF formula and stop-listing, inverted index, DBoW2/DBoW3/fbow and ORB-SLAM remark, RANSAC re-ranking thresholds, VLAD/Fisher/NetVLAD claims and the mAP evaluation notes.
