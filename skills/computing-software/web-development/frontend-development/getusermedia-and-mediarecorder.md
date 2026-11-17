---
id: computing-software.web-development.frontend-development.getusermedia-and-mediarecorder
name: getusermedia-and-mediarecorder
category: computing-software
field: web-development
product: frontend-development
tags: [device-apis, getusermedia, mediarecorder, webrtc, camera, microphone]
level: practitioner
status: docs-checked
description: "Capturing camera and microphone with getUserMedia, choosing constraints, handling permission errors, recording with MediaRecorder, and releasing devices properly."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
  - https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder
  - https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/enumerateDevices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# getUserMedia and MediaRecorder

## 1. Capture
```js
let stream;
async function start() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      audio: { echoCancellation: true, noiseSuppression: true },
      video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
    });
    video.srcObject = stream;            // <video autoplay playsinline muted>
  } catch (e) { handle(e.name); }
}
```
Error names (MDN): `NotAllowedError` (user or setting denied access, insecure page, or a Permissions Policy that does not allow the device), `NotFoundError` (no matching track), `NotReadableError` (permission was granted but a hardware, OS, browser or page-level error blocked access), `OverconstrainedError` (the constraints cannot be met; prefer `ideal` over `exact`), `SecurityError` (user media support is disabled on the document), `TypeError` (empty constraints, or an insecure context where `navigator.mediaDevices` is undefined).

## 2. Device selection
`enumerateDevices()` lists only devices for which permission has been granted (plus default devices). Re-query on the `devicechange` event of `navigator.mediaDevices`. Select with `{ deviceId: { exact: id } }`.

## 3. Record
```js
const type = ["video/webm;codecs=vp9,opus", "video/webm", "video/mp4"].find(t => MediaRecorder.isTypeSupported(t));
const rec = new MediaRecorder(stream, { mimeType: type, videoBitsPerSecond: 2_500_000 });
const chunks = [];
rec.ondataavailable = e => e.data.size && chunks.push(e.data);
rec.onstop = () => upload(new Blob(chunks, { type }));
rec.start(1000);   // timeslice: emit a chunk every second (enables chunked upload)
```
Supported container and codec types differ per browser, so choose the type with `MediaRecorder.isTypeSupported()` rather than assuming one.

## 4. Release
```js
stream.getTracks().forEach(t => t.stop());   // turns off the camera light
```
Do this on stop and on route change. Leaving tracks running keeps the device in use.

## 5. UX and privacy
Explain before prompting; show a live preview and mute toggles (`track.enabled = false` makes the track render silence or black). Screen capture uses `getDisplayMedia()`, which requires transient user activation.

## Verify
Manually test the denied, no-device and device-in-use paths.

## Checked

Checked 2026-10-26 against MDN getUserMedia(), enumerateDevices(), the devicechange event, MediaRecorder() constructor and start(), MediaStreamTrack.enabled and getDisplayMedia() (mdn/content main). Wrong claim fixed: an insecure context or a Permissions Policy block gives `NotAllowedError` (or `TypeError` when `navigator.mediaDevices` is undefined), not `SecurityError`. `NotReadableError` is a hardware/OS/page error, not specifically 'in use'. Removed the unconfirmed Safari-MP4, WebM duration, Chrome test-flag and pagehide claims.

Method: documentation only; no commands were run.
