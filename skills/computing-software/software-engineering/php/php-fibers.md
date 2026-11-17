---
id: computing-software.software-engineering.php.php-fibers
name: php-fibers
category: computing-software
field: software-engineering
product: php
tags: [php, php-fibers, concurrency]
level: advanced
status: docs-checked
description: "Use PHP 8.1 Fibers for cooperative multitasking: start, suspend, resume, throw, and where event loops like Revolt fit."
sources: ["https://www.php.net/manual/en/language.fibers.php", "https://www.php.net/manual/en/class.fiber.php", "https://www.php.net/manual/en/class.fibererror.php", "https://revolt.run/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fibers

A Fiber runs a callable on its own stack; `Fiber::suspend()` pauses it and hands a value to whoever called `start()` or `resume()`.
```php
$fiber = new Fiber(function (string $x): string {
    $y = Fiber::suspend($x . '1');      // pauses; value goes to the start()/resume() caller
    echo "got $y\n";
    $z = Fiber::suspend($y . '2');
    return $z . '3';
});
$a = $fiber->start('a');        // 'a1'
$b = $fiber->resume('b');       // prints "got b", returns 'b2'
$fiber->resume('c');            // fiber finishes
$fiber->isTerminated();         // true
$fiber->getReturn();            // 'c3'
// $fiber->throw(new RuntimeException('cancel')) resumes a suspended fiber by raising the exception at the suspend point
```
Fibers are cooperative: they switch only at `Fiber::suspend()`. Cooperative multitasking needs a single scheduler (an event loop); Revolt provides one, and Amp and ReactPHP build on or share this idea (per revolt.run). Install with `composer require revolt/event-loop`.

## Gotchas
- `FiberError` is thrown for an invalid operation on a Fiber (for example, resuming a fiber that is not suspended).
- `Fiber::suspend()` inside `try` does not run `finally` until the fiber is resumed or garbage collected; this differs from `Generator::throw()`, which runs it immediately.
- Switching fibers inside an object destructor was not allowed before PHP 8.4.0.
- Do not hand-roll schedulers in application code; use a library.

Verify: run the example and check the output order and return values.

## Checked
2026-11-03. Confirmed on the Fibers, Fiber, FiberError manual pages and revolt.run: API names, `finally` behaviour, destructor note, Revolt description and install command. Removed (not on the pages read): "stackful vs generator" comparison, single-thread and blocking-call claims, AMPHP/ReactPHP version numbers, shared-globals note, Xdebug version claim.
Method: documentation only; no commands were run.
