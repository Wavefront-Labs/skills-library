---
id: computing-software.software-engineering.php.php-array-functions
name: php-array-functions
category: computing-software
field: software-engineering
product: php
tags: [php, php-arrays, array-functions]
level: practitioner
status: docs-checked
description: "Use array_map/filter/reduce, spread and sort flags correctly, noting key preservation."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array functions map filter reduce and sorting
- `array_filter` preserves keys (use `array_values` to reindex); `array_map` with multiple arrays; `usort` takes callback returning int (use `<=>`).
- Sorting flags: `sort($a, SORT_STRING)`;
- `array_is_list` (8.1), `array_key_first/last`, `array_column`, `array_combine`, `[...$a, ...$b]` (string keys allowed 8.1).
Verify: test with associative arrays and empty arrays.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
