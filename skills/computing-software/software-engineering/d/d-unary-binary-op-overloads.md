---
id: computing-software.software-engineering.d.d-unary-binary-op-overloads
name: d-unary-binary-op-overloads
category: computing-software
field: software-engineering
product: d
tags: [d-unary-binary-op-overloads, operator-overloading, opbinary, opunary, opbinaryright, opopassign, operator, d]
level: practitioner
status: docs-checked
description: "Overload operators with templated opUnary(string op), opBinary(string op), opBinaryRight, opOpAssign and constrain by op, including commutative and mixed-type cases."
sources:
  - https://dlang.org/spec/operatoroverloading.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opUnary, opBinary, opBinaryRight and opOpAssign

Goal: give your types arithmetic.

```d
struct V2 {
    double x, y;
    V2 opBinary(string op)(V2 r) const if (op == "+" || op == "-") {
        return mixin("V2(x " ~ op ~ " r.x, y " ~ op ~ " r.y)");
    }
    V2 opBinary(string op : "*")(double k) const { return V2(x*k, y*k); }
    V2 opBinaryRight(string op : "*")(double k) const { return this * k; }  // 2.0 * v
    V2 opUnary(string op : "-")() const { return V2(-x, -y); }
    ref V2 opOpAssign(string op)(V2 r) if (op == "+") { x += r.x; y += r.y; return this; }
}
```
- Rewrites: `a + b` -> `a.opBinary!"+"(b)` or `b.opBinaryRight!"+"(a)`, whichever matches better (an error if both match equally); `-a` -> `opUnary!"-"`; `++a` -> `opUnary!"++"` and `a++` is built from it; `a += b` -> `opOpAssign!"+"`.
- Use `string op` template parameter, specialise with `: "*"` or constraints, and `mixin` to generate bodies for groups of operators.
- Mark `const` where appropriate.

Gotchas:
- The D1-style operator overloads are deprecated.
- Comparison and equality are separate (`opEquals`, `opCmp`).

Verify: unittest asserts `2.0 * V2(1,2) == V2(2,4)`.

## Checked
Checked 2026-11-03 against the D spec Operator Overloading page (unary, binary, op-assignment, D1 deprecation). The example's rewrites match the documented ones. Removed: the "else opBinaryRight" ordering (the spec picks the better match) and the `opSub` remark.

Method: documentation only; no commands were run.
