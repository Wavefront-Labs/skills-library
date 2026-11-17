---
id: computing-software.software-engineering.javascript.js-class-fields-private-and-static
name: js-class-fields-private-and-static
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-class-fields, private-fields, static-blocks, accessors]
level: practitioner
status: docs-checked
description: "Declare class fields, #private elements and static members; know private initialisation timing and static restrictions."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_elements", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Static_initialization_blocks", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Class fields, private and static

- Fields: `class A { x = 1; #secret = 2; static count = 0; static { A.count = 1; } }`.
- Private fields are added before the constructor runs in a base class, or immediately after `super()` returns in a derived class.
- `#private` names are enforced by JavaScript itself; referring to one outside the class is a syntax error. Check for one with `#x in obj`.
- A subclass cannot access a base class's private field. Private static members are accessible only from the class that defines them, so use the class name, not `this`, to reach them.
- A `Proxy` around an instance cannot reach its private elements.
- Static initialization blocks run in order with static field initializers; a superclass's static initialization runs first.

## Checked

Date: 2026-11-03. Confirmed on MDN Classes/Private_elements, Classes/Static_initialization_blocks and Global_Objects/Proxy: private field timing, syntax-error rule, `#x in obj`, subclass and static restrictions, proxy limitation, static block order. Removed as not stated in the pages read: public field initialisation timing, arrow-function field memory cost, accessor and static inheritance remarks, `super()`-before-`this` and overridable-method warnings, the composition advice and the dangling cross-reference. The previous gated marker is gone because no unconfirmed claim remains.

Method: documentation only; no commands were run.
