---
id: computing-software.computer-graphics-engineering.opencv.opencv-parallel-for-and-threading
name: opencv-parallel-for-and-threading
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-core, parallel-for, setnumthreads, threading, tbb]
level: advanced
status: docs-checked
description: "Parallelise per-pixel or per-row work with cv::parallel_for_, and control OpenCV's internal thread pool with setNumThreads in multithreaded apps."
sources: ["https://docs.opencv.org/4.x/d7/dff/tutorial_how_to_use_OpenCV_parallel_for_new.html", "https://docs.opencv.org/4.x/db/de0/group__core__utils.html", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/core/include/opencv2/core/utility.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/core/how_to_use_OpenCV_parallel_for_new/how_to_use_OpenCV_parallel_for_new.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cv::parallel_for_ and thread control

## 1. parallel_for_
Signature (utility.hpp): `parallel_for_(const Range& range, const ParallelLoopBody& body, double nstripes=-1.)`, with a `std::function<void(const Range&)>` overload so a lambda works.
```cpp
cv::parallel_for_(cv::Range(0, img.rows), [&](const cv::Range& r) {
    for (int y = r.start; y < r.end; ++y) {
        const uchar* src = img.ptr<uchar>(y);
        uchar* dst = out.ptr<uchar>(y);
        for (int x = 0; x < img.cols; ++x) dst[x] = lut[src[x]];
    }
});
```
- The range passed to your functor is the subset one thread handles; the framework decides how to split the work. The tutorial shows two splits: over every pixel (recover row and column from the index) or over rows.
- Safe pattern: algorithms where only one thread writes any given output location (the tutorial's convolution: threads may read overlapping input but each writes its own pixels). Algorithms where several threads append to one shared structure (contours, feature lists) race and need per-thread storage or another strategy.
- Needs an OpenCV build with a parallel framework. The tutorial lists (OpenCV 4.5, in this order): Intel TBB, OpenMP (both explicitly enabled at build), Apple GCD, Windows RT concurrency, Windows concurrency, pthreads.

## 2. Thread control
```cpp
cv::setNumThreads(4);    // OpenCV will try to use 4 threads for later parallel regions
cv::setNumThreads(1);    // disables threading optimisations: functions run sequentially
cv::setNumThreads(-1);   // negative resets to the system default
int n = cv::getNumThreads();   // always 1 if built without threading support
```
- Header notes: the function is not thread-safe and must not be called inside a parallel region or from concurrent threads; behaviour differs by framework (for example with GCD only values <= 0 are supported, and getNumThreads returns 512 there).
- Python: `cv2.setNumThreads(n)` / `cv2.getNumThreads()` are exposed (declared with `CV_EXPORTS_W`).

## 3. When to turn it off
- If your app already parallelises (a worker per camera, a thread pool, multiprocessing workers), OpenCV's own threads can oversubscribe cores; set the count low at worker start. (Practitioner guidance.)

## Gotchas
- `setNumThreads` is a global setting and not thread-safe; set it once at startup.
- The header's own example of parallel_for_ use is `Mat_::forEach`, which wraps per-row work in a ParallelLoopBody.

## Verify
- [ ] Benchmark with `cv::TickMeter` across thread counts.
- [ ] CPU usage matches the expected core count.

## Checked
Method: docs-checked 2026-11-09 against utility.hpp (4.x branch) and the parallel_for_ tutorial markdown, both from raw GitHub; docs.opencv.org pages were not readable.
Removed as unconfirmed: that `setNumThreads(0)` means sequential (the header says 1 disables threading and negative resets to default), `cv::currentParallelFramework()`, the `OPENCV_FOR_THREADS_NUM` environment variable, the `img.rows / 64.0` stripes hint, the 100k-pixel small-image threshold, and the `setUseOptimized(false)` note.
