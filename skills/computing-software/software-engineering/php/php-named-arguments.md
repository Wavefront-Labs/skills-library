---
id: computing-software.software-engineering.php.php-named-arguments
name: php-named-arguments
category: computing-software
field: software-engineering
product: php
tags: [php, php-functions, named-arguments]
level: practitioner
status: docs-checked
description: "Call functions with named arguments, variadic parameters and argument unpacking."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named arguments variadics and spread
- `htmlspecialchars($s, double_encode: false)` skips defaults (PHP 8.0); cannot mix positional after named; duplicates are errors.
- Variadics: `function f(int ...$xs)`; spread `f(...$arr)`; string keys in spread become named arguments (8.1).
- Renaming a parameter in a public API now breaks named-argument callers.
Verify: call with an unknown name and expect Error.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
