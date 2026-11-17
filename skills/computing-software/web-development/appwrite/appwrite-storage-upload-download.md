---
id: computing-software.web-development.appwrite.appwrite-storage-upload-download
name: appwrite-storage-upload-download
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, storage, upload, download, files, sdk]
level: practitioner
status: docs-checked
description: "Upload files with storage.createFile, understand automatic chunking above 5MB, and fetch files for view or download."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/storage/upload-download/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move files into and out of a bucket from an SDK.

Upload: call `storage.createFile` with `bucketId`, a `fileId` (use `ID.unique()` to generate one) and the file, as long as you have the proper permission. In the Console use the bucket's Files tab > Add File. The Web SDK expects a `File` object, for example from `document.getElementById('uploader').files[0]`. Other SDKs use an `InputFile` class: Node.js `InputFile.fromPath`, `fromBuffer`, `fromPlainText` (browser environments can pass a `File` directly); Flutter and Dart `InputFile.fromPath`, `fromBytes`.

Large files: files above 5MB need to be uploaded in chunks. Appwrite SDKs do this automatically; without an SDK see the REST API file handling docs.

Read back: `getFile` returns metadata; `getFileDownload`, `getFilePreview` and `getFileView` return a resource URL for downloading, previewing and viewing the file.

Gotcha: an upload only succeeds if the bucket is configured to accept the file type and size.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/storage/upload-download. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the create-permission-on-bucket specific, the progress callback claim, the inline vs attachment disposition and read-permission/file-token claims, the list/update/delete method names (page does not name them), and the invented Verify; InputFile helpers now listed per SDK as on the page; Gotcha reworded to the Console statement.

Method: documentation only; no commands were run.
