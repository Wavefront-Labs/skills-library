---
id: computing-software.software-engineering.php.php-file-uploads
name: php-file-uploads
category: computing-software
field: software-engineering
product: php
tags: [php, php-security, file-uploads]
level: advanced
status: docs-checked
description: "Validate uploads, avoid path traversal and store files outside the web root."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File uploads and path handling
- Check `$_FILES['f']['error'] === UPLOAD_ERR_OK`, use `is_uploaded_file` and `move_uploaded_file`; detect type with `finfo` (not client MIME or extension); generate your own filename.
- Store outside the document root or serve through a handler; set size limits (`upload_max_filesize`, `post_max_size`).
- Path traversal: resolve with `realpath()` and check the prefix; never include user paths (LFI/RFI: `allow_url_include=Off`).
Verify: upload a PHP file with image extension in tests.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
