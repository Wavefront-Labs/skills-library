---
id: computing-software.computer-graphics-engineering.opencv.opencv-js-browser
name: opencv-js-browser
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-build-deploy, opencv-js, webassembly, emscripten, browser, javascript]
level: practitioner
status: docs-checked
description: "Use OpenCV.js in the browser: loading the WASM build, cv.Mat memory management with delete(), canvas/video IO, building a custom smaller opencv.js with emscripten."
sources: ["https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html", "https://docs.opencv.org/4.x/d4/da1/tutorial_js_setup.html", "https://docs.opencv.org/4.x/dd/d00/tutorial_js_video_display.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV.js build and browser use

## Load
See the OpenCV.js setup tutorial for how to include `opencv.js` and wait until it is ready before calling `cv` functions.

## Memory: you must delete
Mats created from JavaScript live in the WebAssembly heap: call `.delete()` on them when done (the video tutorial says to delete `src` and `dst` when you stop).

## Video
```javascript
let cap = new cv.VideoCapture(videoElement);   // video source element
let frame = new cv.Mat(video.height, video.width, cv.CV_8UC4);
function loop() { cap.read(frame); /* process */ requestAnimationFrame(loop); }
```
The tutorial builds the Mat as `cv.CV_8UC4` with the same size as the video, for performance.

## Custom build
The setup tutorial builds OpenCV.js from source with Emscripten: run `<opencv_src_dir>/platforms/js/build_js.py <build_dir>`. It builds the WebAssembly version by default (`--build_wasm`). See that page for the SIMD and threaded variants and for trimming the exported function list.

## Verify
Monitor `performance.memory`/heap size over a minute of processing: it must stay flat.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 OpenCV.js tutorials (root, setup/build, video display).
- Confirmed: `cv.VideoCapture(videoSource)`, `cv.CV_8UC4` Mat matching the video size, deleting `src`/`dst`, `build_js.py` with WebAssembly as the default build, Emscripten requirement.
- Removed: load snippet and Promise behaviour, imread/imshow memory sample, MatVector/KeyPointVector claims, the exact emcmake command with `--simd --threads --config`, size figures, COOP/COEP requirement, the CORS, exported-function and Web Worker gotchas (none appear on the fetched pages).

Method: documentation only; no commands were run.
