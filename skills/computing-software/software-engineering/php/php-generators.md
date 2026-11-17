---
id: computing-software.software-engineering.php.php-generators
name: php-generators
category: computing-software
field: software-engineering
product: php
tags: [php, php-functions, generators]
level: advanced
status: docs-checked
description: "Stream large datasets with generators, yield from and Iterator interfaces."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generators and iterators
- `function lines($f) { while (($l = fgets($f)) !== false) { yield $l; } }` holds one item in memory; `yield $k => $v`; `yield from` delegates; `$gen->send($x)` for coroutine-style use.
- Generators are forward-only iterators.
- Use `iterator_to_array($gen, false)` to avoid key collisions.
Verify: compare `memory_get_peak_usage()` against an array version.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
