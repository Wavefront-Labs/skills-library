---
id: computing-software.software-engineering.refactoring.split-phase
name: split-phase
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-first-set, split-phase, intermediate-data-structure, parse-then-compute, separation-of-concerns, pipeline]
level: practitioner
status: verified
description: "Split code that does two things in sequence (parse then compute, compute then format) into two phases connected by an explicit intermediate data structure."
sources: ["https://refactoring.com/catalog/splitPhase.html", "Refactoring, 2nd ed. (Fowler), ch1 example and ch6 Split Phase"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Split Phase

**Goal:** separate code that deals with two different concerns in sequence so each
phase can be understood, tested and changed alone.

## Typical candidates
- Parsing input (CSV, CLI args, HTTP body) mixed with business calculation.
- Calculating results mixed with rendering them (text, HTML, JSON) - Fowler's
  "statement" example in chapter 1.
- Compilers: lexing, parsing, analysis, code generation are the archetype.

## Mechanics
1. Extract the second-phase code into its own function. Test.
2. Introduce an intermediate data structure as an additional argument to that function. Test.
3. Examine each parameter of the extracted second phase. If it is used by the first
   phase, move it into the intermediate structure. Test after each move.
4. Apply Extract Function on the first-phase code, returning the intermediate structure.

Before:
```python
def price_order(product_line: str, qty: int, shipping: ShippingMethod) -> str:
    fields = product_line.split(",")
    price = Decimal(fields[1]) * qty
    discount = max(qty - 100, 0) * Decimal(fields[1]) * Decimal("0.05")
    return f"{price - discount + shipping.cost(qty):.2f}"
```
After:
```python
@dataclass(frozen=True)
class OrderData:               # intermediate structure
    unit_price: Decimal
    quantity: int

def parse_order(product_line: str, qty: int) -> OrderData:
    return OrderData(Decimal(product_line.split(",")[1]), qty)

def price(order: OrderData, shipping: ShippingMethod) -> Decimal:
    base = order.unit_price * order.quantity
    discount = max(order.quantity - 100, 0) * order.unit_price * Decimal("0.05")
    return base - discount + shipping.cost(order.quantity)

def price_order(product_line, qty, shipping) -> str:
    return f"{price(parse_order(product_line, qty), shipping):.2f}"
```

Run (Python 3.14 with a stub `ShippingMethod` costing 5.00): the before and after versions returned identical strings for quantities 1, 100, 101 and 250 (250 units at 9.99 gives 2427.58).

## Benefits
- The calculation is testable without strings; the parser testable without pricing.
- Adding a new input format or output renderer touches only one phase.
- The intermediate structure documents exactly what flows between phases.

## Verify
- [ ] The second phase does not receive raw first-phase input (no strings/IO objects).
- [ ] Each phase has its own unit tests.
