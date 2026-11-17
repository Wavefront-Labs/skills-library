---
id: computing-software.web-development.frontend-development.webtransport-and-webrtc-datachannels
name: webtransport-and-webrtc-datachannels
category: computing-software
field: web-development
product: frontend-development
tags: [webtransport, webrtc-datachannel, http3, unreliable-transport, realtime-networking]
level: advanced
status: docs-checked
description: "Low-latency browser transport beyond WebSockets: WebTransport over HTTP/3 (datagrams, streams, dev certificates) and WebRTC data channels with unordered delivery."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/WebTransport_API
  - https://developer.chrome.com/docs/capabilities/web-apis/webtransport
  - https://developer.mozilla.org/en-US/docs/Web/API/RTCDataChannel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebTransport and WebRTC data channels

WebSocket runs on TCP: one lost packet stalls everything behind it (head-of-line blocking). For game state, live cursors or media control where stale data is worthless, use unreliable/unordered transport.

## 1. WebTransport (client-server, HTTP/3)
```js
const wt = new WebTransport("https://rt.example.com:4433/game");
await wt.ready;
// unreliable datagrams
const w = wt.datagrams.writable.getWriter();
w.write(new Uint8Array([1, 2, 3]));
for await (const msg of wt.datagrams.readable) handle(msg);
// reliable bidirectional stream
const { readable, writable } = await wt.createBidirectionalStream();
wt.closed.then(() => reconnect()).catch(err => reconnect(err));
```
- The server must speak HTTP/3 and WebTransport: the client sends an extended `CONNECT` request with a `:protocol` pseudo-header identifying WebTransport (MDN). Check that your reverse proxy or CDN supports it before relying on it. The URL scheme must be HTTPS.
- Local dev with self-signed certs: `new WebTransport(url, { serverCertificateHashes: [{ algorithm: "sha-256", value: hashBytes }] })`; MDN says the certificate must be X.509v3 with a validity period of less than 2 weeks, must not use RSA keys, and that ECDSA with secp256r1 is the interoperable choice. The option works only with dedicated connections (`allowPooling` false).
- MDN browser-compat-data (checked 2026-10-26): Chrome 97, Firefox 114, Safari 26.4. Feature-detect and keep a WebSocket fallback for older browsers.
- Datagram size is limited; read `wt.datagrams.maxDatagramSize` and keep messages below it.

## 2. WebRTC data channels (peer-to-peer)
```js
const pc = new RTCPeerConnection({ iceServers: [{ urls: "stun:stun.example.com:3478" }] });   // your STUN/TURN servers
const ch = pc.createDataChannel("state", { ordered: false, maxRetransmits: 0 });
ch.binaryType = "arraybuffer";
ch.onmessage = e => apply(e.data);
// exchange offer/answer + ICE candidates over your own signalling (WebSocket/HTTP)
```
- Needs your own signalling, and a TURN server for peers that cannot connect directly.
- `ordered` defaults to `true`; `ordered: false` with `maxRetransmits: 0` gives unreliable, unordered delivery. Specifying both `maxPacketLifeTime` and `maxRetransmits` throws an error.
- Monitor `ch.bufferedAmount` and `bufferedAmountLowThreshold` for backpressure.

## 3. Choosing
| Need | Choose |
|---|---|
| Server push, broad support | WebSocket / SSE |
| Client-server, low latency, can run HTTP/3 | WebTransport |
| Peer-to-peer or alongside audio/video | WebRTC data channel |

## Verify
- [ ] With simulated packet loss (an OS network conditioner), updates keep flowing without multi-second stalls.

## Checked

Checked 2026-10-26 against MDN WebTransport API, WebTransport() constructor, WebTransportDatagramDuplexStream.maxDatagramSize, RTCPeerConnection.createDataChannel() and RTCDataChannel (mdn/content main) and MDN browser-compat-data (api/WebTransport.json): HTTP/3 and extended CONNECT, `serverCertificateHashes` rules (under 2 weeks validity, no RSA, ECDSA secp256r1, sha-256 only, dedicated connections), data-channel `ordered` default and `maxRetransmits`/`maxPacketLifeTime` exclusivity, and support versions. Corrected '14 days' to 'under 2 weeks'. Removed the library list, the ~1200-byte datagram figure, the 10-20% TURN figure and the 'all browsers' claim.

Method: documentation only; no commands were run.
