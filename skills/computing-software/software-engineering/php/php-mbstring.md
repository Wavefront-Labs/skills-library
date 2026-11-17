---
id: computing-software.software-engineering.php.php-mbstring
name: php-mbstring
category: computing-software
field: software-engineering
product: php
tags: [php, php-strings, mbstring]
level: practitioner
status: docs-checked
description: "Handle UTF-8 text with mb_* functions instead of byte-oriented str* functions."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multibyte strings with mbstring
- `strlen('é')` is 2 (bytes); use `mb_strlen($s, 'UTF-8')`, `mb_substr`, `mb_strtoupper`, `mb_str_split`.
- Set `default_charset=UTF-8` and `mb_internal_encoding('UTF-8')`; `mb_check_encoding($s, 'UTF-8')` validates input.
- `ucfirst`, `str_pad` etc. are not multibyte-safe (check 8.x additions such as `mb_str_pad` in later versions).
Verify: test with emoji and combining accents.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
