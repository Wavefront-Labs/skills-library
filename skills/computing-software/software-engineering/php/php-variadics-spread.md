---
id: computing-software.software-engineering.php.php-variadics-spread
name: php-variadics-spread
category: computing-software
field: software-engineering
product: php
tags: [php, variadics-spread, functions]
level: intro
status: docs-checked
description: "Write variadic functions with ... and unpack arguments and arrays in PHP, including the positional-after-unpack rule and string-key array spread."
sources: ["https://www.php.net/manual/en/functions.arguments.php", "https://www.php.net/manual/en/migration81.new-features.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variadics and argument unpacking

```php
function sum(int ...$nums): int { return array_sum($nums); }
sum(1, 2, 3);
sum(...[4, 5, 6]);                  // unpack an array into arguments

function log(string $level, string ...$parts): void {}
log('info', 'a', 'b');

$merged = [...$a, ...$b, 'x'];      // array spread; string keys are allowed from PHP 8.1
```
In a declaration, `...` may be used once and must be on the last parameter; normal positional parameters go before it. When calling, `...` can be used more than once, provided every use comes after the positional arguments: `array_merge(...$a, $b)` is a fatal error ("Cannot use positional argument after argument unpacking"), while `array_merge($b, ...$a)` and `array_merge(...$a, ...$c)` are legal. Since PHP 8.1 a named argument may follow an unpack: `foo(...$args, named: $arg)`.

## Gotchas
- With named arguments, a function declared `function myfunc(...$args)` collects named arguments that match no parameter (the manual notes they need no corresponding parameter when `...` is used).
- When mixing named arguments and defaults, arguments with defaults must be specified at the end.

Verify: call `myfunc(...)` with positional and named arguments and `var_dump($args)`.

## Checked
2026-11-03. Confirmed on the function arguments page and the PHP 8.1 new-features page. Removed (not confirmed in fetched text): array-key renumbering example, by-reference variadics, `func_get_args()` remark, stack-limit claim, trailing-comma version, string-key call unpacking claim.
Method: documentation only; no commands were run.
