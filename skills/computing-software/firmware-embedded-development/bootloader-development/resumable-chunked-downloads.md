---
id: computing-software.firmware-embedded-development.bootloader-development.resumable-chunked-downloads
name: resumable-chunked-downloads
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [resumable-download, ab-update, http-range, download-progress, flash-write-pipeline, firmware-embedded-development]
level: advanced
status: draft
description: "Download firmware in chunks that resume after disconnects or resets: HTTP Range requests, persisted progress, erase-block writes to the inactive slot, final check."
sources:
  - https://www.rfc-editor.org/rfc/rfc9110#name-range-requests
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/esp_https_ota.html
  - https://docs.zephyrproject.org/latest/services/storage/stream/stream_flash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resumable chunked downloads

Cellular and battery devices lose connectivity mid-download. Restarting a 1 MB download from zero
each time can mean it never completes and burns data plans.

## Design
1. **Manifest first**: fetch metadata (version, size, SHA-256 or signature, URL). Store it.
2. **Download in chunks** (e.g. 4-16 KB) into the inactive slot, writing sequentially.
3. **Persist progress** (bytes written, manifest hash/ETag) in a small record after each erase
   block is fully written. Writing it per chunk wears flash; per erase block is enough.
4. **Resume**: on reconnect or reboot, if a stored progress record matches the same manifest,
   request from that offset:
```
GET /fw/acme-2.4.1.bin HTTP/1.1
Range: bytes=262144-
If-Range: "etag-from-first-response"
```
   Expect `206 Partial Content`; a `200` means the server ignored the range (or the file changed):
   restart from zero.
5. **Verify** the whole slot (hash/signature) after the last byte, before marking it for boot.

## Flash write pipeline
- Erase the destination block before writing into it; with `stream_flash` (Zephyr) or a similar
  buffer layer, data is accumulated to the write granularity (e.g. 8 bytes, or a 256-byte page)
  and blocks are erased just ahead of the write pointer.
- On resume, the partially written block after the last persisted offset may contain data from
  before the interruption: resume from the start of that block (re-erase it).
- Keep the radio and the flash from contending: on single-bank parts, flash erase stalls code
  execution and can break radio timing; erase while the link is idle or use dual-bank/external flash.

## Integrity per chunk
HTTP over TLS already guarantees integrity in transit; still verify the full image at the end.
For custom transports (BLE, LoRa, UART), add per-chunk CRC and chunk numbers with acks (see
chunk-ack protocol).

## Libraries
- ESP-IDF `esp_https_ota` supports partial downloads (`partial_http_download = true`,
  `max_http_request_size`) and you can resume using `esp_https_ota_begin` with a Range header
  via `http_client_init_cb`.
- Zephyr `download_client` (nRF Connect SDK) + `dfu_target` handle resume with offsets.
- MCUmgr image upload over SMP resumes by offset natively.

## Verify
- [ ] Kill the connection at random points 20 times during a download: completion with correct hash, total bytes transferred < 1.2x image size.
- [ ] Power-cycle mid-download: resumes from the last persisted block.
