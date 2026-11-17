---
id: computing-software.web-development.node-express.path-traversal-prevention
name: path-traversal-prevention
category: computing-software
field: web-development
product: node-express
tags: [broken-access-control, authorization, path-traversal, directory-traversal, path-resolve, zip-slip, file-download, sendfile]
level: practitioner
status: verified
description: "Preventing path traversal in file downloads and archive extraction: resolve-and-contain checks, express sendFile root option, ids instead of names, zip-slip."
sources:
  - https://owasp.org/www-community/attacks/Path_Traversal
  - https://nodejs.org/api/path.html#pathresolvepaths
  - https://expressjs.com/en/api.html#res.sendFile
  - https://security.snyk.io/research/zip-slip-vulnerability
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Path traversal prevention

**Goal:** user input can never make the server read or write files outside the intended directory.

## 1. The bug
```js
app.get('/files/:name', (req, res) => res.sendFile(path.join(__dirname, 'uploads', req.params.name)));
// GET /files/..%2F..%2F.env   -> reads secrets
```
`path.join` normalises `..` - it does not contain it. Reproduced on Express 4.22 and 5.3: `/files/..%2Fsecret.txt` and `..%5C` (backslash form) both return the file outside `uploads`. `express.static` and `sendFile(name, { root })` are safe: the same requests got 404 and 403.

## 2. Best: don't use user-supplied paths
Store files under server-generated names (UUID), keep the original filename in the DB, look up by id after an authorization check. Then traversal is impossible by construction.

## 3. If names must come from input: resolve and contain
```js
import path from 'node:path';
const ROOT = path.resolve('uploads');
function safeJoin(root, userPath) {
  const p = path.resolve(root, userPath);
  if (p !== root && !p.startsWith(root + path.sep)) throw Object.assign(new Error('bad path'), { status: 400 });
  return p;
}
```
- Compare with `root + path.sep`, or `/uploads-old` passes a `startsWith('/uploads')` check.
- Reject NUL bytes; on Windows also consider `\` and drive letters (`path.resolve` handles them on Windows hosts).
- Symlinks inside the root can still point out: `fs.realpath` the result and re-check if users can create symlinks.

Express `res.sendFile(name, { root: ROOT })` rejects paths escaping `root` (returns 403) - pass the user part as the first argument and the directory as `root`. `express.static` is safe by design.

## 4. Archive extraction (zip slip)
Entries like `../../etc/cron.d/x` write outside the target. For each entry, `safeJoin(dest, entry.path)` before writing; skip symlink entries; limit total size and entry count (zip bombs).

## 5. Other languages
Python: `Path(root, user).resolve().is_relative_to(root.resolve())`; Django's `FileSystemStorage` validates names. Rails: `send_file` with `File.expand_path` check, or Active Storage.

## Verify
- [ ] Tests for `../`, `..%2f`, `%2e%2e/`, `....//`, absolute paths and NUL return 400/404.
- [ ] Extracting a crafted zip with traversal entries writes nothing outside dest.
- [ ] Download route checks the requesting user may access that file id.
## Checked
Run on Windows, Node 20.20, Express 4.22.3 and 5.3.0 (real servers plus fetch): the `sendFile(path.join(...))` traversal (`%2F`, `%2e%2e%2f`, `%5C`) leaks the file; `{ root }` gives 403; `express.static` gives 404; a NUL byte in a `{ root }` name gives 400. `safeJoin` rejected `../secret.txt`, `../uploads-old/x.txt` (a naive `startsWith(root)` accepts it) and absolute `/etc/passwd`.
Windows versus Linux: on Windows `path.resolve` also treats backslash and drive-letter prefixes as separators and roots, so a backslash name escapes with `path.join`; on Linux backslash is an ordinary filename character. Not checked: Linux, zip-slip extraction with a real archive library, `fs.readFile` with a NUL byte, symlinks inside root (resolve does not follow them; use `fs.realpath`).
Linux pass (Node 20.20.2 musl build inside a WSL2 busybox distro, Express 4.22.3): `sendFile(path.join(...))` with `..%2F` leaks the file as on Windows, but `..%5C` (backslash) gets 403 there, confirming the backslash escape is Windows-only; `{ root }` 403, NUL 400 and the `startsWith` prefix pitfall are identical.
