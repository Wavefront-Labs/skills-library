---
id: computing-software.software-engineering.ruby.ruby-numeric-types
name: ruby-numeric-types
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-objects, numeric-types]
level: practitioner
status: docs-checked
description: "Avoid float errors using Integer, Rational or BigDecimal and know division rules."
sources: ["https://docs.ruby-lang.org/en/master/Integer.html", "https://docs.ruby-lang.org/en/master/Float.html", "https://docs.ruby-lang.org/en/master/Rational.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric types Integer Float and Rational
- `Integer#fdiv` returns the Float quotient; `Integer#round` and `Float#round` accept a `half:` option.
- `Float::EPSILON` is the difference between 1 and the smallest double-precision float greater than 1.
- `Rational` represents a number as a/b with integer parts, avoiding float error.
- Compare floats with a tolerance rather than `==`.
Verify: unit tests on sums of 0.1.

## Checked
2026-11-02. Confirmed against: Integer, Float, Rational pages. Removed or softened (not stated on those pages): integer division and modulo examples, BigDecimal details, arbitrary-precision wording.
Method: documentation only; no commands were run.
