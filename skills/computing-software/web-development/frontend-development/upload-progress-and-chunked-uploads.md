---
id: computing-software.web-development.frontend-development.upload-progress-and-chunked-uploads
name: upload-progress-and-chunked-uploads
category: computing-software
field: web-development
product: frontend-development
tags: [fetch-api, browser-networking, upload-progress, chunked-upload, xmlhttprequest-upload, resumable-upload, tus, multipart-upload, presigned-urls]
level: practitioner
status: docs-checked
description: "Showing upload progress (XHR upload events, since fetch lacks them) and uploading large files in resumable chunks via tus or S3 multipart presigned URLs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/upload
  - https://tus.io/protocols/resumable-upload
  - https://github.com/awsdocs/amazon-s3-userguide/blob/main/doc_source/mpuoverview.md
  - https://github.com/awsdocs/amazon-s3-userguide/blob/main/doc_source/qfacts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upload progress and chunked uploads

**Goal:** large uploads show accurate progress and survive flaky connections without restarting from zero.

## 1. Progress needs XHR
`fetch` has no upload progress events (streaming request bodies with `duplex: "half"` are experimental, Chromium only per MDN compatibility data). `XMLHttpRequest.upload` fires `progress` events:
```js
function upload(url, file, onProgress, signal) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('PUT', url);
    xhr.upload.onprogress = (e) => e.lengthComputable && onProgress(e.loaded / e.total);
    xhr.onload = () => (xhr.status < 300 ? resolve(xhr) : reject(new Error(`HTTP ${xhr.status}`)));
    xhr.onerror = () => reject(new Error('network error'));
    signal?.addEventListener('abort', () => xhr.abort());
    xhr.send(file);
  });
}
```
Progress reaching 100% means bytes left the browser, not that the server finished processing - show "Processing…" until `onload`.

## 2. Chunking for big files
Split with `file.slice(start, end)`. For S3 multipart uploads each part must be 5 MiB to 5 GiB (the last part has no minimum) and an upload has at most 10,000 parts (AWS S3 user guide, 2023 snapshot).

### S3 multipart with presigned URLs
1. Server: `CreateMultipartUpload`, returns `uploadId`.
2. Server presigns `UploadPart` URLs for part numbers.
3. Client PUTs each chunk and records the `ETag` response header for each part number (a cross-origin page can only read it if the bucket CORS configuration exposes it).
4. Server: `CompleteMultipartUpload` with the upload ID and the list of part numbers and ETags. There is no expiry on an unfinished upload: complete or abort it, or you keep paying for stored parts (a lifecycle rule can abort incomplete uploads).

### tus protocol
Open resumable-upload protocol (1.0.x): the creation extension uses `POST`, `PATCH` with `Upload-Offset` sends data, and `HEAD` returns the current offset so a resumed upload continues where it stopped. To resume after a page reload you must keep the upload URL yourself.

## 3. Resilience
Retry failed chunks with backoff; only the failed chunk is resent. Keep the page alive (warn on `beforeunload` while uploading).

## Verify
- [ ] Progress bar moves smoothly on a throttled network and switches to "Processing" at 100%.
- [ ] Drop the network mid-upload: resumes from the last completed chunk.
- [ ] Abandoned multipart uploads are cleaned up by lifecycle rule.

## Checked

Checked 2026-10-26 against mdn/content (main) XMLHttpRequest.upload and Request.duplex (plus mdn/browser-compat-data), the tus 1.0.x protocol text (tus/tus.io) and the AWS S3 user guide multipart pages (awsdocs/amazon-s3-userguide, last commit June 2023; the repository is an archived snapshot, so re-check limits on the live page).

- Confirmed: `xhr.upload` exposes `progress`; S3 parts are 5 MiB to 5 GiB with no minimum on the last part and at most 10,000 parts; S3 returns an `ETag` per part and the complete request needs part numbers with ETags; unfinished uploads have no expiry and incur storage charges until completed or stopped; tus uses `HEAD` for the offset, `PATCH` with `Upload-Offset` for data and `POST` under the creation extension.
- Removed: the 100 MB upper chunk size, "3-4 in parallel", the `tus-js-client`/`tusd` names and the localStorage fingerprint advice, which the pages checked do not state.

Method: documentation only; no commands were run.
