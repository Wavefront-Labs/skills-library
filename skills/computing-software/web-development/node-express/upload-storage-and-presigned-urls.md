---
id: computing-software.web-development.node-express.upload-storage-and-presigned-urls
name: upload-storage-and-presigned-urls
category: computing-software
field: web-development
product: node-express
tags: [file-upload-security, secure-file-upload, presigned-urls, upload-storage, s3-presigned-post, direct-to-s3, object-storage, presigned-url, s3-presigned-upload]
level: practitioner
status: draft
description: "Storing uploads outside the webroot via direct-to-S3 presigned POST/PUT with size and type conditions, private buckets and short-lived signed downloads."
sources:
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html
  - https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-HTTPPOSTConstructPolicy.html
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upload storage and presigned URLs

**Goal:** large uploads go straight from the browser to object storage under rules you set, and files are only downloadable by authorised users.

## 1. Why direct-to-storage
Keeps big bodies off app servers (memory, timeouts), scales, and naturally stores outside the webroot. The app only authorises and records metadata.

## 2. Presigned POST with conditions (S3)
```js
import { createPresignedPost } from '@aws-sdk/s3-presigned-post';
const key = `uploads/${req.user.accountId}/${crypto.randomUUID()}`;
const { url, fields } = await createPresignedPost(s3, {
  Bucket: 'app-uploads', Key: key, Expires: 300,
  Conditions: [['content-length-range', 1, 10 * 1024 * 1024], ['eq', '$Content-Type', 'image/png']],
  Fields: { 'Content-Type': 'image/png' },
});
res.json({ url, fields, key });
```
Presigned **POST** can enforce size range and exact content-type; a presigned **PUT** URL cannot enforce max size (only the signed headers), so prefer POST for user uploads or verify size afterwards.

## 3. After upload: verify, then publish
Client tells the app "upload done" with the key -> app checks the object exists, `HeadObject` size/type, then queues a job that downloads, validates magic bytes, re-encodes/scans, and writes the final object to a separate prefix/bucket. Only validated objects are referenced by the app. Use S3 event notifications instead of trusting the client callback when possible.

## 4. Bucket settings
Block Public Access on; bucket policy denies non-TLS (`aws:SecureTransport`); CORS allows only your origin and `POST`/`PUT`; lifecycle rule deletes unvalidated objects in the quarantine prefix after a day and aborts incomplete multipart uploads.

## 5. Downloads
Generate short-lived presigned GET URLs (minutes) **after** an authorization check, with `ResponseContentDisposition=attachment` for untrusted types. Or serve via CloudFront signed URLs/cookies. Never make the bucket public to "fix" access.

## Verify
- [ ] Uploading 11 MB or a different content-type with the presigned form is rejected by S3 (403 policy condition failed).
- [ ] A presigned GET URL stops working after expiry; another user can't obtain one.
- [ ] Quarantine prefix empties via lifecycle.
