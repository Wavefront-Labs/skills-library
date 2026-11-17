---
id: computing-software.software-engineering.mobile-development.vision-camera-v5-and-frame-processing
name: vision-camera-v5-and-frame-processing
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, vision-camera, react-native-vision-camera, camera, photo-capture, video-recording, frame-output, frame-processors, barcode-scanning, qr-scanning, usecameradevice, camera-permissions, constraints-api, mobile-camera, realtime-vision]
level: advanced
status: draft
description: "Capture photos, video and frames with VisionCamera V5: device selection, the Constraints API, output hooks (usePhotoOutput, useVideoOutput, useFrameOutput) and the Recorder."
sources: ["https://github.com/margelo/react-native-vision-camera", "https://visioncamera.margelo.com/llms.txt", "https://visioncamera.margelo.com/docs/frame-output", "https://github.com/margelo/react-native-vision-camera-v4-snapshot"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VisionCamera V5: capture and frame processing

**Goal:** drive the device camera in React Native for photo/video capture, barcode scanning, and
realtime frame analysis, using the V5 architecture.

**Check your major version first.** V4 is no longer maintained and is archived as a separate
snapshot repo with its own docs site. V5 restructured the API around output hooks, so most V3/V4
material on the internet is now wrong:

| V3/V4 | V5 |
|---|---|
| `photo` / `video` props on `Camera` | `usePhotoOutput` / `useVideoOutput` hooks |
| `frameProcessor` prop | `useFrameOutput` / `CameraFrameOutput` |
| `codeScanner` prop | `react-native-vision-camera-barcode-scanner` package |
| `format` prop from `useCameraFormat` | **Constraints API** (`FPSConstraint`, `PhotoHDRConstraint`, ...) |
| `takePhoto()` | `capturePhoto(...)` / `capturePhotoToFile(...)` |
| `startRecording()` | `Recorder.startRecording(...)` |

```bash
npm i react-native-vision-camera
cd ios && pod install
```

## Permissions
```tsx
const { hasPermission, requestPermission } = useCameraPermission();
const { hasPermission: mic } = useMicrophonePermission();
```
Request early and gate the UI on the result; a `<Camera />` mounted without permission shows
nothing useful. Platform permission strings are still configured in `Info.plist` and the Android
manifest.

## Devices and the camera view
```tsx
import { Camera } from 'react-native-vision-camera';

<Camera style={StyleSheet.absoluteFill} device="back" isActive={true} />
```
`device` accepts a plain position string or a `CameraDeviceOrPosition`. For real device selection
use `useCameraDevice` (best match for a filter, or the default device at a position),
`useCameraDevices` for the full list, plus `getDefaultCameraDevice` / `getAllCameraDevices` and
`addOnCameraDevicesChangedListener` for hot-plugging (external lenses, USB cameras). `isActive`
controls the session lifecycle - set it `false` when the screen loses focus so the sensor shuts
down.

## Formats became Constraints
Instead of picking a `format` object, express requirements as typed constraints:
`FPSConstraint`, `PhotoHDRConstraint`, `VideoDynamicRangeConstraint`, `PixelFormatConstraint`,
`VideoStabilizationModeConstraint`, `ResolutionBiasConstraint`, `BinnedConstraint`,
`PreviewStabilizationModeConstraint`. Sorting filters select the device that satisfies them.
Declare what you need, not a resolution you found by trial on one phone.

## Photos
```tsx
const photoOutput = usePhotoOutput(...);       // in-memory or file capture
photoOutput.capturePhoto(CapturePhotoSettings, CapturePhotoCallbacks);
photoOutput.capturePhotoToFile(...);           // straight to a PhotoFile
```

## Video
```tsx
const videoOutput = useVideoOutput(...);       // records to file, optionally with audio
videoOutput.recorder.startRecording(RecorderSettings, { onRecordingFinished });
```
The `Recorder` supports start, pause, resume and stop, and reports why it finished via
`RecordingFinishedReason` - check that reason rather than assuming a stop was user-initiated, since
interrupting calls and backgrounding also end recordings.

## Frame output (formerly frame processors)
`useFrameOutput` / `CameraFrameOutput` stream frames synchronously. Heavy work belongs in an
`AsyncRunner` (`useAsyncRunner` / `createAsyncRunner`) which runs on a separate non-blocking
thread, with the worklet machinery in `react-native-vision-camera-worklets`
(`createRuntimeThreadProvider`, `createWorkletRuntimeForThread`). Drawing overlays, filters or
shapes on frames is the Skia frame processor path; native speed comes from a native Frame
Processor Plugin.

A synchronous frame handler that does model inference will drop frames - that is what
`AsyncRunner` exists for.

## Barcode scanning
Install the MLKit-based `react-native-vision-camera-barcode-scanner` package:
`BarcodeScanner`, `useBarcodeScanner`, `useBarcodeScannerOutput`, `createBarcodeScanner(Output)`,
with `BarcodeScannerOptions` / `TargetBarcodeFormat` to restrict formats and
`BarcodeScannerOutputResolution` to trade detail for speed. There is also a ready-made
`<CodeScanner />` view that uses the default rear camera. On iOS, `useObjectOutput` /
`CameraObjectOutput` is the native alternative, yielding `ScannedObject`, `ScannedFace` and
`ScannedCode` (test with `isScannedCode` / `isScannedFace`).

Zoom is a gesture controller, not a prop: `ZoomGestureController` provides native pinch-to-zoom
and can drive a `CameraController`'s zoom.

## Failure modes
- **Code from a V4 tutorial does nothing** - the props it sets do not exist in V5. Check the
  version in `package.json` against the docs site for that major.
- **Camera shows black** - permissions not granted, or `isActive` false; also check the device is
  not already claimed by another session.
- **Recording stops unexpectedly** - read `RecordingFinishedReason` before treating it as a bug;
  call interruptions end recordings legitimately.
- **Frame processing starves the UI** - inference running synchronously in the frame handler
  instead of an `AsyncRunner`.
- **Barcode scanning drains battery** - unrestricted formats and maximum output resolution;
  narrow `TargetBarcodeFormat` and lower the output resolution.
- **Works in dev, fails in release** - microphone permission only requested for video, or the
  release build's permission strings missing.

## Verify
- [ ] Permission flow tested from a cold install on a real device, including a denial then grant.
- [ ] `isActive` goes false when the screen loses focus, and the sensor indicator confirms it.
- [ ] Constraints state the actual requirements, and the chosen device satisfies them on the
      lowest-end phone you support.
- [ ] Recordings that end for non-user reasons are handled via `RecordingFinishedReason`.
- [ ] Frame work runs in an `AsyncRunner`, and dropped-frame counts stay flat under load.
- [ ] The installed major version's docs match the API being used.

*V5 hook, constraint and method names checked against the official llms.txt index on 2026-10-31;
not executed here, so `status: draft`.*
