---
id: computing-software.web-development.node-express.upload-filenames-and-content-disposition
name: upload-filenames-and-content-disposition
category: computing-software
field: web-development
product: node-express
tags: [filename-sanitization, content-disposition, rfc-6266, path-traversal, rtl-override, file-upload-security]
level: practitioner
status: verified
description: "Handling uploaded file names safely: storage keys vs display names, sanitising Unicode and path characters, RFC 6266 Content-Disposition with UTF-8 names, and spoofed extensions."
sources:
  - https://datatracker.ietf.org/doc/html/rfc6266
  - https://github.com/jshttp/content-disposition
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html#filename-sanitization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upload filenames and Content-Disposition

## 1. Never store under the client's name
```js
const key = `uploads/${tenantId}/${crypto.randomUUID()}${safeExt(detectedType)}`;   // extension from detected type
await db.files.insert({ key, displayName: cleanName(file.originalname), size, mime: detectedType });
```
Client filenames can contain `../`, absolute paths, NUL, reserved Windows names (`CON`, `NUL`, `COM1`), or collide with other users' files.

## 2. Clean the display name
```js
function cleanName(name) {
  return name.normalize("NFC")
    .replace(/[\u0000-\u001f\u007f\u202a-\u202e\u2066-\u2069]/g, "")   // control + bidi override chars
    .replace(/[\/\\:*?"<>|]/g, "_")
    .replace(/^\.+/, "")
    .slice(0, 200) || "file";
}
```
(The class above is written with escapes; the earlier version held the invisible characters literally, which works but is easy to damage when copying.) Bidi overrides (`U+202E`) make `invoice‮fdp.exe` display as `invoiceexe.pdf`; strip them.

## 3. Serving with the right name
```js
import contentDisposition from "content-disposition";
res.setHeader("Content-Disposition", contentDisposition(file.displayName, { type: "attachment" }));
// -> attachment; filename="na?ve.pdf"; filename*=UTF-8''na%C3%AFve.pdf   (content-disposition 2.x replaces non-Latin-1 characters in the fallback with `?`; the `filename*` form carries the real name)
res.setHeader("Content-Type", file.mime);
res.setHeader("X-Content-Type-Options", "nosniff");
```
- `filename*` (RFC 5987/6266) carries UTF-8; `filename` is the ASCII fallback. Hand-built headers with raw quotes or non-ASCII break downloads or allow header injection.
- Framework helpers: Express `res.attachment(name)` / `res.download(path, name)` (Express 4.22 emitted `attachment; filename="naïve.pdf"` with a raw Latin-1 byte in the header for `naïve.pdf` and set `Content-Type` from the extension, so prefer `contentDisposition(name)` explicitly for non-ASCII names); Django `FileResponse(f, as_attachment=True, filename=name)`; Rails `send_data data, filename: name, disposition: "attachment"`; S3 presigned GET with `ResponseContentDisposition`.
- Use `attachment` for anything that is not an image/video you intend to display inline.

## Verify
- [ ] Uploading `../../etc/passwd`, `con.txt`, `résumé.pdf` and a bidi-spoofed name stores safely and downloads with a sensible, correctly encoded name.

## Checked
Run on Windows with Node 20.20.2, Express 4.22.3, multer 2.4.0 (and 1.4.5-lts.2 for the behaviour list), file-type 21.3, sharp 0.35, content-disposition 2.0.1 : `cleanName` on `../../etc/passwd` (`_.._etc_passwd`), `con.txt` (unchanged: reserved Windows names are only safe because stored files get random keys), `résumé.pdf`, a name with U+202E (stripped), a NUL (stripped), `.hidden` (`hidden`) and `...` (`file`); `content-disposition` 2.0.1 output for `naïve.pdf`, `résumé.pdf`, `日本.pdf` and a bidi name (ASCII fallback with `?` plus `filename*=UTF-8''...`); Express `res.attachment`. Not run: Django, Rails, S3 `ResponseContentDisposition`, browser rendering of the bidi name, `nosniff` effects.
