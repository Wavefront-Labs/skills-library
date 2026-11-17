---
id: computing-software.web-development.frontend-development.postmessage-and-transferable-objects
name: postmessage-and-transferable-objects
category: computing-software
field: web-development
product: frontend-development
tags: [web-workers, off-main-thread, transferable-objects, postmessage, structured-clone, arraybuffer-transfer, messagechannel]
level: practitioner
status: docs-checked
description: "Passing data to workers, iframes and windows efficiently: structured-clone costs, transferring ArrayBuffers, MessageChannel ports and origin checks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Worker/postMessage
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# postMessage and transferable objects

**Goal:** move data between threads/windows without needless copies and without trusting the wrong sender.

## 1. Structured clone
`postMessage` copies its argument with the structured clone algorithm. Functions and DOM nodes throw `DataCloneError`; the prototype chain is not duplicated (class instances arrive as plain objects), property descriptors, getters and setters are not copied, and symbols are not cloneable. Copying a large object graph takes main-thread time, so measure it.

## 2. Transfer instead of copy
```js
const buf = new Float32Array(10_000_000).buffer;
worker.postMessage({ buf }, [buf]);     // ownership moves; zero-copy
console.log(buf.byteLength);             // 0 - detached in the sender
```
Transferable (MDN list): `ArrayBuffer`, `MessagePort`, `ImageBitmap`, `OffscreenCanvas`, `ReadableStream`/`WritableStream`/`TransformStream`, `VideoFrame`, `AudioData`, `MediaStreamTrack`, `RTCDataChannel` and others. Transfer the underlying `.buffer` of a typed array. After transfer, reading or writing the detached data throws, though `byteLength` reads 0 - send it back when done.

## 3. MessageChannel for private lines
```js
const { port1, port2 } = new MessageChannel();
worker.postMessage({ type: 'connect' }, [port2]);
port1.onmessage = (e) => {};
```
Useful to connect two workers directly, or to give an iframe a dedicated channel after a handshake.

## 4. Window/iframe messaging security
```js
// sender: always specify the target origin
iframe.contentWindow.postMessage({ type: 'resize' }, 'https://widget.example.com');
// receiver: always check origin (and shape)
window.addEventListener('message', (e) => {
  if (e.origin !== 'https://app.example.com') return;
  if (e.data?.type !== 'resize') return;
});
```
MDN: always give a specific `targetOrigin` rather than `*` when you know where the recipient lives, since `*` can disclose data to a malicious site. Any listener receiving messages from other sites must verify the sender with `event.origin` (and possibly `event.source`) before acting; `data:` URLs have opaque origins and need `"*"`.

## Verify
- [ ] Performance panel shows no long "Serialize"/"Deserialize" for large payloads after switching to transfer.
- [ ] Sender's buffer is detached (byteLength 0) after transfer.
- [ ] Message handlers ignore messages from unexpected origins (test from the console of another site in an iframe).

## Checked

Checked 2026-10-26 against MDN Structured clone algorithm, Transferable objects and Window.postMessage() (mdn/content main): clone limits, the transferable list, detached-buffer behaviour (`byteLength` 0), the targetOrigin and origin-verification guidance. Removed the unconfirmed claim that a missing check is a 'common XSS/CSRF vector' and the ES-level claim that copying 100 MB takes a specific time.

Method: documentation only; no commands were run.
