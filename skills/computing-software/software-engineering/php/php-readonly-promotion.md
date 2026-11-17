---
id: computing-software.software-engineering.php.php-readonly-promotion
name: php-readonly-promotion
category: computing-software
field: software-engineering
product: php
tags: [php, php-oop, readonly-promotion]
level: practitioner
status: docs-checked
description: "Write compact immutable value objects with constructor property promotion and readonly."
sources: ["https://www.php.net/manual/en/language.oop5.decon.php", "https://www.php.net/manual/en/language.oop5.properties.php#language.oop5.properties.readonly-properties", "https://www.php.net/manual/en/language.oop5.cloning.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constructor promotion and readonly properties
- `public function __construct(public readonly string $id, private int $n = 0) {}` declares and assigns properties in one place. The constructors page says a visibility modifier is the likeliest trigger for promotion, but any other single modifier (such as `readonly`) has the same effect.
- A readonly property (PHP 8.1.0) can be initialised once, from inside the declaring scope; modifying it afterwards throws `Error`.
- Objects held in a readonly property are still mutable internally.
- To get a changed copy: build a new object with `new`, or, from PHP 8.5.0, use `clone($this, ['x' => $x])` (the `withProperties` argument), which may update readonly properties on the copy.

Verify: attempt reassignment in a test and expect `Error`.

## Checked
2026-11-03. Confirmed on the constructors, properties (readonly) and cloning manual pages. Removed: the "promotion 8.0" and "readonly classes 8.2" version labels not on these pages (see the readonly-classes skill for 8.2).
Method: documentation only; no commands were run.
