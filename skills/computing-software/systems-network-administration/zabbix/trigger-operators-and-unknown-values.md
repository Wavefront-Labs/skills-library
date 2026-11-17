---
id: computing-software.systems-network-administration.zabbix.trigger-operators-and-unknown-values
name: trigger-operators-and-unknown-values
category: computing-software
field: systems-network-administration
product: zabbix
tags: [trigger-operators, unknown, precedence, float-comparison, operators]
level: advanced
status: docs-checked
description: "Know trigger operator precedence, the float tolerance in comparisons and how Unknown propagates through and, or and not."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/triggers/expression
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Operators in descending priority: unary minus, not, * and /, + and -, < <= > >=, = and <>, and, or. Operators other than unary minus and not associate left to right. Write -(-1) and not (not 1) instead of -- or not not.

not, and, or must be lowercase and surrounded by spaces or parentheses.

Comparisons are tolerant: A=B means A is within 0.000001 of B, A<B means A<B-0.000001, and so on. Relations yield 1 when true and 0 when false.

Unknown values (for example, an item with no data):
- Arithmetic with Unknown gives Unknown, even 0 * Unknown. Unknown / 0 is an error.
- Unknown on either side of a comparison gives Unknown.
- 0 and Unknown is 0; 1 and Unknown is Unknown.
- 1 or Unknown is 1; 0 or Unknown is Unknown.
- not Unknown is Unknown.

So an expression such as a and b can still resolve to FALSE when one side is Unknown, but a or b with a FALSE side stays Unknown. A trigger expression that evaluates to Unknown does not change the trigger state (Problem or OK).

String handling: a string operand is cast to numeric when the other operand is numeric or when you use an operator other than = or <>. If the cast fails with =, <> the operands are compared as raw strings; with <, <=, >, >= the result is Unknown.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Trigger expression (current): operator priority table and associativity, lowercase and spacing rule for not/and/or, the 0.000001 comparison definitions, unknown-value results for arithmetic, comparison, and and or, string cast rules, and the unchanged trigger state on Unknown. Removed the unconfirmed sentence about comparing returned strings.

Method: documentation only; no commands were run.
