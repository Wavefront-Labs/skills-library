---
id: computing-software.software-engineering.refactoring.replace-magic-literal
name: replace-magic-literal
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, replace-magic-literal, magic-numbers, named-constants, enums, organizing-data]
level: intro
status: docs-checked
description: "Replace magic numbers and strings with named constants, enums or configuration, choosing which literals need names and avoiding meaningless constant names."
sources: ["https://martinfowler.com/books/refactoring.html", "https://eslint.org/docs/latest/rules/no-magic-numbers", "https://docs.astral.sh/ruff/rules/magic-value-comparison/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Magic Literal

**Motivation:** a literal whose meaning isn't obvious (`0.0825`, `86400`, `"PND"`, `3`) forces
readers to guess, and the same value copied in many places changes inconsistently.

## Mechanics
1. Declare a constant with a name that says what it means, not what it is:
   `STANDARD_GRAVITY = 9.81`, `MAX_LOGIN_ATTEMPTS = 3`, `SECONDS_PER_DAY = 86_400`.
2. Find every occurrence of the literal. Replace **only those with the same meaning**: the `3` for
   login attempts is unrelated to the `3` in `retries = 3`.
3. Test after each replacement or batch.

## Choose the right replacement
| Literal kind | Replace with |
|---|---|
| Fixed fact | named constant |
| Closed set of codes (`"PND"`, `"SHP"`) | enum / union type (`OrderStatus.PENDING`) |
| Value that varies by environment or business decision (tax rate, timeout) | configuration, not a constant |
| Value derived from others | expression or function (`SECONDS_PER_DAY = 24 * 60 * 60`) |
| Units | typed values (`Duration.ofDays(1)`, `timedelta(days=1)`) beat bare ints |

## Don't overdo it
- `0`, `1`, `-1`, `""`, `2` in `x / 2` for halving are usually clear in context. A constant named
  `ONE = 1` or `TEN = 10` adds nothing.
- Test data literals are often clearer inline.
- A constant used once whose meaning is obvious from the line can stay a literal with a comment.

## Linters
ESLint `no-magic-numbers` (it has an `ignore` option for numbers you accept) and Ruff `PLR2004`
(magic value used in comparison). Other languages have equivalents; look up your linter. Use them as prompts for
review, not absolute rules.

## Checked
2026-11-01. Confirmed against the ESLint `no-magic-numbers` page and the Ruff `PLR2004` rule page: both rule names and the
ESLint `ignore` option. Removed the Sonar, Pylint and Checkstyle rule names and the specific ignore list (not confirmable).
The constants and literals in the examples are illustrations, not claims.
Method: documentation only; no commands were run.
