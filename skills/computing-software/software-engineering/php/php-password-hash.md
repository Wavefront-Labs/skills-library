---
id: computing-software.software-engineering.php.php-password-hash
name: php-password-hash
category: computing-software
field: software-engineering
product: php
tags: [php, php-security, password-hash]
level: practitioner
status: docs-checked
description: "Store passwords with password_hash/password_verify and rehash when parameters change."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password hashing
- `password_hash($pw, PASSWORD_DEFAULT)` (bcrypt currently, may change) or `PASSWORD_ARGON2ID`; store the full string (column 255 chars).
- `password_verify`, then `password_needs_rehash` and update the stored hash after login.
- Never use md5/sha1 for passwords; compare secrets with `hash_equals`.
Verify: unit tests for verify and rehash.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
