---
id: computing-software.software-engineering.php.php-unserialize-safety
name: php-unserialize-safety
category: computing-software
field: software-engineering
product: php
tags: [php, php-security, unserialize-safety]
level: advanced
status: docs-checked
description: "Avoid object injection: never unserialize untrusted data, and treat eval, extract and shell functions on user input as dangerous."
sources: ["https://www.php.net/manual/en/function.unserialize.php", "https://www.php.net/manual/en/function.eval.php", "https://www.php.net/manual/en/function.extract.php", "https://www.php.net/manual/en/function.escapeshellarg.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unserialize and dangerous functions
- Do not pass untrusted user input to `unserialize()`, regardless of the `allowed_classes` option: the manual says unserialization can result in code being loaded and executed through object instantiation and autoloading. Use `json_decode()` for data from outside.
- `eval()` is described as very dangerous because it allows execution of arbitrary PHP code; its use is discouraged.
- Do not use `extract()` on untrusted data such as `$_GET` or `$_FILES`; if you must, use a non-overwriting flag such as `EXTR_SKIP`.
- Escape individual arguments from user input with `escapeshellarg()` before passing them to `exec()`, `system()` or the backtick operator; better, avoid the shell.

Verify: search the codebase for these functions and review each call site.

## Checked
2026-11-03. Confirmed on the unserialize, eval, extract and escapeshellarg manual pages. Corrected: the original suggested `allowed_classes => false` makes untrusted unserialize acceptable. Removed: `disable_functions` hardening and `composer audit` advice (not on the pages read).
Method: documentation only; no commands were run.
