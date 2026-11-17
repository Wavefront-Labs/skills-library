---
id: computing-software.web-development.node-express.multer-file-uploads
name: multer-file-uploads
category: computing-software
field: web-development
product: node-express
tags: [multer, multipart-form-data, file-uploads, express-uploads, busboy, node]
level: practitioner
status: verified
description: "Handling multipart uploads in Express with Multer: storage engines, limits, error handling, why fileFilter mimetype is untrusted, streaming to object storage and safe naming."
sources:
  - https://github.com/expressjs/multer#readme
  - https://github.com/sindresorhus/file-type
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multer file uploads

## 1. Configure with limits
```js
import multer from "multer";
const upload = multer({
  storage: multer.memoryStorage(),                         // or diskStorage for large files
  limits: { fileSize: 5 * 1024 * 1024, files: 5, fields: 20, fieldSize: 100 * 1024, parts: 30 },
  fileFilter(req, file, cb) {                              // early reject only; file.mimetype is client-supplied
    cb(null, ["image/jpeg", "image/png", "image/webp"].includes(file.mimetype));
  },
});
app.post("/avatar", requireUser, upload.single("avatar"), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: "No valid file" });
  const type = await fileTypeFromBuffer(req.file.buffer);  // magic-byte check (file-type package)
  if (!type || !["image/jpeg", "image/png", "image/webp"].includes(type.mime)) return res.status(415).end();
  const key = `avatars/${req.user.id}/${crypto.randomUUID()}.${type.ext}`;
  await s3.putObject({ Bucket, Key: key, Body: await reencode(req.file.buffer), ContentType: type.mime });
  res.status(201).json({ key });
});
```
`.single(name)`, `.array(name, max)`, `.fields([{ name, maxCount }])`, `.none()` for text-only multipart.

## 2. Errors
```js
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    const status = err.code === "LIMIT_FILE_SIZE" ? 413 : 400;
    return res.status(status).json({ error: err.code });
  }
  next(err);
});
```
Observed codes (both versions): oversize file `LIMIT_FILE_SIZE` (413 in the handler above), wrong field name `LIMIT_UNEXPECTED_FILE` (400), too many files for `.array(name, max)` `LIMIT_FILE_COUNT`, too many text fields `LIMIT_FIELD_COUNT`, long field value `LIMIT_FIELD_VALUE`. A file rejected by `fileFilter` (`cb(null, false)`) raises no error; `req.file` is simply undefined, hence the 400 in the route. Without limits, a client can stream gigabytes into memory or disk.

## 3. Storage choice
- Memory storage: simplest; only with tight `fileSize` limits.
- Disk storage: never use `file.originalname` in the destination path; generate names; clean temp files after processing (also on errors).
- Large files: stream directly with busboy to object storage, or skip the server entirely with presigned uploads.

## 4. Versions
Multer 1.x is affected by several denial-of-service advisories and 2.x has needed repeated fixes: the GitHub advisory list (fetched 2026-10-18) shows fixes in 2.1.1 (uncontrolled recursion), 2.2.0 (deeply nested field names, incomplete cleanup of aborted uploads), 2.3.0 (crafted and oversized-index field names, a file-size-limit bypass through an async `fileFilter`, descriptor leak on aborted uploads in 2.2.0) and 2.4.0 (orphaned disk writes on aborted uploads in 2.2.x-2.3.x). Use the latest 2.x and re-check the advisories; do not assume any 2.x is safe. Multer only parses `multipart/form-data`; JSON bodies still need `express.json()`.

`file.originalname` is decoded as Latin-1 by default: a client filename `résumé-日本.png` arrived as `rÃ©sumÃ©-æ¥æ¬.png` (same on 1.4.5 and 2.4.0). Pass `defParamCharset: "utf8"` to `multer({...})` to get the real name (checked). Either way, never use the name for the storage path.

## Verify
- [ ] Oversize upload returns 413; a renamed `.exe` with `image/png` mimetype is rejected by the magic-byte check; temp files do not accumulate.

## Checked
Run on Windows with Node 20.20.2, Express 4.22.3, multer 2.4.0 (and 1.4.5-lts.2 for the behaviour list), file-type 21.3, sharp 0.35, content-disposition 2.0.1 against a real server with `fetch` and `FormData`: a valid PNG accepted; an executable renamed with an `image/png` mimetype got past `fileFilter` and was rejected by the magic-byte check (`file-type` detected `application/x-msdownload`, response 415); wrong mimetype rejected by `fileFilter`; the error codes above; the `defParamCharset` fix; and the advisory list fetched from GitHub. Not run: disk storage cleanup, S3, `reencode`, streaming with busboy, the specific advisories themselves. Multer is pure JavaScript; behaviour was not run on Linux.
