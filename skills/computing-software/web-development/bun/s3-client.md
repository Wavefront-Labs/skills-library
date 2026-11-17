---
id: computing-software.web-development.bun.s3-client
name: s3-client
category: computing-software
field: web-development
product: bun
tags: [bun-s3, s3-presign, s3-multipart, s3-compatible-storage]
level: practitioner
status: docs-checked
description: "Use Bun's built-in S3 client with AWS, R2, MinIO and other endpoints: credentials, S3File reads and writes, presigned URLs, listing and multipart uploads."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/s3.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Credentials come from `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_REGION`, `S3_ENDPOINT`, `S3_BUCKET`, `S3_SESSION_TOKEN`, each falling back to its `AWS_*` name. `Bun.s3` uses them; constructor options override.

```ts
import { S3Client, s3 } from "bun";
const r2 = new S3Client({
  accessKeyId: "key", secretAccessKey: "secret", bucket: "media",
  endpoint: "https://<account-id>.r2.cloudflarestorage.com",
});
const f = r2.file("data.json");            // lazy S3File (extends Blob)
await f.write(JSON.stringify(obj), { type: "application/json" });
const head = await r2.file("video.mp4").slice(0, 1024).bytes(); // HTTP Range
const url = r2.file("incoming/photo.jpg").presign({ method: "PUT", expiresIn: 900, type: "image/jpeg" });
await f.delete();

const w = r2.file("big.bin").writer({ partSize: 5 * 1024 * 1024, queueSize: 4, retry: 3 });
w.write(chunk); await w.flush(); await w.end();   // multipart
```

- Presign is synchronous (no network); default GET, 24 hours. `new Response(s3file)` returns a 302 to a presigned URL.
- `S3Client.list(options, creds)` returns up to 1,000 objects; if `isTruncated`, pass the last key as `startAfter`.
- Virtual-hosted endpoints need `virtualHostedStyle: true`; AWS defaults region to `us-east-1`.

Gotchas: `size` is `NaN` and deprecated, use `stat()`; env vars are read at initialization; errors carry codes like `ERR_S3_MISSING_CREDENTIALS`.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/s3: S3_* variables with AWS_* fallback, constructor options overriding defaults, lazy S3File extending Blob, write with type, slice using the HTTP Range header, presign being synchronous with GET and 24 hour defaults and the method/expiresIn/type options, new Response(S3File) returning a 302, multipart writer options partSize/queueSize/retry, list up to 1,000 objects with isTruncated and startAfter, virtualHostedStyle, us-east-1 region default, size being NaN and deprecated in favour of stat(), environment read at initialization, and ERR_S3_* error codes. Nothing removed.
Method: documentation only; no commands were run.
