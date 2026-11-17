---
id: computing-software.software-engineering.php.php-pcre-regex
name: php-pcre-regex
category: computing-software
field: software-engineering
product: php
tags: [php, php-strings, pcre-regex]
level: practitioner
status: docs-checked
description: "Use preg_* with delimiters, the u flag, named groups, and check preg_last_error."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCRE regular expressions
- `preg_match('/^(?<y>\d{4})-(?<m>\d{2})$/u', $s, $m)`; `preg_replace_callback`, `preg_split`, `preg_quote($s, '/')` for literals.
- Add `/u` for UTF-8; functions return false/null on error: check `preg_last_error_msg()`; backtracking limits (`pcre.backtrack_limit`) cause silent failures.
- Never build patterns from raw user input without `preg_quote`.
Verify: test pathological inputs for backtracking limit.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
