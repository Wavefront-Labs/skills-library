---
id: computing-software.software-engineering.mobile-development.camera-capture-camerax-and-avfoundation
name: camera-capture-camerax-and-avfoundation
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, camerax, avfoundation, camera, image-analysis, barcode-scanning, video-recording, photo-picker, permissions]
level: advanced
status: docs-checked
description: "Build Android camera features with CameraX (Preview, ImageCapture, ImageAnalysis, VideoCapture), its analysis backpressure modes, and the Android photo picker."
sources: ["https://developer.android.com/media/camera/camerax", "https://developer.android.com/media/camera/camerax/analyze", "https://developer.android.com/training/data-storage/shared/photopicker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camera and media capture (CameraX, Android photo picker)

**Goal:** reliable photo, video and frame-analysis features across many Android device models, with correct lifecycle handling. The iOS AVFoundation half of this skill was removed because Apple's documentation could not be read; check Apple's capture-setup documentation directly.

## Do you need a custom camera?
- Just pick an existing photo or video: the **photo picker** gives a safe, built-in way to grant access to only selected images and videos instead of the whole library. Use the Jetpack Activity contracts (`androidx.activity` 1.7.0 or higher): `PickVisualMedia` for one item, `PickMultipleVisualMedia` for several. If the picker is unavailable the library falls back to `ACTION_OPEN_DOCUMENT` (Android 4.4, API 19 or higher); `isPhotoPickerAvailable()` tells you which.
- Media types: `PickVisualMedia.ImageAndVideo`, `ImageOnly`, `VideoOnly`, or `SingleMimeType("image/gif")` wrapped in `PickVisualMediaRequest(...)`. The callback receives a `uri`, null when nothing was selected.
- Custom camera (scanning, branded capture, continuous analysis): CameraX.

## CameraX
CameraX is a Jetpack library recommended for new apps. It supports Android 5.0 (API level 21) and higher. Use cases:
- Preview: view an image on the display.
- Image analysis: access a buffer for your algorithms, for example ML Kit.
- Image capture: save images.
- Video capture: save video and audio.

An optional Extensions API exposes bokeh (portrait), HDR, night mode and face retouching, all of which require device support.

## ImageAnalysis
The use case gives the app a CPU-accessible image; you implement `analyze()` (via `ImageAnalysis.Analyzer`), which runs on each frame.
```kotlin
val imageAnalysis = ImageAnalysis.Builder()
    // .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_RGBA_8888) // if RGBA is needed
    .setTargetResolution(Size(1280, 720))
    .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
    .build()
imageAnalysis.setAnalyzer(executor, ImageAnalysis.Analyzer { imageProxy ->
    val rotationDegrees = imageProxy.imageInfo.rotationDegrees
    // analyse here
    imageProxy.close()   // release the ImageProxy
})
cameraProvider.bindToLifecycle(this as LifecycleOwner, cameraSelector, imageAnalysis, preview)
```
- Output format: `YUV_420_888` (default) or `RGBA_8888` via `setOutputImageFormat`. Set either resolution or aspect ratio, not both. Other builder options: rotation, target name (debugging), background executor, queue depth, backpressure strategy.
- Backpressure: non-blocking (default, `STRATEGY_KEEP_ONLY_LATEST`) keeps only the newest frame, like a queue of depth one, and `setImageQueueDepth()` has no effect. Blocking (`STRATEGY_BLOCK_PRODUCER`) queues images and drops frames only when the queue is full, and it blocks all use cases bound to the camera, so preview is blocked while images are processed.
- Choosing a mode: for a fast analyzer (under a frame duration, for example 16 ms at 60 fps) either works; a slow but throughput-capable analyzer needs blocking mode with a longer queue; an analyzer that cannot keep up suits non-blocking, so other use cases still see all frames.
- Always release the `ImageProxy` with `ImageProxy.close()`; do not call `close()` on the wrapped `Media.Image`.
- Only one analyzer is active; `setAnalyzer()` replaces it. Stop with `clearAnalyzer()` or by unbinding.
- Bind with `ProcessCameraProvider.bindToLifecycle()`; it returns the `Camera` for adjusting settings such as exposure.
- ML Kit integrates through the ML Kit Analyzer described in the CameraX docs.

## Verify
- [ ] Every analyzer path calls `ImageProxy.close()`.
- [ ] The backpressure strategy matches the analyzer's speed, and preview is not stalled by blocking mode.
- [ ] Photo picker returns a null `uri` handled as "nothing selected".

## Checked
Date: 2026-11-08. Confirmed against the CameraX overview, CameraX Image analysis guide and Android photo picker guide: use cases, API 21 support, extensions list, analysis builder options, formats, backpressure modes and effects, close rules, single analyzer, bindToLifecycle, picker contracts, androidx.activity 1.7.0, fallback and request types. Removed all AVFoundation content (Apple pages returned no text), plus unconfirmed CameraX details: Compose CameraXViewfinder, VideoCapture Recorder/QualitySelector, RECORD_AUDIO, takePicture and targetRotation usage, and ImageCapture settings.
Method: documentation only; no commands were run.
